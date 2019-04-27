@echo off
call conda activate webdev
:loop
python main.py
waitfor /T 3600 pause 2>nul
goto loop
call conda deactivate
