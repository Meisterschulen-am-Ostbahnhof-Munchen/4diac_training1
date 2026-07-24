::Script

@echo off & setlocal

del ..\Uebungen\const\UT\PWM\DefaultPool_PWM.gcf
del ..\Uebungen\const\UT\PWM\DefaultPool_PWM_Numeric.gcf
python ..\..\..\scripts_central\GcfScript.py --oldfile ISO-DesignerProjects\Workspace_PWM\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_AX\Uebungen\const\UT\PWM\ --newfile DefaultPool_PWM --package Uebungen::const::UT::PWM --jopfile ISO-DesignerProjects\Workspace_PWM\DefaultPool\DefaultPool.jop
