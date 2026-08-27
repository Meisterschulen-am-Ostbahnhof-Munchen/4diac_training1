::Script

@echo off & setlocal

del ..\Uebungen\const\UT\DIDO\DefaultPool_DIDO.gcf
del ..\Uebungen\const\UT\DIDO\DefaultPool_DIDO_Numeric.gcf
python ..\..\..\scripts_central\GcfScript.py --oldfile ISO-DesignerProjects\Workspace_DIDO\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_AX\Uebungen\const\UT\DIDO\ --newfile DefaultPool_DIDO --package Uebungen::const::UT::DIDO --jopfile ISO-DesignerProjects\Workspace_DIDO\DefaultPool\DefaultPool.jop
