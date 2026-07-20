#!/bin/bash

# Script to run all GcfScript.py configurations on Linux

echo "Starting GcfScript processing..."

./RunSkript_Workspace.sh
./RunSkript_Workspace_PWM.sh
./RunSkript_Workspace_TECU.sh
./RunSkript_Workspace_Horse.sh
./RunSkript_Workspace_Tester.sh
./RunSkript_Workspace_Joystick.sh
./RunSkript_Workspace_TC_SC.sh"

echo "Processing finished."
