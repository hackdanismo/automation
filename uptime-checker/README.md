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