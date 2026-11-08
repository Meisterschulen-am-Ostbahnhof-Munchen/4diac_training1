#!/bin/bash
set -e

# Script to run GcfScript.py for Workspace_Dreieck on Linux

run_gcf() {
    python3 ../../../scripts_central/GcfScript.py "$@"
}

echo "Starting GcfScript processing for Workspace_Dreieck..."

# DefaultPool_Dreieck for test_B
rm -f ../Uebungen/const/UT/Dreieck/DefaultPool_Dreieck.gcf
rm -f ../Uebungen/const/UT/Dreieck/DefaultPool_Dreieck_Numeric.gcf
run_gcf --oldfile ISO-DesignerProjects/Workspace_Dreieck/DefaultPool/Output/DefaultPool.iop.h --newfolder 4diacIDE-workspace/test_B/Uebungen/const/UT/Dreieck/ --newfile DefaultPool_Dreieck --package Uebungen::const::UT::Dreieck --jopfile ISO-DesignerProjects/Workspace_Dreieck/DefaultPool/DefaultPool.jop
# DefaultPool_Dreieck_BargraphSplit.gcf and DefaultPool_Dreieck_PositionMarker.gcf are not managed by this script (same as test_AX) - keep in sync with test_AX manually.

echo "Processing finished."
