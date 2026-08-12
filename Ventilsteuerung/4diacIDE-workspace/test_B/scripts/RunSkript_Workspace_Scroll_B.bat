::Script

@echo off & setlocal

del ..\Uebungen\const\UT\Scroll\DefaultPool.gcf
del ..\Uebungen\const\UT\Scroll\DefaultPool_Numeric.gcf
del ..\Uebungen\const\UT\Scroll\DefaultPool_Scroll.gcf
python ..\..\..\scripts_central\GcfScript.py --oldfile ISO-DesignerProjects\Workspace_Scroll\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_B\Uebungen\const\UT\Scroll\ --newfile DefaultPool --package Uebungen::const::UT::Scroll --jopfile ISO-DesignerProjects\Workspace_Scroll\DefaultPool\DefaultPool.jop
