#!/bin/bash

# Script to run GcfScript.py for Workspace_Empty on Linux

run_gcf() {
    python3 ../../../scripts_central/GcfScript.py "$@"
}

echo "Starting GcfScript processing for Workspace_Empty..."

# DefaultPool_Empty for test_AX
rm -f ../Uebungen/const/UT/Empty/DefaultPool_Empty.gcf
rm -f ../Uebungen/const/UT/Empty/DefaultPool_Empty_Numeric.gcf
run_gcf --oldfile ISO-DesignerProjects/Workspace_Empty/DefaultPool/Output/DefaultPool.iop.h --newfolder 4diacIDE-workspace/test_AX/Uebungen/const/UT/Empty/ --newfile DefaultPool_Empty --package Uebungen::const::UT::Empty --jopfile ISO-DesignerProjects/Workspace_Empty/DefaultPool/DefaultPool.jop

echo "Processing finished."
