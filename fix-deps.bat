@echo off
@setlocal enableextensions enabledelayedexpansion
powershell.exe -command ".\fixsrc.ps1"
cd .\requestssrc\requests-2.25.1
py setup.py install
pause