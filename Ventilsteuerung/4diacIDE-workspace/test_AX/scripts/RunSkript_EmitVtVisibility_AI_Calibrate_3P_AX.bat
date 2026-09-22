::Script

@echo off & setlocal

python ..\..\..\scripts_central\list_mask_objects.py --pool-dir ISO-DesignerProjects\Workspace_AI_Calibrate_3P\DefaultPool --emit-visibility ..\..\..\ISO-DesignerProjects\Workspace_AI_Calibrate_3P\DefaultPool\Output\DefaultPool.vis.csv --emit-visibility-json ..\..\..\ISO-DesignerProjects\Workspace_AI_Calibrate_3P\DefaultPool\Output\DefaultPool.vis.json %*
