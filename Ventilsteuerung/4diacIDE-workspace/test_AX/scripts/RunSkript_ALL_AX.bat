::Script

@echo off & setlocal

call RunSkript_Workspace_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_Workspace_PWM_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_Workspace_TECU_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_Workspace_Horse_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_Workspace_DIDO_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_Workspace_Joystick_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_Workspace_TC_SC_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_Workspace_Scroll_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_Workspace_PI_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_Workspace_AI_Calibrate_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_Workspace_AI_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_Workspace_PWM12_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_Workspace_Dreieck_AX.bat
if errorlevel 1 exit /b 1
