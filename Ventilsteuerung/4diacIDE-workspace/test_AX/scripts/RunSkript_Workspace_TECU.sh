#!/bin/bash

# Script to run GcfScript.py for Workspace_TECU on Linux

run_gcf() {
    python3 GcfScript.py "$@"
}

echo "Starting GcfScript processing for Workspace_TECU..."

# DefaultPool_TECU for test_AX
rm -f ../4diacIDE-workspace/test_AX/Uebungen/const/UT/TECU/DefaultPool_TECU.gcf
rm -f ../4diacIDE-workspace/test_AX/Uebungen/const/UT/TECU/DefaultPool_TECU_Numeric.gcf
run_gcf --oldfile ISO-DesignerProjects/Workspace_TECU/DefaultPool/Output/DefaultPool.iop.h --newfolder 4diacIDE-workspace/test_AX/Uebungen/const/UT/TECU/ --newfile DefaultPool_TECU --package Uebungen::const::UT::TECU --jopfile ISO-DesignerProjects/Workspace_TECU/DefaultPool/DefaultPool.jop

# DefaultPool_TECU for test_B
rm -f ../4diacIDE-workspace/test_B/Uebungen/const/UT/TECU/DefaultPool_TECU.gcf
rm -f ../4diacIDE-workspace/test_B/Uebungen/const/UT/TECU/DefaultPool_TECU_Numeric.gcf
run_gcf --oldfile ISO-DesignerProjects/Workspace_TECU/DefaultPool/Output/DefaultPool.iop.h --newfolder 4diacIDE-workspace/test_B/Uebungen/const/UT/TECU/ --newfile DefaultPool_TECU --package Uebungen::const::UT::TECU --jopfile ISO-DesignerProjects/Workspace_TECU/DefaultPool/DefaultPool.jop

echo "Processing finished."
