import time
import sys
def log(message):
    now = time.strftime("%Y-%m-%d %H:%M")
    print(f"[{now}] {message}",file=sys.stderr)