# fastAttendix
sign your attendance 40 microseconds quicker.<sub><sub>heh.</sub></sub> powered by HTTP forgery. </br>aims to do away with that other browser tab- is a alternative frontend for the attendance system. </br></br>doubles as a proof-of-concept of header construction.

## Usage
run init.cmd. you will need to provide your login credentials on first use. </br>this should be able to work on preinstalled libraries. 

## Deps
\> stdlib: json, datetime </br>
\> *requests*

### Notice
there is no known limit on how many "invalid" otp inputs get accepted by the server.</br>
in this regard serverside throttling is entirely at the discretion of the backend </br></br>
on versions older than Python 3.9.1, a dependency might be missing. </br>
should the main program fail to run, run fix-deps.cmd AS ADMINISTRATOR to repair dependencies. </br>you might also need to run `set-executionpolicy unrestricted` in powershell.</br></br>
alternatively, just run `pip install requests`

known issue(s): </br>
occassional lockup/connection errors on start (cause untraceable- likely serverside). attempt to rectify by restarting script</br>
**DO NOT** spam/restart the script too much or youll be throttled

###### tested for Python 3.9.1.
