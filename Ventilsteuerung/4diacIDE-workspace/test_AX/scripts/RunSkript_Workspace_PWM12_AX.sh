#!/bin/bash
set -e

# Script to run GcfScript.py for Workspace_PWM12 on Linux

run_gcf() {
    python3 ../../../scripts_central/GcfScript.py "$@"
}

echo "Starting GcfScript processing for Workspace_PWM12..."

# DefaultPool_PWM12 for test_AX
rm -f ../Uebungen/const/UT/PWM12/DefaultPool_PWM12.gcf
rm -f ../Uebungen/const/UT/PWM12/DefaultPool_PWM12_Numeric.gcf
run_gcf --oldfile ISO-DesignerProjects/Workspace_PWM12/DefaultPool/Output/DefaultPool.iop.h --newfolder 4diacIDE-workspace/test_AX/Uebungen/const/UT/PWM12/ --newfile DefaultPool_PWM12 --package Uebungen::const::UT::PWM12 --jopfile ISO-DesignerProjects/Workspace_PWM12/DefaultPool/DefaultPool.jop

echo "Processing finished."
