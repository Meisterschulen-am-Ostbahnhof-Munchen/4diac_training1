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

# DefaultPool_PWM for test_AX
rm -f ../4diacIDE-workspace/test_AX/Uebungen/const/UT/PWM/DefaultPool_PWM.gcf
rm -f ../4diacIDE-workspace/test_AX/Uebungen/const/UT/PWM/DefaultPool_PWM_Numeric.gcf
run_gcf --oldfile ISO-DesignerProjects/Workspace_PWM/DefaultPool/Output/DefaultPool.iop.h --newfolder 4diacIDE-workspace/test_AX/Uebungen/const/UT/PWM/ --newfile DefaultPool_PWM --package Uebungen::const::UT::PWM --jopfile ISO-DesignerProjects/Workspace_PWM/DefaultPool/DefaultPool.jop

# DefaultPool_PWM for test_B
rm -f ../4diacIDE-workspace/test_B/Uebungen/const/UT/PWM/DefaultPool_PWM.gcf
rm -f ../4diacIDE-workspace/test_B/Uebungen/const/UT/PWM/DefaultPool_PWM_Numeric.gcf
run_gcf --oldfile ISO-DesignerProjects/Workspace_PWM/DefaultPool/Output/DefaultPool.iop.h --newfolder 4diacIDE-workspace/test_B/Uebungen/const/UT/PWM/ --newfile DefaultPool_PWM --package Uebungen::const::UT::PWM --jopfile ISO-DesignerProjects/Workspace_PWM/DefaultPool/DefaultPool.jop

# DefaultPool_TECU for test_AX
rm -f ../4diacIDE-workspace/test_AX/Uebungen/const/UT/TECU/DefaultPool_TECU.gcf
rm -f ../4diacIDE-workspace/test_AX/Uebungen/const/UT/TECU/DefaultPool_TECU_Numeric.gcf
run_gcf --oldfile ISO-DesignerProjects/Workspace_TECU/DefaultPool/Output/DefaultPool.iop.h --newfolder 4diacIDE-workspace/test_AX/Uebungen/const/UT/TECU/ --newfile DefaultPool_TECU --package Uebungen::const::UT::TECU --jopfile ISO-DesignerProjects/Workspace_TECU/DefaultPool/DefaultPool.jop

# DefaultPool_TECU for test_B
rm -f ../4diacIDE-workspace/test_B/Uebungen/const/UT/TECU/DefaultPool_TECU.gcf
rm -f ../4diacIDE-workspace/test_B/Uebungen/const/UT/TECU/DefaultPool_TECU_Numeric.gcf
run_gcf --oldfile ISO-DesignerProjects/Workspace_TECU/DefaultPool/Output/DefaultPool.iop.h --newfolder 4diacIDE-workspace/test_B/Uebungen/const/UT/TECU/ --newfile DefaultPool_TECU --package Uebungen::const::UT::TECU --jopfile ISO-DesignerProjects/Workspace_TECU/DefaultPool/DefaultPool.jop

echo "Processing finished."
