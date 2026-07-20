::Script

@echo off & setlocal

del ..\4diacIDE-workspace\test_AX\Uebungen\const\UT\TC_SC\DefaultPool_TC_SC.gcf
del ..\4diacIDE-workspace\test_AX\Uebungen\const\UT\TC_SC\DefaultPool_TC_SC_Numeric.gcf
python GcfScript.py --oldfile ISO-DesignerProjects\Workspace_TC-SC\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_AX\Uebungen\const\UT\TC_SC\ --newfile DefaultPool_TC_SC --package Uebungen::const::UT::TC_SC --jopfile ISO-DesignerProjects\Workspace_TC-SC\DefaultPool\DefaultPool.jop

del ..\4diacIDE-workspace\test_B\Uebungen\const\UT\TC_SC\DefaultPool_TC_SC.gcf
del ..\4diacIDE-workspace\test_B\Uebungen\const\UT\TC_SC\DefaultPool_TC_SC_Numeric.gcf
python GcfScript.py --oldfile ISO-DesignerProjects\Workspace_TC-SC\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_B\Uebungen\const\UT\TC_SC\ --newfile DefaultPool_TC_SC --package Uebungen::const::UT::TC_SC --jopfile ISO-DesignerProjects\Workspace_TC-SC\DefaultPool\DefaultPool.jop
