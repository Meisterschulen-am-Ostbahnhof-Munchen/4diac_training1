#!/bin/bash

# Script to run GcfScript.py for Workspace_Scroll on Linux

run_gcf() {
    python3 ../../../scripts_central/GcfScript.py "$@"
}

echo "Starting GcfScript processing for Workspace_Scroll..."

# DefaultPool for test_B
rm -f ../Uebungen/const/UT/Scroll/DefaultPool.gcf
rm -f ../Uebungen/const/UT/Scroll/DefaultPool_Numeric.gcf
rm -f ../Uebungen/const/UT/Scroll/DefaultPool_Scroll.gcf
run_gcf --oldfile ISO-DesignerProjects/Workspace_Scroll/DefaultPool/Output/DefaultPool.iop.h --newfolder 4diacIDE-workspace/test_B/Uebungen/const/UT/Scroll/ --newfile DefaultPool --package Uebungen::const::UT::Scroll --jopfile ISO-DesignerProjects/Workspace_Scroll/DefaultPool/DefaultPool.jop

echo "Processing finished."
