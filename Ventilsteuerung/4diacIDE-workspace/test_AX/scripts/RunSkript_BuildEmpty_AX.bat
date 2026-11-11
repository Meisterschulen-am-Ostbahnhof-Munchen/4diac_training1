::Script

@echo off & setlocal

cd /d "%~dp0"
python ..\..\..\scripts_central\compile_iso_designer_project.py --pool-dir ISO-DesignerProjects\Workspace_Empty\DefaultPool
if errorlevel 1 exit /b 1
del ..\Uebungen\const\UT\Empty\DefaultPool_Empty.gcf
del ..\Uebungen\const\UT\Empty\DefaultPool_Empty_Numeric.gcf
python ..\..\..\scripts_central\GcfScript.py --oldfile ISO-DesignerProjects\Workspace_Empty\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_AX\Uebungen\const\UT\Empty\ --newfile DefaultPool_Empty --package Uebungen::const::UT::Empty --jopfile ISO-DesignerProjects\Workspace_Empty\DefaultPool\DefaultPool.jop
if errorlevel 1 exit /b 1
python ..\..\..\scripts_central\list_mask_objects.py --pool-dir ISO-DesignerProjects\Workspace_Empty\DefaultPool --emit-visibility ..\..\..\ISO-DesignerProjects\Workspace_Empty\DefaultPool\Output\DefaultPool.vis.csv --emit-visibility-json ..\..\..\ISO-DesignerProjects\Workspace_Empty\DefaultPool\Output\DefaultPool.vis.json
if errorlevel 1 exit /b 1
