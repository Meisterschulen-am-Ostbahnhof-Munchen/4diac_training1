#!/bin/bash

# Script to run all GcfScript.py configurations on Linux

echo "Starting GcfScript processing..."

./RunSkript_Workspace_AX.sh
./RunSkript_Workspace_PWM_AX.sh
./RunSkript_Workspace_TECU_AX.sh
./RunSkript_Workspace_Horse_AX.sh
./RunSkript_Workspace_DIDO_AX.sh
./RunSkript_Workspace_Joystick_AX.sh
./RunSkript_Workspace_TC_SC_AX.sh
./RunSkript_Workspace_PI_AX.sh
./RunSkript_Workspace_AI_Calibrate_AX.sh

echo "Processing finished."
