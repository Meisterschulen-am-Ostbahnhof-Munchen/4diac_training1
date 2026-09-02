#!/bin/bash

# Script to run GcfScript.py for Workspace_AI_Calibrate on Linux

run_gcf() {
    python3 ../../../scripts_central/GcfScript.py "$@"
}

echo "Starting GcfScript processing for Workspace_AI_Calibrate..."

# DefaultPool_AIC for test_AX
rm -f ../Uebungen/const/UT/AIC/DefaultPool_AIC.gcf
run_gcf --oldfile ISO-DesignerProjects/Workspace_AI_Calibrate/DefaultPool/Output/DefaultPool.iop.h --newfolder 4diacIDE-workspace/test_AX/Uebungen/const/UT/AIC/ --newfile DefaultPool_AIC --package Uebungen::const::UT::AIC --jopfile ISO-DesignerProjects/Workspace_AI_Calibrate/DefaultPool/DefaultPool.jop

echo "Processing finished."
