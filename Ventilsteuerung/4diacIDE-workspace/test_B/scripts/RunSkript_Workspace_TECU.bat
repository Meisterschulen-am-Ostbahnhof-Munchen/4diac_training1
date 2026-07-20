::Script

@echo off & setlocal

del ..\Uebungen\const\UT\TECU\DefaultPool_TECU.gcf
del ..\Uebungen\const\UT\TECU\DefaultPool_TECU_Numeric.gcf
python ..\..\..\scripts_central\GcfScript.py --oldfile ISO-DesignerProjects\Workspace_TECU\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_B\Uebungen\const\UT\TECU\ --newfile DefaultPool_TECU --package Uebungen::const::UT::TECU --jopfile ISO-DesignerProjects\Workspace_TECU\DefaultPool\DefaultPool.jop
