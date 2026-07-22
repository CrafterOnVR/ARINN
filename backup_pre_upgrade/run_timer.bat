@echo off
REM ARINN Autonomous Goal Timer
REM Runs the autonomous goal timer in a separate CMD window

echo Starting ARINN Autonomous Goal Timer...
echo.
echo This window will show a live countdown timer for autonomous goals.
echo Close this window to stop the timer.
echo.

python autonomous_timer.py

echo.
echo Timer stopped.
pause