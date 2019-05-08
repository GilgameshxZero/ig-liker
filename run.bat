@echo off
call activate webdev
:loop
python main.py
timeout /t 3600 /nobreak
goto loop
