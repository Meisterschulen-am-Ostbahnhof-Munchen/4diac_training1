from argparse import ArgumentParser
import os
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom

def getPaths():
    script_path = os.path.dirname(os.path.abspath(__file__))
    parser = ArgumentParser()
    parser.add_argument("-o", "--oldfile", dest="old_file", required=True)
    parser.add_argument("-n", "--newfile", dest="new_file", required=True)
    parser.add_argument("-p", "--newfolder", dest="new_folder", required=True)
    parser.add_argument("-k", "--package", dest="package", required=True)
    parser.add_argument("-j", "--jopfile", dest="jop_file", required=False, default=None)
    args = parser.parse_args()

    # Create the absolute paths using os.path.join
    new_path = os.path.join(os.path.dirname(script_path), args.new_folder)
    old_path = os.path.join(os.path.dirname(script_path), args.old_file)
    jop_path = os.path.join(os.path.dirname(script_path), args.jop_file) if args.jop_file else None

    filepaths = [old_path, new_path, args.new_file, args.package, jop_path]
    return filepaths

def printPaths(filepaths):
    print('')
    print('')
    print(f"Old File:     {filepaths[0]}")
    print(f"New Folder:   {filepaths[1]}")
    print(f"New File:     {filepaths[2]}")
    if filepaths[4]:
        print(f"Jop File:     {filepaths[4]}")

def checkPath(path):
    if os.path.exists(path):
        print(f'Path exists : {path}')
    else:
        raise FileNotFoundError(f"The new file '{path}' does not exist.")

def readIOPH(filepaths):
    oldfilepath   = filepaths[0]
    newfilepath   = filepaths[1]

    print("Oldfilepath")
    checkPath(oldfilepath)
    print("Newfilepath")
    checkPath(newfilepath)

    pattern = re.compile(r'#define\s+(\w+)\s+(\S+)')
    with open(oldfilepath, 'r') as file:
    # Initialize a dictionary to store the name and corresponding number
        definitions = {}

        # Iterate through each line in the file
        for line in file:
            # Use the regular expression pattern to match lines with #define
            match = pattern.match(line)
            if match:
                # Extract the name and number from the matched groups
                name, number = match.groups()

                # Save the information in the dictionary
                definitions[name] = number

    return definitions

def readJOP(jop_filepath):
    """Parse a JetViewSoft .jop XML file and extract InputNumber and OutputNumber objects.

    Returns a dict keyed by ObjectName:
        { "InputNumber_I1": {"id": 9000, "scale": 1.0, "offset": 0, "decimals": 0}, ... }
    """
    tree = ET.parse(jop_filepath)
    root = tree.getroot()

    result = {}

    for obj in root.iter("Object"):
        cls = obj.get("Class")
        if cls not in ("CInputNumber", "COutputNumber"):
            continue

        name = obj.get("ObjectName")
        jvs_id = obj.get("JVS-ID")
        if not name or not jvs_id:
            continue

        # Extract properties from the PropertySheet children
        props = {}
        for prop in obj.iter("Property"):
            prop_name = prop.get("Name")
            value_el = prop.find("Value")
            if prop_name and value_el is not None and value_el.text:
                props[prop_name] = value_el.text.strip()

        obj_id   = int(jvs_id)
        scale    = float(props.get("Scale", "1"))
        offset   = int(props.get("Offset", "0"))
        decimals = int(props.get("NoOfDecimals", "0"))

        result[name] = {
            "id":       obj_id,
            "scale":    scale,
            "offset":   offset,
            "decimals": decimals,
        }

    return result

def writeGCFfile(data, filepaths):
    newfilepath = os.path.join(filepaths[1], filepaths[2]+'.gcf')

    root = ET.Element("GlobalConstants", Name=filepaths[2], Comment="Global constants")

    compiler_info = ET.SubElement(root, "CompilerInfo")
    compiler_info.set("packageName", filepaths[3])

    global_constants = ET.SubElement(root, "GlobalConstants")

    for name, value in data.items():
        var_declaration = ET.SubElement(global_constants, "VarDeclaration", Name=name, Type="UINT", InitialValue=value)

        if name == 'ISO_VERSION_LABEL':
            var_declaration.set('Type', 'STRING')
            var_declaration.set('InitialValue', '')

    # Create an ElementTree object and write it to a file
    tree = ET.ElementTree(root)

    # Create a string with indentation
    xml_str = ET.tostring(root, encoding='utf-8').decode()
    xml_str = minidom.parseString(xml_str).toprettyxml(indent="    ")

    # Adding UTF8-encoding
    xml_str = xml_str[:19] + ' ' + 'encoding="UTF-8"' + xml_str[20:]

    # Write the formatted XML to a file
    with open(newfilepath, "w") as file:
        file.write(xml_str)

def _format_real(value):
    """Format a float as an IEC 61131-3 REAL literal (no scientific notation)."""
    s = f"{float(value):.10f}".rstrip('0')
    if s.endswith('.'):
        s += '0'
    return s

def writeNumericGCFfile(data, filepaths):
    """Write a <name>_Numeric.gcf with NumericObjectPool_S constants for each InputNumber/OutputNumber."""
    newfilepath = os.path.join(filepaths[1], filepaths[2] + '_Numeric.gcf')
    gcf_name    = filepaths[2] + '_Numeric'
    package     = filepaths[3]
    struct_type = "isobus::UT::io::NumericValue::NumericObjectPool_S"

    root = ET.Element("GlobalConstants", Name=gcf_name, Comment="Numeric object pool constants (ID, Scale, Offset, Decimals)")

    compiler_info = ET.SubElement(root, "CompilerInfo")
    compiler_info.set("packageName", package)

    global_constants = ET.SubElement(root, "GlobalConstants")

    for name, info in sorted(data.items(), key=lambda x: x[1]["id"]):
        scale_str    = _format_real(info["scale"])
        offset_str   = str(info["offset"])
        decimals_str = str(info["decimals"])
        obj_id_str   = str(info["id"])

        initial_value = (
            f"(u16ObjId := {obj_id_str}, "
            f"r32Scale := {scale_str}, "
            f"i32Offset := {offset_str}, "
            f"u8Decimals := {decimals_str})"
        )

        ET.SubElement(
            global_constants,
            "VarDeclaration",
            Name=name,
            Type=struct_type,
            InitialValue=initial_value,
        )

    xml_str = ET.tostring(root, encoding='utf-8').decode()
    xml_str = minidom.parseString(xml_str).toprettyxml(indent="\t")
    xml_str = xml_str[:19] + ' ' + 'encoding="UTF-8"' + xml_str[20:]

    with open(newfilepath, "w") as file:
        file.write(xml_str)

    print(f"Written: {newfilepath}")


if __name__ == "__main__":

    # Gets filepaths and saves it in a variable
    filepaths = getPaths()

    os.makedirs(filepaths[1], exist_ok=True)

    # Prints filepaths
    printPaths(filepaths)
    file_data = readIOPH(filepaths)
    writeGCFfile(file_data, filepaths)

    # If a .jop file was provided, also generate the Numeric struct GCF
    if filepaths[4]:
        checkPath(filepaths[4])
        numeric_data = readJOP(filepaths[4])
        writeNumericGCFfile(numeric_data, filepaths)


__author__ = "Lorenz Bauer / Franz Höpfinger"
__version__ = "0.2"
__description__ = "Converts .iop.h to .gcf; optionally converts .jop to NumericObjectPool_S .gcf"
