::Script

@echo off & setlocal

del ..\Uebungen\const\UT\PWM12\DefaultPool_PWM12.gcf
del ..\Uebungen\const\UT\PWM12\DefaultPool_PWM12_Numeric.gcf
python ..\..\..\scripts_central\GcfScript.py --oldfile ISO-DesignerProjects\Workspace_PWM12\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_AX\Uebungen\const\UT\PWM12\ --newfile DefaultPool_PWM12 --package Uebungen::const::UT::PWM12 --jopfile ISO-DesignerProjects\Workspace_PWM12\DefaultPool\DefaultPool.jop
