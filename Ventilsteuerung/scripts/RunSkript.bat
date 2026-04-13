::Script

@echo off & setlocal


del ..\4diacIDE-workspace\test_AX\Uebungen\const\UT\DefaultPool.gcf
python GcfScript.py --oldfile ISO-DesignerProjects\Workspace\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_AX\Uebungen\const\UT\ --newfile DefaultPool

del ..\4diacIDE-workspace\test_AX\Uebungen\const\UT\DefaultPool.gcf
python GcfScript.py --oldfile ISO-DesignerProjects\Workspace\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_AX\Uebungen\const\UT\Workspace\ --newfile DefaultPool

del ..\4diacIDE-workspace\test_AX\Uebungen\const\UT\TECU\DefaultPool_TECU.gcf
python GcfScript.py --oldfile ISO-DesignerProjects\Workspace_TECU\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_AX\Uebungen\const\UT\Workspace_TECU\ --newfile DefaultPool_TECU

del ..\4diacIDE-workspace\test_AX\Uebungen\const\UT\TECU\DefaultPool_TECU.gcf
python GcfScript.py --oldfile ISO-DesignerProjects\Workspace_TECU\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_AX\Uebungen\const\UT\Workspace_TECU\ --newfile DefaultPool_TECU

del ..\4diacIDE-workspace\test_AX\Uebungen\const\UT\PWM\DefaultPool_PWM.gcf
python GcfScript.py --oldfile ISO-DesignerProjects\Workspace_PWM\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_AX\Uebungen\const\UT\Workspace_PWM\ --newfile DefaultPool_PWM

del ..\4diacIDE-workspace\test_AX\Uebungen\const\UT\PWM\DefaultPool_PWM.gcf
python GcfScript.py --oldfile ISO-DesignerProjects\Workspace_PWM\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_AX\Uebungen\const\UT\Workspace_PWM\ --newfile DefaultPool_PWM