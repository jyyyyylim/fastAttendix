@echo off
@setlocal enableextensions enabledelayedexpansion
set "ver=1.0.1"
color a & title instAttendix v%ver% by JY
py attendance.py

timeout 5
