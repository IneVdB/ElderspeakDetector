@echo off
2>startup.log (
REM Check if .venv folder exists
if not exist .venv (
    REM Create .venv folder using Python 3.10
    py -3.10 -m venv .venv
)

REM Activate the virtual environment
call .venv\Scripts\activate

REM Update pip
python.exe -m pip install --upgrade pip


REM Install requirements using .venv Python executable
python.exe -m pip install -r requirements.txt

REM Install Whisper
REM python.exe -m pip install git+https://github.com/openai/whisper.git

REM install spacy model
python.exe -m spacy download nl_core_news_lg
)