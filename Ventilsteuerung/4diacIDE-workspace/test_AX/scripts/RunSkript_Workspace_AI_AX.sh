#!/bin/bash
set -e

# Script to run GcfScript.py for Workspace_AI on Linux

run_gcf() {
    python3 ../../../scripts_central/GcfScript.py "$@"
}

echo "Starting GcfScript processing for Workspace_AI..."

# DefaultPool_AI for test_AX
rm -f ../Uebungen/const/UT/AI/DefaultPool_AI.gcf
rm -f ../Uebungen/const/UT/AI/DefaultPool_AI_Numeric.gcf
run_gcf --oldfile ISO-DesignerProjects/Workspace_AI/DefaultPool/Output/DefaultPool.iop.h --newfolder 4diacIDE-workspace/test_AX/Uebungen/const/UT/AI/ --newfile DefaultPool_AI --package Uebungen::const::UT::AI --jopfile ISO-DesignerProjects/Workspace_AI/DefaultPool/DefaultPool.jop

echo "Processing finished."
