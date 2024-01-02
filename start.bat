@echo off
cd /d "D:\work\pys\good-note-processor\"
call .\venv\Scripts\activate.bat
python -m flask --app .\app.py run --port=7826