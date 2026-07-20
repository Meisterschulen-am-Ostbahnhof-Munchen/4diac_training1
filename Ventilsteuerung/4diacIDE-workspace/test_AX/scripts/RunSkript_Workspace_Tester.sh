#!/bin/bash

# Script to run GcfScript.py for Workspace_Tester on Linux

run_gcf() {
    python3 GcfScript.py "$@"
}

echo "Starting GcfScript processing for Workspace_Tester..."

# DefaultPool_Tester for test_AX
rm -f ../4diacIDE-workspace/test_AX/Uebungen/const/UT/Tester/DefaultPool_Tester.gcf
rm -f ../4diacIDE-workspace/test_AX/Uebungen/const/UT/Tester/DefaultPool_Tester_Numeric.gcf
run_gcf --oldfile ISO-DesignerProjects/Workspace_Tester/DefaultPool/Output/DefaultPool.iop.h --newfolder 4diacIDE-workspace/test_AX/Uebungen/const/UT/Tester/ --newfile DefaultPool_Tester --package Uebungen::const::UT::Tester --jopfile ISO-DesignerProjects/Workspace_Tester/DefaultPool/DefaultPool.jop

# DefaultPool_Tester for test_B
rm -f ../4diacIDE-workspace/test_B/Uebungen/const/UT/Tester/DefaultPool_Tester.gcf
rm -f ../4diacIDE-workspace/test_B/Uebungen/const/UT/Tester/DefaultPool_Tester_Numeric.gcf
run_gcf --oldfile ISO-DesignerProjects/Workspace_Tester/DefaultPool/Output/DefaultPool.iop.h --newfolder 4diacIDE-workspace/test_B/Uebungen/const/UT/Tester/ --newfile DefaultPool_Tester --package Uebungen::const::UT::Tester --jopfile ISO-DesignerProjects/Workspace_Tester/DefaultPool/DefaultPool.jop

echo "Processing finished."
