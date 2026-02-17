import os

# Base paths
base_types_dir = "Ventilsteuerung/4diacIDE-workspace/.lib/adapter-3.0.0/typelib/types/unidirectional"
base_events_dir = "Ventilsteuerung/4diacIDE-workspace/.lib/adapter-3.0.0/typelib/events/unidirectional"

# Ensure base events dir exists
if not os.path.exists(base_events_dir):
    os.makedirs(base_events_dir)

# Template for .fbt file
fbt_template = """<?xml version="1.0" encoding="UTF-8"?>
<FBType Name="{fb_name}" Comment="{comment}">
	<Identification Standard="61499-2" Description="Copyright (c) 2025 HR Agrartechnik GmbH  &#10; &#10;This program and the accompanying materials are made  &#10;available under the terms of the Eclipse Public License 2.0  &#10;which is available at https://www.eclipse.org/legal/epl-2.0/  &#10; &#10;SPDX-License-Identifier: EPL-2.0">
	</Identification>
	<VersionInfo Organization="HR Agrartechnik GmbH" Version="1.0" Author="Franz Höpfinger" Date="2025-01-24">
	</VersionInfo>
	<CompilerInfo packageName="adapter::events::unidirectional">
		<Import declaration="eclipse4diac::core::GenericClassName"/>
		<Import declaration="eclipse4diac::core::TypeHash"/>
	</CompilerInfo>
	<InterfaceList>
		<Plugs>
{plugs}
		</Plugs>
		<Sockets>
			<AdapterDeclaration Name="IN" Type="{adapter_type}"/>
		</Sockets>
	</InterfaceList>
	<Attribute Name="eclipse4diac::core::GenericClassName" Value="'{generic_class_name}'"/>
	<Attribute Name="eclipse4diac::core::TypeHash" Value="''"/>
</FBType>
"""

# Walk through the types directory to find adapters
adapters = []
for root, dirs, files in os.walk(base_types_dir):
    for file in files:
        if file.endswith(".adp"):
            adapter_name = os.path.splitext(file)[0]
            subdir = os.path.relpath(root, base_types_dir)
            adapters.append((adapter_name, subdir))

print(f"Found {len(adapters)} adapters.")

# Generate split FBs
for adapter_name, subdir in adapters:
    target_dir = os.path.join(base_events_dir, subdir)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    adapter_type_full = f"adapter::types::unidirectional::{adapter_name}"

    for n in range(2, 10): # 2 to 9
        fb_name = f"{adapter_name}_SPLIT_{n}"
        comment = f"SPLIT 1 {adapter_name} into {n} {adapter_name} (generic FB)"
        generic_class_name = f"GEN_{adapter_name}_SPLIT"
        
        plugs_str = ""
        for i in range(1, n + 1):
            plugs_str += f'\t\t\t<AdapterDeclaration Name="OUT{i}" Type="{adapter_type_full}"/>\n'
        
        # Remove the last newline character
        plugs_str = plugs_str[:-1] if plugs_str else ""

        content = fbt_template.format(
            fb_name=fb_name,
            comment=comment,
            plugs=plugs_str,
            adapter_type=adapter_type_full,
            generic_class_name=generic_class_name
        )

        file_path = os.path.join(target_dir, f"{fb_name}.fbt")
        # Ensure directory exists for file (just in case)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        # print(f"Generated {file_path}") 

print("Done.")
