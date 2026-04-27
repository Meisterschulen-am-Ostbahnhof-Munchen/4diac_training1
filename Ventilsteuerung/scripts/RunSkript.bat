::Script

@echo off & setlocal


del ..\4diacIDE-workspace\test_AX\Uebungen\const\UT\DefaultPool.gcf
del ..\4diacIDE-workspace\test_AX\Uebungen\const\UT\DefaultPool_Numeric.gcf
python GcfScript.py --oldfile ISO-DesignerProjects\Workspace\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_AX\Uebungen\const\UT\ --newfile DefaultPool --package Uebungen::const::UT --jopfile ISO-DesignerProjects\Workspace\DefaultPool\DefaultPool.jop

del ..\4diacIDE-workspace\test_B\Uebungen\const\UT\DefaultPool.gcf
del ..\4diacIDE-workspace\test_B\Uebungen\const\UT\DefaultPool_Numeric.gcf
python GcfScript.py --oldfile ISO-DesignerProjects\Workspace\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_B\Uebungen\const\UT\ --newfile DefaultPool --package Uebungen::const::UT --jopfile ISO-DesignerProjects\Workspace\DefaultPool\DefaultPool.jop
