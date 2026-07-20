::Script

@echo off & setlocal

del ..\4diacIDE-workspace\test_AX\Uebungen\const\UT\TECU\DefaultPool_TECU.gcf
del ..\4diacIDE-workspace\test_AX\Uebungen\const\UT\TECU\DefaultPool_TECU_Numeric.gcf
python GcfScript.py --oldfile ISO-DesignerProjects\Workspace_TECU\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_AX\Uebungen\const\UT\TECU\ --newfile DefaultPool_TECU --package Uebungen::const::UT::TECU --jopfile ISO-DesignerProjects\Workspace_TECU\DefaultPool\DefaultPool.jop

del ..\4diacIDE-workspace\test_B\Uebungen\const\UT\TECU\DefaultPool_TECU.gcf
del ..\4diacIDE-workspace\test_B\Uebungen\const\UT\TECU\DefaultPool_TECU_Numeric.gcf
python GcfScript.py --oldfile ISO-DesignerProjects\Workspace_TECU\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_B\Uebungen\const\UT\TECU\ --newfile DefaultPool_TECU --package Uebungen::const::UT::TECU --jopfile ISO-DesignerProjects\Workspace_TECU\DefaultPool\DefaultPool.jop
