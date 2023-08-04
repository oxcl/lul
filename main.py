#!/usr/bin/env python3
import requests
import os
import json
import time
import datetime
from env import *
from util import *
from fetch import fetch
import router
from dotenv import load_dotenv

# load .env file if exists
load_dotenv()

log("program has started.")

if not os.path.exists(DATA_DIR):
    log(f"creating '${DATA_DIR}' folder")
    os.makedirs(DATA_DIR)

database_file = f"{DATA_DIR}/database.json"
if os.path.exists(database_file):
    with open(database_file,'r') as file:
        log(f"loading database from '{database_file}'")
        database = json.load(file)
else:
    with open(database_file,'w') as file: 
        log(f"database does not exist at '{database_file}'. creating it.")
        file.write("{}")
        database = {}

now = time.time()

# if standby mode is on ensure standby time is due or else exit the program
if "standby" in database and database["standby"] == True:
    standby_until_time = database["standby_until"]
    if now < standby_until_time:
        log(f"standby mode is on until: {time.ctime(standby_until_time)}. exitting.")
        exit(0)

log("fetching new information from ISP.")
isp_data = fetch()
log(isp_data)
total_traffic = isp_data["total_traffic"]
remained_traffic = isp_data["remained_traffic"]
total_days = isp_data["total_days"]
remained_days = isp_data["remained_days"]

if total_traffic == 0:
    log("total traffic is 0. perhaps no internet package is active. enabling lul in the router.")
    router.on()
    log("exitting")
    exit(0)

# should today's share be included in calculations or not
is_new_day = int(time.strftime('%H')) >= DAY_STARTS_AT
# calculate how much traffic is allowed for each day
daily_traffic_share = total_traffic / total_days
# calculate how much traffic was used
used_traffic = total_traffic - remained_traffic
# calculate how much traffic is allowed to be used for the passed days
traffic_limit = daily_traffic_share * (total_days - remained_days + (1 if is_new_day else 0) )

log(f"is_new_day: {is_new_day}, used_traffic: {used_traffic}, traffic_limit: {traffic_limit}")

if used_traffic >= traffic_limit:
    log(f"used traffic exceeds traffic limit. enabling lul in the router.")
    router.on()
    log(f"enabling standby mode until tomorrow at {DAY_STARTS_AT} o'clock.")
    standby_until_time = datetime.datetime.today() + datetime.timedelta(days=1)
    standby_until_time = standby_until_time.replace(hour=DAY_STARTS_AT,minute=0,second=0)
    standby_until_time = int(standby_until_time.strftime("%s")) # convert to epoch
    new_database = {"standby":True,"standby_until": standby_until_time}
    with open(database_file,'w') as file:
        json.dump(new_database,file)
else:
    log(f"used traffic has not reached the limit yet. disabling lul if enabled")
    router.off()
log("exitting")