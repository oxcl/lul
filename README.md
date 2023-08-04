# lul - LTE Usage Limiter
constantly monitor lte traffic usage and limit the usage using mwan3

## Requirements
- python3
- nginx
- cron

## Setup
```bash
$ git clone https://github.com/oxcl/lul ./lul
$ cd lul
$ vim .env_template # add required variables
$ vim .router_template # add required variables
$ sh ./setup *ROUTER_IP_ADDRESS*
```
you should also add the required environment variables for the lul instance to work properly.
environments are loaded automatically if a `.env` file is available in the lul folder ( a .env_template file is available to make life easy)

fetching information from the ISP requires a `headers.json` file which contains request headers and can optionally use a `req_data.txt` which contains post request data. these files are used for authentication of ISP web service. make sure they are placed correctly at `$LUL_DATA_DIR` which is by default `$HOME/.lul`

make sure `www` user exists for nginx to work

## Environment Variables
required environment variables for the router:
- `LUL_ALLOWED_IPS` (separated by space)
- `LUL_PASSWORD`

required environment variables for the lul instance to work:
- `LUL_ROUTER_URL`
- `LUL_ROUTER_PASSWORD`
- `LUL_ISP_URL`
- `LUL_ROUTER_PROTOCOL` (`http` or `https`. defaults to `http` if not provided)
- `LUL_DATA_DIR` (defaults to `~/.lul` if not provided)
- `LUL_DAY_STARTS_AT` (defaults to 0)