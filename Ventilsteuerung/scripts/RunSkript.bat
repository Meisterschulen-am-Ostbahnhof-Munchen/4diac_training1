::Script

@echo off & setlocal


set PATH="C:\Espressif\python_env\idf5.2_py3.11_env\Scripts"

del ..\4diacIDE-workspace\test\FBs\Ventilsteuerung\Workspace\DefaultPool.globalconsts

python GcfScript.py --oldfile ISO-DesignerProjects\Workspace\DefaultPool\Output\DefaultPool.iop.h --newfile 4diacIDE-workspace\test\FBs\Ventilsteuerung\Workspace\

del ..\4diacIDE-workspace\test\FBs\Ventilsteuerung\Workspace_TECU\DefaultPool.globalconsts

python GcfScript.py --oldfile ISO-DesignerProjects\Workspace_TECU\DefaultPool\Output\DefaultPool.iop.h --newfile 4diacIDE-workspace\test\FBs\Ventilsteuerung\Workspace_TECU\