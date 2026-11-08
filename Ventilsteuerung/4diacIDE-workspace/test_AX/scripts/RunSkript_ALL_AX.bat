::Script

@echo off & setlocal

cd /d "%~dp0"

call RunSkript_BuildAX.bat
if errorlevel 1 exit /b 1
call RunSkript_BuildPWM_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_BuildTECU_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_BuildHorse_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_BuildDIDO_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_BuildJoystick_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_BuildTC_SC_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_BuildScroll_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_BuildPI_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_BuildAI_Calibrate_2P_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_BuildAI_Calibrate_3P_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_BuildAI_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_BuildPWM12_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_BuildDreieck_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_BuildHystereseHorizontal_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_BuildHystereseVertikal_AX.bat
if errorlevel 1 exit /b 1
