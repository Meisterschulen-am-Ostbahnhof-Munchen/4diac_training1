#!/bin/bash

# Script to run GcfScript.py for Workspace_TC-SC on Linux

run_gcf() {
    python3 GcfScript.py "$@"
}

echo "Starting GcfScript processing for Workspace_TC-SC..."

# DefaultPool_TC-SC for test_AX
rm -f ../4diacIDE-workspace/test_AX/Uebungen/const/UT/TC-SC/DefaultPool_TC-SC.gcf
rm -f ../4diacIDE-workspace/test_AX/Uebungen/const/UT/TC-SC/DefaultPool_TC-SC_Numeric.gcf
run_gcf --oldfile ISO-DesignerProjects/Workspace_TC-SC/DefaultPool/Output/DefaultPool.iop.h --newfolder 4diacIDE-workspace/test_AX/Uebungen/const/UT/TC-SC/ --newfile DefaultPool_TC-SC --package Uebungen::const::UT::TC-SC --jopfile ISO-DesignerProjects/Workspace_TC-SC/DefaultPool/DefaultPool.jop

# DefaultPool_TC-SC for test_B
rm -f ../4diacIDE-workspace/test_B/Uebungen/const/UT/TC-SC/DefaultPool_TC-SC.gcf
rm -f ../4diacIDE-workspace/test_B/Uebungen/const/UT/TC-SC/DefaultPool_TC-SC_Numeric.gcf
run_gcf --oldfile ISO-DesignerProjects/Workspace_TC-SC/DefaultPool/Output/DefaultPool.iop.h --newfolder 4diacIDE-workspace/test_B/Uebungen/const/UT/TC-SC/ --newfile DefaultPool_TC-SC --package Uebungen::const::UT::TC-SC --jopfile ISO-DesignerProjects/Workspace_TC-SC/DefaultPool/DefaultPool.jop

echo "Processing finished."
