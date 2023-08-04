# this file should be modified when switching to a new ISP
import json
import os
import sys
import requests
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
        return {"total_traffic": 51200, "remained_traffic": 51200, "total_days":30,"remained_days":29}