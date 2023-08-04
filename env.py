import os
from util import *
def get_environ(variable_name,default_value=None):
    try:
        return os.environ[variable_name]
    except:
        if default_value is None:
            log(f"Environment Variable '{variable_name}' must be set for this program to work")
            exit(1)
        else:
            return default_value

ROUTER_URL = get_environ("LUL_ROUTER_URL")
ROUTER_PASSWORD = get_environ("LUL_ROUTER_PASSWORD")
ROUTER_PROTOCOL = get_environ("LUL_ROUTER_PROTOCOL","http")
DATA_DIR = get_environ("LUL_DATA_DIR",f"{os.path.expanduser('~')}/.lul")
ISP_URL = get_environ("LUL_ISP_URL")
DAY_STARTS_AT = int(get_environ("LUL_DAY_STARTS_AT","0")) # at what hour of the day should the traffic share for the day be allocated