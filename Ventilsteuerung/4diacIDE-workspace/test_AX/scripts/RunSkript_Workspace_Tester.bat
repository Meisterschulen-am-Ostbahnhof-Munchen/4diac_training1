::Script

@echo off & setlocal

del ..\Uebungen\const\UT\Tester\DefaultPool_Tester.gcf
del ..\Uebungen\const\UT\Tester\DefaultPool_Tester_Numeric.gcf
python ..\..\..\scripts_central\GcfScript.py --oldfile ISO-DesignerProjects\Workspace_Tester\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_AX\Uebungen\const\UT\Tester\ --newfile DefaultPool_Tester --package Uebungen::const::UT::Tester --jopfile ISO-DesignerProjects\Workspace_Tester\DefaultPool\DefaultPool.jop
