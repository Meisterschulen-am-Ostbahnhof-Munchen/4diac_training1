::Script

@echo off & setlocal

python ..\..\..\scripts_central\list_mask_objects.py --pool-dir ISO-DesignerProjects\Workspace_PI\DefaultPool --emit-visibility ..\..\..\ISO-DesignerProjects\Workspace_PI\DefaultPool\Output\DefaultPool.vis.csv --emit-visibility-json ..\..\..\ISO-DesignerProjects\Workspace_PI\DefaultPool\Output\DefaultPool.vis.json %*
