::Script

@echo off & setlocal

del ..\Uebungen\const\UT\Joystick\DefaultPool_Joystick.gcf
del ..\Uebungen\const\UT\Joystick\DefaultPool_Joystick_Numeric.gcf
python ..\..\..\scripts_central\GcfScript.py --oldfile ISO-DesignerProjects\Workspace_Joystick\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_AX\Uebungen\const\UT\Joystick\ --newfile DefaultPool_Joystick --package Uebungen::const::UT::Joystick --jopfile ISO-DesignerProjects\Workspace_Joystick\DefaultPool\DefaultPool.jop
