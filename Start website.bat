@echo off
REM Activate the virtual environment
call .venv\Scripts\activate

REM Run the Flask web server using .venv Python executable
python website.py

REM Deactivate the virtual environment
deactivate
