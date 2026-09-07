#!/bin/bash

# Script to run GcfScript.py for Workspace_PI on Linux

run_gcf() {
    python3 ../../../scripts_central/GcfScript.py "$@"
}

echo "Starting GcfScript processing for Workspace_PI..."

# DefaultPool_PI for test_AX
rm -f ../Uebungen/const/UT/PI/DefaultPool_PI.gcf
run_gcf --oldfile ISO-DesignerProjects/Workspace_PI/DefaultPool/Output/DefaultPool.iop.h --newfolder 4diacIDE-workspace/test_AX/Uebungen/const/UT/PI/ --newfile DefaultPool_PI --package Uebungen::const::UT::PI --jopfile ISO-DesignerProjects/Workspace_PI/DefaultPool/DefaultPool.jop

echo "Processing finished."
