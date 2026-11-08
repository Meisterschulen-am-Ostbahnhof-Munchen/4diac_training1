#!/bin/bash

# Script to run GcfScript.py for Workspace_PWM on Linux

run_gcf() {
    python3 ../../../scripts_central/GcfScript.py "$@"
}

echo "Starting GcfScript processing for Workspace_PWM..."

# DefaultPool_PWM for test_B
rm -f ../Uebungen/const/UT/PWM/DefaultPool_PWM.gcf
rm -f ../Uebungen/const/UT/PWM/DefaultPool_PWM_Numeric.gcf
run_gcf --oldfile ISO-DesignerProjects/Workspace_PWM/DefaultPool/Output/DefaultPool.iop.h --newfolder 4diacIDE-workspace/test_B/Uebungen/const/UT/PWM/ --newfile DefaultPool_PWM --package Uebungen::const::UT::PWM --jopfile ISO-DesignerProjects/Workspace_PWM/DefaultPool/DefaultPool.jop

echo "Processing finished."
