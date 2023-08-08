#!/usr/bin/env python3

# load .env file if exists
from dotenv import load_dotenv
load_dotenv()

import json
import time
from env import *
from util import *
from fetch import fetch
from init import init
import www
import router

database_path = f"{DATA_DIR}/database.json"
database = init(database_path)
new_database = {}

now = time.time()

# if standby mode is on ensure standby time is due or else exit the program
if "standby" in database and database["standby"] == True:
    standby_until_time = database["standby_until"]
    if now < standby_until_time:
        log(f"standby mode is on until: {time.ctime(standby_until_time)}. exitting.")
        exit(0)

log(f"router status: {'on' if router.is_on() else 'off'}")

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
# calculate how much traffic is allowed to be used
traffic_limit = daily_traffic_share * (total_days - remained_days + (1 if is_new_day else 0) )

log(f"is_new_day: {is_new_day}, used_traffic: {used_traffic}, traffic_limit: {traffic_limit}")


if used_traffic >= traffic_limit:
    log(f"used traffic exceeds traffic limit. enabling lul in the router.")
    router.on()
    # NOTE: standby is disabled for now to have more excesive logs in www/db
    # log(f"enabling standby mode until tomorrow at {DAY_STARTS_AT} o'clock.")
    # standby_until_time = datetime.datetime.today() + datetime.timedelta(days=1)
    # standby_until_time = standby_until_time.replace(hour=DAY_STARTS_AT,minute=0,second=0)
    # standby_until_time = int(standby_until_time.strftime("%s")) # convert to epoch
    # new_database["standby"] = True
    # new_database["standby_until"] = standby_until_time
else:
    log(f"used traffic has not reached the limit yet. disabling lul if enabled")
    router.off()

# log data to WWW_DIR/db
router_is_on = router.is_on()
www.monitor(
    time=now * 1000, # javascript reads time in milliseconds
    total_traffic=total_traffic,
    remained_traffic=remained_traffic,
    usage = (database["last_saved_traffic"] - remained_traffic) if ( "last_saved_traffic" in database ) else 0,
    required_traffic_in_reserve= total_traffic - traffic_limit,
    lul_status= router_is_on
)
www.send_data(
    total_traffic_share = traffic_limit - used_traffic,
    daily_traffic_share = daily_traffic_share,
    day_starts_at = DAY_STARTS_AT,
    lul_is_on = router_is_on
)

new_database["last_saved_traffic"] = remained_traffic
with open(database_path,'w') as file:
    json.dump(new_database,file)

log("exitting")