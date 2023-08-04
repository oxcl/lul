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

ROUTER_IP = get_environ("LUL_ROUTER_IP")
ROUTER_PASSWORD = get_environ("LUL_ROUTER_PASSWORD")
ROUTER_USE_SSL = get_environ("LUL_USE_SSL","no")
DATA_DIR = get_environ("LUL_DATA_DIR",f"{os.path.expanduser('~')}/.lul")
DATABASE_FILE = f"{DATA_DIR}/database.json"
ISP_URL = get_environ("LUL_ISP_URL")