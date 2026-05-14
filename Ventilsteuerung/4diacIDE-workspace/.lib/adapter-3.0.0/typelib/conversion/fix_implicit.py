#!/usr/bin/env python3
"""
Script to remove unnecessary intermediate Convert FBs from adapter .fbt files.
A Convert FB is unnecessary if the source type can be implicitly assigned to the target type.
"""

import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path

# Mapping from adapter short names to IEC 61131-3 types
ADAPTER_TO_IEC = {
    'AX': 'BOOL',
    'AUS': 'USINT',
    'AS': 'SINT',
    'AUI': 'UINT',
    'AI': 'INT',
    'AUDI': 'UDINT',
    'ADI': 'DINT',
    'AULI': 'ULINT',
    'ALI': 'LINT',
    'AB': 'BYTE',
    'AW': 'WORD',
    'AD': 'DWORD',
    'AL': 'LWORD',
    'AR': 'REAL',
    'ALR': 'LREAL',
}

# Define implicit conversion rules
# Format: source_type -> set of allowed target types
IMPLICIT = {
    'BOOL': {'BOOL', 'BYTE', 'WORD', 'DWORD', 'LWORD'},
    'BYTE': {'BYTE', 'WORD', 'DWORD', 'LWORD'},
    'WORD': {'WORD', 'DWORD', 'LWORD'},
    'DWORD': {'DWORD', 'LWORD'},
    'LWORD': {'LWORD'},
    'SINT': {'SINT', 'INT', 'DINT', 'LINT', 'REAL', 'LREAL'},
    'INT': {'INT', 'DINT', 'LINT', 'REAL', 'LREAL'},
    'DINT': {'DINT', 'LINT', 'LREAL'},
    'LINT': {'LINT'},
    'USINT': {'USINT', 'UINT', 'UDINT', 'ULINT', 'REAL', 'LREAL'},
    'UINT': {'UINT', 'UDINT', 'ULINT', 'REAL', 'LREAL'},
    'UDINT': {'UDINT', 'ULINT', 'LREAL'},
    'ULINT': {'ULINT'},
    'REAL': {'REAL', 'LREAL'},
    'LREAL': {'LREAL'},
    'TIME': {'TIME', 'LTIME'},
    'LTIME': {'LTIME'},
    'DATE': {'DATE', 'LDATE'},
    'LDATE': {'LDATE'},
    'TOD': {'TOD', 'LTOD'},
    'LTOD': {'LTOD'},
    'DT': {'DT', 'LDT'},
    'LDT': {'LDT'},
}

def is_implicit_allowed(source, target):
    """Check if source can be implicitly assigned to target."""
    if source == target:
        return True
    return target in IMPLICIT.get(source, set())

def find_conversion_files(base_dir):
    """Find all .fbt files under base_dir."""
    return list(Path(base_dir).rglob('*.fbt'))

