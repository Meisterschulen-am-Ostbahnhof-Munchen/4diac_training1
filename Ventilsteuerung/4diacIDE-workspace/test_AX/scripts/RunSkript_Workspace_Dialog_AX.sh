#!/bin/bash

# Script to run GcfScript.py for Workspace_Dialog on Linux

run_gcf() {
    python3 ../../../scripts_central/GcfScript.py "$@"
}

echo "Starting GcfScript processing for Workspace_Dialog..."

# DefaultPool for test_AX
rm -f ../Uebungen/const/UT/Dialog/DefaultPool.gcf
rm -f ../Uebungen/const/UT/Dialog/DefaultPool_Numeric.gcf
run_gcf --oldfile ISO-DesignerProjects/Workspace_Dialog/DefaultPool/Output/DefaultPool.iop.h --newfolder 4diacIDE-workspace/test_AX/Uebungen/const/UT/Dialog/ --newfile DefaultPool --package Uebungen::const::UT::Dialog --jopfile ISO-DesignerProjects/Workspace_Dialog/DefaultPool/DefaultPool.jop

echo "Processing finished."
