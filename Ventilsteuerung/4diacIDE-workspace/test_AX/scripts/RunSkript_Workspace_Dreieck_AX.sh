#!/bin/bash
set -e

# Script to run GcfScript.py for Workspace_Dreieck on Linux

run_gcf() {
    python3 ../../../scripts_central/GcfScript.py "$@"
}

echo "Starting GcfScript processing for Workspace_Dreieck..."

# DefaultPool_Dreieck for test_AX
rm -f ../Uebungen/const/UT/Dreieck/DefaultPool_Dreieck.gcf
rm -f ../Uebungen/const/UT/Dreieck/DefaultPool_Dreieck_Numeric.gcf
run_gcf --oldfile ISO-DesignerProjects/Workspace_Dreieck/DefaultPool/Output/DefaultPool.iop.h --newfolder 4diacIDE-workspace/test_AX/Uebungen/const/UT/Dreieck/ --newfile DefaultPool_Dreieck --package Uebungen::const::UT::Dreieck --jopfile ISO-DesignerProjects/Workspace_Dreieck/DefaultPool/DefaultPool.jop

echo "Processing finished."