def process_file(filepath):
    """
    Process a single .fbt file.
    Returns True if file was modified, False otherwise.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse XML
    try:
        root = ET.fromstring(content)
    except ET.ParseError as e:
        print(f"  XML parse error in {filepath}: {e}")
        return False
    
    ns = {'': root.tag.split('}')[0].strip('{')} if '}' in root.tag else {}
    
    # Find FBNetwork
    fb_network = root.find('.//FBNetwork', ns)
    if fb_network is None:
        return False
    
    # Find all FB elements
    fbs = fb_network.findall('FB', ns)
    if len(fbs) != 1:
        # Only handle files with exactly one FB (the Convert)
        return False
    
    fb = fbs[0]
    fb_type = fb.get('Type', '')
    fb_name = fb.get('Name', '')
    
    if fb_name != 'Convert' or not fb_type.startswith('iec61131::conversion::F_'):
        return False
    
    # Extract conversion function name
    func_name = fb_type.split('::')[-1]  # e.g., F_INT_TO_LREAL
    match = re.match(r'F_(\w+)_TO_(\w+)', func_name)
    if not match:
        return False
    
    source_type = match.group(1)
    target_type = match.group(2)
    
    # Check if implicit conversion is allowed
    if not is_implicit_allowed(source_type, target_type):
        return False
    
    print(f"  Processing: {filepath.name} ({source_type} -> {target_type} is implicit)")
    
    # Now modify the XML content manually to preserve formatting
    # Remove the FB element
    fb_pattern = re.compile(
        r'\t\t<FB Name="Convert" Type="iec61131::conversion::F_[^"]+"[^/]*/>\n'
    )
    content = fb_pattern.sub('', content)
    
    # Also remove if it has a separate closing tag
    fb_pattern2 = re.compile(
        r'\t\t<FB Name="Convert" Type="iec61131::conversion::F_[^"]+"[^>]*>\n\t\t</FB>\n'
    )
    content = fb_pattern2.sub('', content)
    
    # Remove the Import declaration for the conversion function
    import_pattern = re.compile(
        r'\t\t<Import declaration="iec61131::conversion::' + re.escape(func_name) + r""""/>\n"""
    )
    content = import_pattern.sub('', content)
    
    # Simplify event connections: remove Convert.REQ and Convert.CNF intermediate
    # Pattern: Source="XXX.E1" Destination="Convert.REQ" ...
    #         Source="Convert.CNF" Destination="YYY.E1" ...
    # We need to find the actual source and destination adapter names
    event_connections = fb_network.find('EventConnections', ns)
    data_connections = fb_network.find('DataConnections', ns)
    
    source_socket = None
    target_plug = None
    
    # Find socket (input adapter) and plug (output adapter)
    interface_list = root.find('InterfaceList', ns)
    if interface_list is not None:
        sockets = interface_list.find('Sockets', ns)
        plugs = interface_list.find('Plugs', ns)
        if sockets is not None:
            socket_decl = sockets.find('AdapterDeclaration', ns)
            if socket_decl is not None:
                source_socket = socket_decl.get('Name')
        if plugs is not None:
            plug_decl = plugs.find('AdapterDeclaration', ns)
            if plug_decl is not None:
                target_plug = plug_decl.get('Name')
    
    if source_socket and target_plug:
        # Replace event connections going through Convert
        # Old: <Connection Source="AI_IN.E1" Destination="Convert.REQ" dx1="100"/>
        #      <Connection Source="Convert.CNF" Destination="ALR_OUT.E1" dx1="100"/>
        # New: <Connection Source="AI_IN.E1" Destination="ALR_OUT.E1"/>
        
        # Match the two connection lines and replace with direct connection
        event_repl = re.compile(
            r'(\t\t<EventConnections>\n)'
            r'\t\t\t<Connection Source="([^"]+)\.E1" Destination="Convert\.REQ"[^/]*/>\n'
            r'\t\t\t<Connection Source="Convert\.CNF" Destination="([^"]+)\.E1"[^/]*/>\n'
            r'(\t\t</EventConnections>)'
        )
        content = event_repl.sub(
            r'\1\t\t\t<Connection Source="\2.E1" Destination="\3.E1"/>\n\4',
            content
        )
        
        # Same for data connections
        data_repl = re.compile(
            r'(\t\t<DataConnections>\n)'
            r'\t\t\t<Connection Source="([^"]+)\.D1" Destination="Convert\.IN"[^/]*/>\n'
            r'\t\t\t<Connection Source="Convert\.OUT" Destination="([^"]+)\.D1"[^/]*/>\n'
            r'(\t\t</DataConnections>)'
        )
        content = data_repl.sub(
            r'\1\t\t\t<Connection Source="\2.D1" Destination="\3.D1"/>\n\4',
            content
        )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    base_dir = '/home/franz/git/proj_4d_headless/LOGIBUS_integration_datapanel/4diac_training1/Ventilsteuerung/4diacIDE-workspace/.lib/adapter-3.0.0/typelib/conversion'
    files = find_conversion_files(base_dir)
    print(f"Found {len(files)} .fbt files")
    
    modified = 0
    for filepath in files:
        if process_file(filepath):
            modified += 1
    
    print(f"\nModified {modified} files")

if __name__ == '__main__':
    main()
