#!/bin/bash

# Script to run GcfScript.py for Workspace_Joystick on Linux

run_gcf() {
    python3 ../../../scripts_central/GcfScript.py "$@"
}

echo "Starting GcfScript processing for Workspace_Joystick..."

# DefaultPool_Joystick for test_B
rm -f ../Uebungen/const/UT/Joystick/DefaultPool_Joystick.gcf
rm -f ../Uebungen/const/UT/Joystick/DefaultPool_Joystick_Numeric.gcf
run_gcf --oldfile ISO-DesignerProjects/Workspace_Joystick/DefaultPool/Output/DefaultPool.iop.h --newfolder 4diacIDE-workspace/test_B/Uebungen/const/UT/Joystick/ --newfile DefaultPool_Joystick --package Uebungen::const::UT::Joystick --jopfile ISO-DesignerProjects/Workspace_Joystick/DefaultPool/DefaultPool.jop

echo "Processing finished."
