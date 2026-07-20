::Script

@echo off & setlocal

del ..\Uebungen\const\UT\Horse\DefaultPool_Horse.gcf
del ..\Uebungen\const\UT\Horse\DefaultPool_Horse_Numeric.gcf
python ..\..\..\scripts_central\GcfScript.py --oldfile ISO-DesignerProjects\Workspace_Horse\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_AX\Uebungen\const\UT\Horse\ --newfile DefaultPool_Horse --package Uebungen::const::UT::Horse --jopfile ISO-DesignerProjects\Workspace_Horse\DefaultPool\DefaultPool.jop
