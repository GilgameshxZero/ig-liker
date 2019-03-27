@echo off
:loop
git pull
call conda activate webdev
python main.py
call conda deactivate
waitfor /T 3600 pause 2>nul
goto loop
