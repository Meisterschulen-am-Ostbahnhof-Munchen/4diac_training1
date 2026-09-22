#!/bin/sh
# Script

python3 ../../../scripts_central/list_mask_objects.py --pool-dir ISO-DesignerProjects/Workspace_AI/DefaultPool --emit-visibility ../../../ISO-DesignerProjects/Workspace_AI/DefaultPool/Output/DefaultPool.vis.csv --emit-visibility-json ../../../ISO-DesignerProjects/Workspace_AI/DefaultPool/Output/DefaultPool.vis.json "$@"
