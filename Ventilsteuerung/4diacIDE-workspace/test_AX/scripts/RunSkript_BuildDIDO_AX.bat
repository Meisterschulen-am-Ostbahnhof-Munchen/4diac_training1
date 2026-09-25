::Script

@echo off & setlocal

cd /d "%~dp0"
python ..\..\..\scripts_central\compile_iso_designer_project.py --pool-dir ISO-DesignerProjects\Workspace_DIDO\DefaultPool
if errorlevel 1 exit /b 1
del ..\Uebungen\const\UT\DIDO\DefaultPool_DIDO.gcf
del ..\Uebungen\const\UT\DIDO\DefaultPool_DIDO_Numeric.gcf
python ..\..\..\scripts_central\GcfScript.py --oldfile ISO-DesignerProjects\Workspace_DIDO\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_AX\Uebungen\const\UT\DIDO\ --newfile DefaultPool_DIDO --package Uebungen::const::UT::DIDO --jopfile ISO-DesignerProjects\Workspace_DIDO\DefaultPool\DefaultPool.jop
if errorlevel 1 exit /b 1
python ..\..\..\scripts_central\list_mask_objects.py --pool-dir ISO-DesignerProjects\Workspace_DIDO\DefaultPool --emit-visibility ..\..\..\ISO-DesignerProjects\Workspace_DIDO\DefaultPool\Output\DefaultPool.vis.csv --emit-visibility-json ..\..\..\ISO-DesignerProjects\Workspace_DIDO\DefaultPool\Output\DefaultPool.vis.json
if errorlevel 1 exit /b 1
