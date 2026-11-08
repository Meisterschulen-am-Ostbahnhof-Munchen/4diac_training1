::Script

@echo off & setlocal

del ..\Uebungen\const\UT\DefaultPool.gcf
del ..\Uebungen\const\UT\DefaultPool_Numeric.gcf
python ..\..\..\scripts_central\GcfScript.py --oldfile ISO-DesignerProjects\Workspace\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_VV\Uebungen\const\UT\ --newfile DefaultPool --package Uebungen::const::UT --jopfile ISO-DesignerProjects\Workspace\DefaultPool\DefaultPool.jop
