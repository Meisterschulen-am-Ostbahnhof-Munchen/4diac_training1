#!/bin/bash

# Script to run all GcfScript.py configurations on Linux

echo "Starting GcfScript processing..."

./RunSkript_Workspace_B.sh
./RunSkript_Workspace_PWM_B.sh
./RunSkript_Workspace_TECU_B.sh
./RunSkript_Workspace_Horse_B.sh
./RunSkript_Workspace_DIDO_B.sh
./RunSkript_Workspace_Joystick_B.sh
./RunSkript_Workspace_TC_SC_B.sh

echo "Processing finished."
