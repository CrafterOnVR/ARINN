@echo off
REM Super Enhanced Research Agent - Run GUI as Administrator
REM This batch file runs the research agent GUI with administrator privileges

echo ===========================================
echo  Super Enhanced Research Agent
echo  Running GUI as Administrator
echo ===========================================
echo.

REM Get the directory where this batch file is located
set "BATCH_DIR=%~dp0"
set "BATCH_DIR=%BATCH_DIR:~0,-1%"

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running with administrator privileges...
    goto :run_gui
) else (
    echo Requesting administrator privileges...
    goto :request_admin
)

:run_gui
echo Starting Super Enhanced Research Agent GUI...
cd /d "%BATCH_DIR%"
python run_desktop_gui.py
goto :end

:request_admin
REM Create a temporary script to run with admin privileges
echo cd /d "%BATCH_DIR%"> "%TEMP%\run_gui_admin_temp.cmd"
echo python run_desktop_gui.py>> "%TEMP%\run_gui_admin_temp.cmd"

REM Run the temporary script as administrator
powershell -Command "Start-Process 'cmd.exe' -ArgumentList '/c ""%TEMP%\run_gui_admin_temp.cmd""' -Verb RunAs -Wait"

REM Clean up
del "%TEMP%\run_gui_admin_temp.cmd" 2>nul
goto :end

:end
echo.
echo GUI session ended.
pause