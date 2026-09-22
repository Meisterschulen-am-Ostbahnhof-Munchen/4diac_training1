#!/bin/sh
# Script

python3 ../../../scripts_central/list_mask_objects.py --pool-dir ISO-DesignerProjects/Workspace/DefaultPool --emit-visibility ../../../ISO-DesignerProjects/Workspace/DefaultPool/Output/DefaultPool.vis.csv --emit-visibility-json ../../../ISO-DesignerProjects/Workspace/DefaultPool/Output/DefaultPool.vis.json "$@"
