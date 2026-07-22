@echo off  
REM ARINN Autonomous Goal Timer Launcher  
REM This runs the autonomous goal system independently  
  
echo ============================================  
echo  ARINN Autonomous Goal Timer  
echo  Running Independently of VS Code  
echo ============================================  
echo.  
  
REM Change to the ARINN directory  
cd /d "C:\Users\dmdra\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\research_agent"  
  
echo Starting ARINN autonomous goal system...  
echo Goals will be executed every 5 minutes  
echo Press Ctrl+C to stop  
echo.  
  
python autonomous_timer.py  
  
echo.  
echo Autonomous goal system stopped.  
pause 
