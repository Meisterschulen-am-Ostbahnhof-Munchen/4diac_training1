#!/bin/bash

# Script to run GcfScript.py for multiple configurations on Linux

# Function to run the python script with forward slashes
run_gcf() {
    python3 GcfScript.py "$@"
}

echo "Starting GcfScript processing..."

# DefaultPool for test_AX
rm -f ../4diacIDE-workspace/test_AX/Uebungen/const/UT/DefaultPool.gcf
rm -f ../4diacIDE-workspace/test_AX/Uebungen/const/UT/DefaultPool_Numeric.gcf
run_gcf --oldfile ISO-DesignerProjects/Workspace/DefaultPool/Output/DefaultPool.iop.h --newfolder 4diacIDE-workspace/test_AX/Uebungen/const/UT/ --newfile DefaultPool --package Uebungen::const::UT --jopfile ISO-DesignerProjects/Workspace/DefaultPool/DefaultPool.jop

# DefaultPool for test_B
rm -f ../4diacIDE-workspace/test_B/Uebungen/const/UT/DefaultPool.gcf
rm -f ../4diacIDE-workspace/test_B/Uebungen/const/UT/DefaultPool_Numeric.gcf
run_gcf --oldfile ISO-DesignerProjects/Workspace/DefaultPool/Output/DefaultPool.iop.h --newfolder 4diacIDE-workspace/test_B/Uebungen/const/UT/ --newfile DefaultPool --package Uebungen::const::UT --jopfile ISO-DesignerProjects/Workspace/DefaultPool/DefaultPool.jop



echo "Processing finished."
