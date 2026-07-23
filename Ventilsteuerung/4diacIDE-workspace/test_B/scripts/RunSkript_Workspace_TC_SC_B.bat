::Script

@echo off & setlocal

del ..\Uebungen\const\UT\TC_SC\DefaultPool_TC_SC.gcf
del ..\Uebungen\const\UT\TC_SC\DefaultPool_TC_SC_Numeric.gcf
python ..\..\..\scripts_central\GcfScript.py --oldfile ISO-DesignerProjects\Workspace_TC_SC\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_B\Uebungen\const\UT\TC_SC\ --newfile DefaultPool_TC_SC --package Uebungen::const::UT::TC_SC --jopfile ISO-DesignerProjects\Workspace_TC_SC\DefaultPool\DefaultPool.jop
