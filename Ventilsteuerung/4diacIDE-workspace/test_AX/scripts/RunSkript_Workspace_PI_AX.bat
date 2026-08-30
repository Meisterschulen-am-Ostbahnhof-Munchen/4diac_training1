::Script

@echo off & setlocal

del ..\Uebungen\const\UT\PI\DefaultPool_PI.gcf
python ..\..\..\scripts_central\GcfScript.py --oldfile ISO-DesignerProjects\Workspace_PI\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_AX\Uebungen\const\UT\PI\ --newfile DefaultPool_PI --package Uebungen::const::UT::PI --jopfile ISO-DesignerProjects\Workspace_PI\DefaultPool\DefaultPool.jop
