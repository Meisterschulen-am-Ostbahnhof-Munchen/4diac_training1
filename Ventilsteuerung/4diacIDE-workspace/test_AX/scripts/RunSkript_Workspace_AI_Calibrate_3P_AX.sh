#!/bin/bash

# Script to run GcfScript.py for Workspace_AI_Calibrate_3P on Linux

run_gcf() {
    python3 ../../../scripts_central/GcfScript.py "$@"
}

echo "Starting GcfScript processing for Workspace_AI_Calibrate_3P..."

# DefaultPool_AIC_3P for test_AX
rm -f ../Uebungen/const/UT/AIC/DefaultPool_AIC_3P.gcf
run_gcf --oldfile ISO-DesignerProjects/Workspace_AI_Calibrate_3P/DefaultPool/Output/DefaultPool.iop.h --newfolder 4diacIDE-workspace/test_AX/Uebungen/const/UT/AIC/ --newfile DefaultPool_AIC_3P --package Uebungen::const::UT::AIC --jopfile ISO-DesignerProjects/Workspace_AI_Calibrate_3P/DefaultPool/DefaultPool.jop

echo "Processing finished."
