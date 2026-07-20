::Script

@echo off & setlocal

del ..\4diacIDE-workspace\test_AX\Uebungen\const\UT\Tester\DefaultPool_Tester.gcf
del ..\4diacIDE-workspace\test_AX\Uebungen\const\UT\Tester\DefaultPool_Tester_Numeric.gcf
python GcfScript.py --oldfile ISO-DesignerProjects\Workspace_Tester\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_AX\Uebungen\const\UT\Tester\ --newfile DefaultPool_Tester --package Uebungen::const::UT::Tester --jopfile ISO-DesignerProjects\Workspace_Tester\DefaultPool\DefaultPool.jop

del ..\4diacIDE-workspace\test_B\Uebungen\const\UT\Tester\DefaultPool_Tester.gcf
del ..\4diacIDE-workspace\test_B\Uebungen\const\UT\Tester\DefaultPool_Tester_Numeric.gcf
python GcfScript.py --oldfile ISO-DesignerProjects\Workspace_Tester\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_B\Uebungen\const\UT\Tester\ --newfile DefaultPool_Tester --package Uebungen::const::UT::Tester --jopfile ISO-DesignerProjects\Workspace_Tester\DefaultPool\DefaultPool.jop
