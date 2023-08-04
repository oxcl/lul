#!/usr/bin/env python3
import requests
import os
import sys
import json

def log(message):
    time = time.strftime("%Y-%m-%d %H:%M")
    print(f"[{time}] {message}",file=sys.stderr)
    
def get_environ(variable_name,default_value=None):
    try:
        return os.environ[variable_name]
    except:
        if default_value is None:
            log(f"Environment Variable '{variable_name}' must be set for this program to work")
            exit(1)
        else:
            return default_value

ROUTER_IP = get_environ("LUL_ROUTER_IP")
ROUTER_PASSWORD = get_environ("LUL_ROUTER_PASSWORD")
ROUTER_USE_SSL = get_environ("LUL_USE_SSL","no")
DATA_DIR = get_environ("LUL_DATA_DIR",f"{os.path.expanduser('~')}/.lul")
DATABASE_FILE = f"{DATA_DIR}/database.json"
ISP_URL = get_environ("LUL_ISP_URL")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

if os.path.exists(DATABASE_FILE):
    with open(DATABASE_FILE,'r') as file:
        database = json.load(file.read())
else:
    with open(DATABASE_FILE,'w') as file: 
        file.write("{}")