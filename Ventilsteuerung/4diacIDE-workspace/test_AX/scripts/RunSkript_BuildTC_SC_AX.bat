::Script

@echo off & setlocal

cd /d "%~dp0"
python ..\..\..\scripts_central\compile_iso_designer_project.py --pool-dir ISO-DesignerProjects\Workspace_TC_SC\DefaultPool
if errorlevel 1 exit /b 1
del ..\Uebungen\const\UT\TC_SC\DefaultPool_TC_SC.gcf
del ..\Uebungen\const\UT\TC_SC\DefaultPool_TC_SC_Numeric.gcf
python ..\..\..\scripts_central\GcfScript.py --oldfile ISO-DesignerProjects\Workspace_TC_SC\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_AX\Uebungen\const\UT\TC_SC\ --newfile DefaultPool_TC_SC --package Uebungen::const::UT::TC_SC --jopfile ISO-DesignerProjects\Workspace_TC_SC\DefaultPool\DefaultPool.jop
if errorlevel 1 exit /b 1
python ..\..\..\scripts_central\list_mask_objects.py --pool-dir ISO-DesignerProjects\Workspace_TC_SC\DefaultPool --emit-visibility ..\..\..\ISO-DesignerProjects\Workspace_TC_SC\DefaultPool\Output\DefaultPool.vis.csv --emit-visibility-json ..\..\..\ISO-DesignerProjects\Workspace_TC_SC\DefaultPool\Output\DefaultPool.vis.json
if errorlevel 1 exit /b 1
