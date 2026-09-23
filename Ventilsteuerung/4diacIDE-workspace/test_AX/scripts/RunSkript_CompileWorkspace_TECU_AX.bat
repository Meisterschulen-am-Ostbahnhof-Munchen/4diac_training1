::Script

@echo off ^& setlocal

cd /d "%~dp0"
python ..\..\..\scripts_central\compile_iso_designer_project.py --pool-dir ISO-DesignerProjects\Workspace_TECU\DefaultPool
if errorlevel 1 exit /b 1
