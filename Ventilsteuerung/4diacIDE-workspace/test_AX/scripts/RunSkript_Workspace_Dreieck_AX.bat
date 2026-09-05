::Script

@echo off & setlocal

del ..\Uebungen\const\UT\Dreieck\DefaultPool_Dreieck.gcf
del ..\Uebungen\const\UT\Dreieck\DefaultPool_Dreieck_Numeric.gcf
python ..\..\..\scripts_central\GcfScript.py --oldfile ISO-DesignerProjects\Workspace_Dreieck\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_AX\Uebungen\const\UT\Dreieck\ --newfile DefaultPool_Dreieck --package Uebungen::const::UT::Dreieck --jopfile ISO-DesignerProjects\Workspace_Dreieck\DefaultPool\DefaultPool.jop
