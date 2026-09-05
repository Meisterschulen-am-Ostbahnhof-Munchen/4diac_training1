::Script

@echo off & setlocal

del ..\Uebungen\const\UT\AI\DefaultPool_AI.gcf
del ..\Uebungen\const\UT\AI\DefaultPool_AI_Numeric.gcf
python ..\..\..\scripts_central\GcfScript.py --oldfile ISO-DesignerProjects\Workspace_AI\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_AX\Uebungen\const\UT\AI\ --newfile DefaultPool_AI --package Uebungen::const::UT::AI --jopfile ISO-DesignerProjects\Workspace_AI\DefaultPool\DefaultPool.jop
