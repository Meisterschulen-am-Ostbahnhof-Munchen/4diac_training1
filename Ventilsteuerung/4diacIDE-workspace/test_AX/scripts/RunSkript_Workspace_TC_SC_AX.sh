#!/bin/bash

# Script to run GcfScript.py for Workspace_TC_SC on Linux

run_gcf() {
    python3 ../../../scripts_central/GcfScript.py "$@"
}

echo "Starting GcfScript processing for Workspace_TC_SC..."

# DefaultPool_TC_SC for test_AX
rm -f ../Uebungen/const/UT/TC_SC/DefaultPool_TC_SC.gcf
rm -f ../Uebungen/const/UT/TC_SC/DefaultPool_TC_SC_Numeric.gcf
run_gcf --oldfile ISO-DesignerProjects/Workspace_TC_SC/DefaultPool/Output/DefaultPool.iop.h --newfolder 4diacIDE-workspace/test_AX/Uebungen/const/UT/TC_SC/ --newfile DefaultPool_TC_SC --package Uebungen::const::UT::TC_SC --jopfile ISO-DesignerProjects/Workspace_TC_SC/DefaultPool/DefaultPool.jop

echo "Processing finished."
