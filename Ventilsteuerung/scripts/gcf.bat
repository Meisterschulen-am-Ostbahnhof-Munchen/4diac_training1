



set PATH="C:\Espressif\python_env\idf5.1_py3.11_env\Scripts"

del ..\4diacIDE-workspace\test\FBs\Ventilsteuerung\DefaultPool.globalconsts

python GcfScript.py --oldfile 4diacIDE-workspace\4diac_training1_empty-main_Uebung2\Ventilsteuerung\ISO-DesignerProjects\Workspace\DefaultPool\Output --newfile 4diacIDE-workspace\4diac_training1_empty-main_Uebung2\Ventilsteuerung\4diacIDE-workspace\test\FBs\Ventilsteuerung
