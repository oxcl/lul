# lul - LTE Usage Limiter
constantly monitor lte traffic usage and limit the usage using mwan3

## Setup
```
git clone https://github.com/oxcl/lul ./lul
cd lul
scp ./lul root@router-ip-address:/www/cgi-bin/lul
cp ./nginx.conf /etc/nginx/nginx.conf
(crontab -l; cat ./crontab) | crontab -
```

## Environment Variables
these environment variables should be set in the router
- LUL_ALLOWED_IPS (separated by space)
- LUL_PASSWORD