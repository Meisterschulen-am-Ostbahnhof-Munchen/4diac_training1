import xml.etree.ElementTree as ET
import glob
import os

def update_xml_file(filepath):
    """
    Updates an XML file by changing attribute values and adding new elements.
    Args:
        filepath (str): The path to the XML file to be updated.
    """
    try:
        # Register the default namespace to avoid prefixes like ns0 in the output
        ET.register_namespace('', 'http://www.w3.org/2001/XMLSchema-instance')
        
        tree = ET.parse(filepath)
        root = tree.getroot()

        # Update the 'DigitalOutput_Q1' FB block
        for fb in root.findall(".//FB[@Name='DigitalOutput_Q1']"):
            fb.set("Type", "logiBUS_QX")
            
            # Check if the parameter already exists to avoid duplicates
            if not fb.find("Parameter[@Name='Output']") is not None:
                output_param = ET.Element("Parameter", Name="Output", Value="logiBUS_DO::Output_Q1")
                fb.append(output_param)
                print(f"  - Updated DigitalOutput_Q1 in {os.path.basename(filepath)}")

        # Update the 'DigitalInput_CLK_I1' FB block
        for fb in root.findall(".//FB[@Name='DigitalInput_CLK_I1']"):
            fb.set("Type", "logiBUS_IE")
            
            # Check for existing parameters before adding to avoid duplicates
            if not fb.find("Parameter[@Name='Input']") is not None:
                input_param = ET.Element("Parameter", Name="Input", Value="logiBUS_DI::Input_I1")
                fb.append(input_param)

            if not fb.find("Parameter[@Name='InputEvent']") is not None:
                input_event_param = ET.Element("Parameter", Name="InputEvent", Value="logiBUS_DI_Events::BUTTON_SINGLE_CLICK")
                fb.append(input_event_param)
                print(f"  - Updated DigitalInput_CLK_I1 in {os.path.basename(filepath)}")

        # Save the updated XML to the same file with a proper formatting
        tree.write(filepath, encoding='UTF-8', xml_declaration=True)
        print(f"Successfully updated and saved the file: {filepath}")

    except FileNotFoundError:
        print(f"Error: The file {filepath} was not found.")
    except Exception as e:
        print(f"An error occurred while processing {filepath}: {e}")

def process_directory(directory_path):
    """
    Finds all XML files in a directory and applies the update function to each.
    Args:
        directory_path (str): The path to the directory containing the XML files.
    """
    # Use glob to find all files ending with .xml
    # Adjust the pattern if your files have a different naming convention
    xml_files = glob.glob(os.path.join(directory_path, '*.SUB'))
    
    if not xml_files:
        print(f"No XML files found in the directory: {directory_path}")
        return

    print(f"Found {len(xml_files)} XML file(s) to process.")
    for file_path in xml_files:
        print(f"\nProcessing file: {file_path}")
        update_xml_file(file_path)
    
    print("\nProcessing complete.")

# --- Beispiel-Nutzung ---
# Ersetzen Sie 'pfad/zu/ihrem/verzeichnis' mit dem tatsächlichen Pfad zu Ihrem Verzeichnis.
# Das Skript ändert alle .xml-Dateien, die sich direkt in diesem Verzeichnis befinden.
# Seien Sie vorsichtig und erstellen Sie vor der Ausführung ein Backup Ihrer Dateien.
# process_directory('pfad/zu/ihrem/verzeichnis')

# Beispiel mit dem aktuellen Verzeichnis
# current_directory = os.getcwd()
# process_directory(current_directory)

# Beispiel mit einem spezifischen Verzeichnis
current_directory = os.getcwd()
process_directory(current_directory)