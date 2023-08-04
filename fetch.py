# this file should be modified when switching to a new ISP
import json
import os
import re
import requests
import jdatetime
from datetime import datetime
from env import *
from util import *
def fetch():
    """
    fetch information from ISP to determine how much traffic has been used.
    this function cuold be modified depending on the ISP that is used at the time.
    it should always return a dict with four items: total_traffic, remained_traffic, total_days, remained_days
    """
    headers_file = f"{DATA_DIR}/headers.json"
    if not os.path.exists(headers_file):
        log(f"No headers file exists at '{headers_file}'. headers file is required to send requests to ISP")
        exit(1)
    with open(headers_file,'r') as file:
        headers = json.load(file)
    
    req_data_file = f"{DATA_DIR}/req_data.txt"
    if os.path.exists(req_data_file):
        with open(req_data_file,'r') as file:
            req_data = file.read()
    else:
        req_data = None
    
    res = requests.post(ISP_URL,headers=headers,data=req_data)
    if res.status_code != 200:
        log(f"request to ISP returned with status code: '{res.status_code}'. exitting.")
        log(f"response_text: {res.text}")
        exit(1)
    data = res.json()
    if len(data["internet_packages"]) == 0:
        return {"total_traffic": 51200, "remained_traffic": 0, "total_days":30,"remained_days":29}
    else:
        start_date_raw = data["internet_packages"][0]["startDate"]
        start_date = datetime.strptime(start_date_raw,"%Y-%m-%dT%H:%M:%S+03:30")
        expire_time_raw = data["internet_packages"][0]["expire"]
        expire_time = jdatetime.date(*[int(x) for x in expire_time_raw.split('/')]).togregorian()
        expire_date = datetime(expire_time.year,expire_time.month,expire_time.day)
        total_days = ( expire_date - start_date ).days
        total_days = total_days + 1 # because isp reports 30 days as 29 days
        remained_days = (expire_date - datetime.today()).days
        remained_days = remained_days + 1 # because isp reports 30 days as 29 days

        remained_traffic_raw = data["internet_packages"][0]["remained"]
        remained_traffic = re.findall("\d",remained_traffic_raw)
        remained_traffic = "".join(remained_traffic)
        remained_traffic = int(remained_traffic)

        name = data["internet_packages"][0]["name"]
        total_traffic_raw = name.split("-")[1]
        total_traffic = re.findall("\d",total_traffic_raw)
        total_traffic = "".join(total_traffic)
        total_traffic = int(total_traffic) * 1024

        return {
            "total_traffic":total_traffic,
            "remained_traffic":remained_traffic,
            "total_days": total_days,
            "remained_days":remained_days
        }

        exit()