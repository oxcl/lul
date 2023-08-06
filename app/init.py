import json
from util import *
from env import *
def init(database_path):
    log("program has started.")

    if not os.path.exists(DATA_DIR):
        log(f"creating '${DATA_DIR}' folder")
        os.makedirs(DATA_DIR)

    # make sure database folders for www database exists
    www_db = f"{WWW_DIR}/db/jalali"
    if not os.path.exists(www_db):
        log(f"creating ${www_db} folder")
        os.makedirs(www_db)

    if os.path.exists(database_path):
        with open(database_path,'r') as file:
            log(f"loading database from '{database_path}'")
            database = json.load(file)
    else:
        with open(database_path,'w') as file: 
            log(f"database does not exist at '{database_path}'. creating it.")
            file.write("{}")
        database = {}
    return database