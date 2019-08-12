@echo off
:loop
call activate webdev
python main.py
call conda deactivate
timeout /t 86400 /nobreak
goto loop
