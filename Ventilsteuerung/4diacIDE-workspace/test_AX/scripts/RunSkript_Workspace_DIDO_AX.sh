#!/bin/bash

# Script to run GcfScript.py for Workspace_DIDO on Linux

run_gcf() {
    python3 ../../../scripts_central/GcfScript.py "$@"
}

echo "Starting GcfScript processing for Workspace_DIDO..."

# DefaultPool_DIDO for test_AX
rm -f ../Uebungen/const/UT/DIDO/DefaultPool_DIDO.gcf
rm -f ../Uebungen/const/UT/DIDO/DefaultPool_DIDO_Numeric.gcf
run_gcf --oldfile ISO-DesignerProjects/Workspace_DIDO/DefaultPool/Output/DefaultPool.iop.h --newfolder 4diacIDE-workspace/test_AX/Uebungen/const/UT/DIDO/ --newfile DefaultPool_DIDO --package Uebungen::const::UT::DIDO --jopfile ISO-DesignerProjects/Workspace_DIDO/DefaultPool/DefaultPool.jop

echo "Processing finished."
