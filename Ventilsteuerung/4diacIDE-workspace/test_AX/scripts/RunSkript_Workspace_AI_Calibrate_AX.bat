::Script

@echo off & setlocal

del ..\Uebungen\const\UT\AIC\DefaultPool_AIC.gcf
python ..\..\..\scripts_central\GcfScript.py --oldfile ISO-DesignerProjects\Workspace_AI_Calibrate\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_AX\Uebungen\const\UT\AIC\ --newfile DefaultPool_AIC --package Uebungen::const::UT::AIC --jopfile ISO-DesignerProjects\Workspace_AI_Calibrate\DefaultPool\DefaultPool.jop
