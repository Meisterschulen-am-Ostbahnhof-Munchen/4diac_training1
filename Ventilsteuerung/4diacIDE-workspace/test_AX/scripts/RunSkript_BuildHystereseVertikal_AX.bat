::Script

@echo off & setlocal

cd /d "%~dp0"
python ..\..\..\scripts_central\compile_iso_designer_project.py --pool-dir ISO-DesignerProjects\Workspace_Hysterese_Vertikal\DefaultPool
if errorlevel 1 exit /b 1
del ..\Uebungen\const\UT\HystereseVertikal\DefaultPool.gcf
del ..\Uebungen\const\UT\HystereseVertikal\DefaultPool_Numeric.gcf
python ..\..\..\scripts_central\GcfScript.py --oldfile ISO-DesignerProjects\Workspace_Hysterese_Vertikal\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_AX\Uebungen\const\UT\HystereseVertikal\ --newfile DefaultPool --package Uebungen::const::UT::HystereseVertikal --jopfile ISO-DesignerProjects\Workspace_Hysterese_Vertikal\DefaultPool\DefaultPool.jop
if errorlevel 1 exit /b 1
python ..\..\..\scripts_central\list_mask_objects.py --pool-dir ISO-DesignerProjects\Workspace_Hysterese_Vertikal\DefaultPool --emit-visibility ..\..\..\ISO-DesignerProjects\Workspace_Hysterese_Vertikal\DefaultPool\Output\DefaultPool.vis.csv --emit-visibility-json ..\..\..\ISO-DesignerProjects\Workspace_Hysterese_Vertikal\DefaultPool\Output\DefaultPool.vis.json
if errorlevel 1 exit /b 1
