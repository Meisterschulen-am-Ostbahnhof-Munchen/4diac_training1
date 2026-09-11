::Script

@echo off & setlocal

del ..\Uebungen\const\UT\AIC\DefaultPool_AIC_3P.gcf
python ..\..\..\scripts_central\GcfScript.py --oldfile ISO-DesignerProjects\Workspace_AI_Calibrate_3P\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_AX\Uebungen\const\UT\AIC\ --newfile DefaultPool_AIC_3P --package Uebungen::const::UT::AIC --jopfile ISO-DesignerProjects\Workspace_AI_Calibrate_3P\DefaultPool\DefaultPool.jop
