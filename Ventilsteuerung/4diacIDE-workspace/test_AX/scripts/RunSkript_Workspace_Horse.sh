#!/bin/bash

# Script to run GcfScript.py for Workspace_Horse on Linux

run_gcf() {
    python3 GcfScript.py "$@"
}

echo "Starting GcfScript processing for Workspace_Horse..."

# DefaultPool_Horse for test_AX
rm -f ../4diacIDE-workspace/test_AX/Uebungen/const/UT/Horse/DefaultPool_Horse.gcf
rm -f ../4diacIDE-workspace/test_AX/Uebungen/const/UT/Horse/DefaultPool_Horse_Numeric.gcf
run_gcf --oldfile ISO-DesignerProjects/Workspace_Horse/DefaultPool/Output/DefaultPool.iop.h --newfolder 4diacIDE-workspace/test_AX/Uebungen/const/UT/Horse/ --newfile DefaultPool_Horse --package Uebungen::const::UT::Horse --jopfile ISO-DesignerProjects/Workspace_Horse/DefaultPool/DefaultPool.jop

# DefaultPool_Horse for test_B
rm -f ../4diacIDE-workspace/test_B/Uebungen/const/UT/Horse/DefaultPool_Horse.gcf
rm -f ../4diacIDE-workspace/test_B/Uebungen/const/UT/Horse/DefaultPool_Horse_Numeric.gcf
run_gcf --oldfile ISO-DesignerProjects/Workspace_Horse/DefaultPool/Output/DefaultPool.iop.h --newfolder 4diacIDE-workspace/test_B/Uebungen/const/UT/Horse/ --newfile DefaultPool_Horse --package Uebungen::const::UT::Horse --jopfile ISO-DesignerProjects/Workspace_Horse/DefaultPool/DefaultPool.jop

echo "Processing finished."
