@echo off
REM ARINN Simple Web UI
REM Runs the clean Flask-based web interface for research

echo Starting ARINN Simple Web UI...
echo.
echo This will start the Flask web server for ARINN.
echo Main interface: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python simple_web_ui.py

echo.
echo Web UI stopped.
pause