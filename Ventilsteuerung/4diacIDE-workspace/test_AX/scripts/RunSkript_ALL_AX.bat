::Script

@echo off & setlocal

call RunSkript_CompileWorkspace_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_Workspace_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_EmitVtVisibility_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_CompileWorkspace_PWM_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_Workspace_PWM_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_EmitVtVisibility_PWM_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_CompileWorkspace_TECU_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_Workspace_TECU_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_EmitVtVisibility_TECU_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_CompileWorkspace_Horse_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_Workspace_Horse_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_EmitVtVisibility_Horse_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_CompileWorkspace_DIDO_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_Workspace_DIDO_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_EmitVtVisibility_DIDO_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_CompileWorkspace_Joystick_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_Workspace_Joystick_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_EmitVtVisibility_Joystick_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_CompileWorkspace_TC_SC_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_Workspace_TC_SC_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_EmitVtVisibility_TC_SC_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_CompileWorkspace_Scroll_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_Workspace_Scroll_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_EmitVtVisibility_Scroll_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_CompileWorkspace_PI_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_Workspace_PI_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_EmitVtVisibility_PI_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_CompileWorkspace_AI_Calibrate_2P_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_Workspace_AI_Calibrate_2P_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_EmitVtVisibility_AI_Calibrate_2P_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_CompileWorkspace_AI_Calibrate_3P_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_Workspace_AI_Calibrate_3P_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_EmitVtVisibility_AI_Calibrate_3P_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_CompileWorkspace_AI_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_Workspace_AI_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_EmitVtVisibility_AI_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_CompileWorkspace_PWM12_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_Workspace_PWM12_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_EmitVtVisibility_PWM12_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_CompileWorkspace_Dreieck_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_Workspace_Dreieck_AX.bat
if errorlevel 1 exit /b 1
call RunSkript_EmitVtVisibility_Dreieck_AX.bat
if errorlevel 1 exit /b 1
