@echo off
:loop
call activate webdev
python main.py
call deactivate
waitfor /T 3600 pause
goto loop