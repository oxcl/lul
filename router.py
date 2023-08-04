import requests
from env import *
from util import *

def on():
    res = requests.post(f"{ROUTER_PROTOCOL}://{ROUTER_URL}",data=f"{ROUTER_PASSWORD}:on")
    res_text = res.text.strip()
    if res.status_code != 200:
        log(f"request to turn on lul in router '{ROUTER_URL}' failed with status code '{res.status_code}'")
        log(f"router response: {res_text}")
        exit(1)
    else:
        log(f"router: {res_text}")

def off():
    res = requests.post(f"{ROUTER_PROTOCOL}://{ROUTER_URL}",data=f"{ROUTER_PASSWORD}:off")
    res_text = res.text.strip()
    if res.status_code != 200:
        log(f"request to turn off lul in router '{ROUTER_URL}' failed with status code '{res.status_code}'")
        log(f"router response: {res_text}")
        exit(1)
    else:
        log(f"router: {res_text}")

def is_on():
    res = requests.post(f"{ROUTER_PROTOCOL}://{ROUTER_URL}",data=f"{ROUTER_PASSWORD}:status")
    res_text = res.text.strip()
    if res.status_code != 200:
        log(f"request to get status of lul in router '{ROUTER_URL}' failed with status code '{res.status_code}'")
        log(f"router response: {res_text}")
        exit(1)
    elif res_text == "off":
        return False
    elif res_text == "on":
        return True
    else:
        log(f"invalid response from router '{ROUTER_URL}' when obtaining lul status: '{res_text}'")
        exit(1)
