# Uptime Checker
An `Uptime Checker`, also called an `Uptime Monitor`, is a tool that checks whether a website, API, or server is online and responding properly.

The tool sends regular `HTTP` or `HTTPS` requests to a list of URLs and reports whether each one is `up` (responding correctly), or `down` (not reachable or returning an error).

## How it works
The tool works like this:

+ It sends a small request - often a `HEAD` or `GET` request - to the website e.g. `GET https://example.com`.
+ The tool then checks the status code in response. `200-399`, the site is up. `400-599`, the site is down and/or has an error.
+ This process is repeated on a schedule.
+ The results can be reported through: `logging to a file`, `dashboard`, or `alerting system`.

## Why is this useful?
+ `Detects outages quickly`, before users do.
+ Helps `measure uptime percentage` (e.g, 99.95%).
+ `Triggers alerts` (Email, Slack, SMS) when the site goes down.
+ Tracks the response time for performance monitoring.

## Setup the Uptime Checker tool
To run the `Uptime Checker` tool, `Python` needs to be installed. Begin be checking that `Python` is installed on your machine:

```shell
$ python3 --version
```

The repository can be cloned using `Git`. `SSH` has been setup:

```shell
$ git clone git@github.com:hackdanismo/automation.git
```

Once cloned, change directory to the subfolder containing the `uptime-checker` code and install the dependencies:

```shell
# Change directory into the main project folder
$ cd automation
# Change directory into the subfolder containing the uptime-checker tool
$ cd uptime-checker

# Setup the Virtual Environment to create the venv folder
$ python3 -m venv venv
# Activate the Virtual Environment
$ source venv/bin/activate

# Install the dependencies listed in the requirements.txt file
$ pip3 install -r requirements.txt
```

## Run the Uptime Checker tool
Once setup has been completed, the following process can be used to run the tool:

```shell
# Change directory into the main project folder
$ cd automation
# Change directory into the subfolder containing the uptime-checker tool
$ cd uptime-checker

# Activate the Virtual Environment
$ source venv/bin/activate

# Run the Python script containing the code for the tool locally
$ LOCAL_LOOP=1 python3 index.py

# To close the tool and end the Virtual Environment session
$ deactivate
```

By default, the script is setup to run using a scheduled `GitHub Action`. The code for the action can be found in the `.github/workflows/uptime-check.yml` file within the root of the project folder. 

In `GitHub Actions` the alias of `python3` and `pip3` is replaced with: `python` and `pip`.

The script can be run locally from within the terminal:

```shell
$ LOCAL_LOOP=1 python3 index.py
```

The script will run in the terminal and send a `HEAD` request to the URLs listed. The response will be returned to check the `HTTP` or `HTTPS` status.