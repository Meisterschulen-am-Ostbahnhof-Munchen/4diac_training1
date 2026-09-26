::Script

@echo off & setlocal

cd /d "%~dp0"
python ..\..\..\scripts_central\compile_iso_designer_project.py --pool-dir ISO-DesignerProjects\Workspace_AI_Calibrate_3P\DefaultPool
if errorlevel 1 exit /b 1
del ..\Uebungen\const\UT\AIC\DefaultPool_AIC_3P.gcf
python ..\..\..\scripts_central\GcfScript.py --oldfile ISO-DesignerProjects\Workspace_AI_Calibrate_3P\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_AX\Uebungen\const\UT\AIC\ --newfile DefaultPool_AIC_3P --package Uebungen::const::UT::AIC --jopfile ISO-DesignerProjects\Workspace_AI_Calibrate_3P\DefaultPool\DefaultPool.jop
if errorlevel 1 exit /b 1
python ..\..\..\scripts_central\list_mask_objects.py --pool-dir ISO-DesignerProjects\Workspace_AI_Calibrate_3P\DefaultPool --emit-visibility ..\..\..\ISO-DesignerProjects\Workspace_AI_Calibrate_3P\DefaultPool\Output\DefaultPool.vis.csv --emit-visibility-json ..\..\..\ISO-DesignerProjects\Workspace_AI_Calibrate_3P\DefaultPool\Output\DefaultPool.vis.json
if errorlevel 1 exit /b 1
