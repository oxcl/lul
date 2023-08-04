#!/usr/bin/env python3
import requests
import os
import sys
import json
import time
from env import *
from util import *
from fetch import fetch


log("program has started.")

if not os.path.exists(DATA_DIR):
    log(f"creating '${DATA_DIR}' folder")
    os.makedirs(DATA_DIR)

if os.path.exists(DATABASE_FILE):
    with open(DATABASE_FILE,'r') as file:
        log(f"loading database from '{DATABASE_FILE}'")
        database = json.load(file)
else:
    with open(DATABASE_FILE,'w') as file: 
        log(f"database does not exist at '{DATABASE_FILE}'. creating it.")
        file.write("{}")
        database = {}

# if standby mode is on ensure standby time is due or else exit the program
if "standby" in database and database["standby"] == True:
    standby_until_time = database["standby_until"]
    if time.time() < standby_until_time:
        log(f"standby mode is on until: {time.ctime(standby_until_time)}. exitting.")
        exit(0)

