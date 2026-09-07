::Script

@echo off & setlocal

del ..\Uebungen\const\UT\Dreieck\DefaultPool_Dreieck.gcf
del ..\Uebungen\const\UT\Dreieck\DefaultPool_Dreieck_Numeric.gcf
python ..\..\..\scripts_central\GcfScript.py --oldfile ISO-DesignerProjects\Workspace_Dreieck\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test_B\Uebungen\const\UT\Dreieck\ --newfile DefaultPool_Dreieck --package Uebungen::const::UT::Dreieck --jopfile ISO-DesignerProjects\Workspace_Dreieck\DefaultPool\DefaultPool.jop
:: DefaultPool_Dreieck_BargraphSplit.gcf und DefaultPool_Dreieck_PositionMarker.gcf werden von diesem Skript nicht verwaltet (wie in test_AX) - manuell mit test_AX synchron halten.
