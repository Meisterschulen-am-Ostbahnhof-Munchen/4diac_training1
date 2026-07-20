#!/bin/bash

# Script to run GcfScript.py for Workspace on Linux

run_gcf() {
    python3 ../../../scripts_central/GcfScript.py "$@"
}

echo "Starting GcfScript processing for Workspace..."

# DefaultPool for test_B
rm -f ../Uebungen/const/UT/DefaultPool.gcf
rm -f ../Uebungen/const/UT/DefaultPool_Numeric.gcf
run_gcf --oldfile ISO-DesignerProjects/Workspace/DefaultPool/Output/DefaultPool.iop.h --newfolder 4diacIDE-workspace/test_B/Uebungen/const/UT/ --newfile DefaultPool --package Uebungen::const::UT --jopfile ISO-DesignerProjects/Workspace/DefaultPool/DefaultPool.jop

echo "Processing finished."
