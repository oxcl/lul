import jdatetime
import datetime
import os
from env import *
# log certain data to WWW_DIR so that it can be used to draw graphs and display information in the web interface
# data is separated month by month into different files formatted in this way: YYYY-MM
# every data is saved twice once with normal date month separation into WWW_DIR/db and once with jalali month separation in WWW_DIR/db/jalali
def monitor(**kwargs):
    date = datetime.date.fromtimestamp(kwargs["time"])
    jdate = jdatetime.date.fromtimestamp(kwargs["time"])
    file_path = f"{WWW_DIR}/db/{date.year}-{date.month}.csv"
    jfile_path = f"{WWW_DIR}/db/jalali/{jdate.year}-{jdate.month}.csv"
    # create database files if they don't exist
    for date_file in {file_path,jfile_path}:
        if not os.path.exists(date_file):
            with open(date_file,'w') as file:
                file.write(",".join([title for title in kwargs.keys()]))
                file.write("\n")

    for date_file in {file_path,jfile_path}:
        with open(date_file,'a') as file:
            file.write(",".join([str(int(item)) for item in kwargs.values()]))
            file.write("\n")