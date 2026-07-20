::Script

@echo off & setlocal

del ..\4diacIDE-workspace\test_AX\Uebungen\const\UT\Joystick\DefaultPool_Joystick.gcf
del ..\4diacIDE-workspace\test_AX\Uebungen\const\UT\Joystick\DefaultPool_Joystick_Numeric.gcf
python GcfScript.py --oldfile ISO-DesignerProjects\Workspace_Joystick\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_AX\Uebungen\const\UT\Joystick\ --newfile DefaultPool_Joystick --package Uebungen::const::UT::Joystick --jopfile ISO-DesignerProjects\Workspace_Joystick\DefaultPool\DefaultPool.jop

del ..\4diacIDE-workspace\test_B\Uebungen\const\UT\Joystick\DefaultPool_Joystick.gcf
del ..\4diacIDE-workspace\test_B\Uebungen\const\UT\Joystick\DefaultPool_Joystick_Numeric.gcf
python GcfScript.py --oldfile ISO-DesignerProjects\Workspace_Joystick\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_B\Uebungen\const\UT\Joystick\ --newfile DefaultPool_Joystick --package Uebungen::const::UT::Joystick --jopfile ISO-DesignerProjects\Workspace_Joystick\DefaultPool\DefaultPool.jop
