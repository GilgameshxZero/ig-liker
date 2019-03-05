@echo off
:loop
git pull
call activate webdev
python main.py
call deactivate
waitfor /T 3600 pause 2>nul
goto loop