import xml.etree.ElementTree as ET
import glob
import os
import re

def update_xml_file(filepath):
    """
    Aktualisiert eine XML-Datei, indem Attributwerte geändert und neue Elemente hinzugefügt werden.
    Args:
        filepath (str): Der Pfad zur zu aktualisierenden XML-Datei.
    """
    try:
        # Registrieren Sie den Standard-Namespace
        ET.register_namespace('', 'http://www.w3.org/2001/XMLSchema-instance')
        
        # Parse the XML file
        tree = ET.parse(filepath)
        root = tree.getroot()

        # Update all 'DigitalOutput_Qx' FB blocks
        for fb in root.findall(".//FB"):
            fb_name = fb.get("Name")
            if fb_name and re.match(r"DigitalOutput_Q\d+", fb_name):
                fb.set("Type", "logiBUS_QX")
                
                output_param_exists = any(p.get('Name') == 'Output' for p in fb.findall('Parameter'))
                if not output_param_exists:
                    # Dynamischer Wert für den Parameter "Output"
                    output_value = f"logiBUS_DO::Output_{fb_name.split('_')[1]}"
                    output_param = ET.Element("Parameter", Name="Output", Value=output_value)
                    fb.append(output_param)
                    print(f"  - Parameter 'Output' zu {fb_name} in {os.path.basename(filepath)} hinzugefügt.")

        # Update all 'DigitalInput_CLK_Ix' FB blocks
        for fb in root.findall(".//FB"):
            fb_name = fb.get("Name")
            if fb_name and re.match(r"DigitalInput_CLK_I\d+", fb_name):
                fb.set("Type", "logiBUS_IE")
                
                input_param_exists = any(p.get('Name') == 'Input' for p in fb.findall('Parameter'))
                if not input_param_exists:
                    # Dynamischer Wert für den Parameter "Input"
                    input_value = f"logiBUS_DI::Input_{fb_name.split('_')[2]}"
                    input_param = ET.Element("Parameter", Name="Input", Value=input_value)
                    fb.append(input_param)
                    print(f"  - Parameter 'Input' zu {fb_name} in {os.path.basename(filepath)} hinzugefügt.")

                input_event_param_exists = any(p.get('Name') == 'InputEvent' for p in fb.findall('Parameter'))
                if not input_event_param_exists:
                    input_event_param = ET.Element("Parameter", Name="InputEvent", Value="logiBUS_DI_Events::BUTTON_SINGLE_CLICK")
                    fb.append(input_event_param)
                    print(f"  - Parameter 'InputEvent' zu {fb_name} in {os.path.basename(filepath)} hinzugefügt.")

        # Speichern Sie die aktualisierte XML-Datei
        tree.write(filepath, encoding='UTF-8', xml_declaration=True)
        print(f"Datei erfolgreich aktualisiert und gespeichert: {filepath}")

    except FileNotFoundError:
        print(f"Fehler: Die Datei {filepath} wurde nicht gefunden.")
    except Exception as e:
        print(f"Ein Fehler ist bei der Verarbeitung von {filepath} aufgetreten: {e}")

def process_directory(directory_path):
    """
    Findet alle XML-Dateien in einem Verzeichnis und wendet die Update-Funktion auf jede an.
    Args:
        directory_path (str): Der Pfad zu dem Verzeichnis, das die XML-Dateien enthält.
    """
    xml_files = glob.glob(os.path.join(directory_path, '*.SUB'))
    
    if not xml_files:
        print(f"Keine XML-Dateien im Verzeichnis gefunden: {directory_path}")
        return

    print(f"Es wurden {len(xml_files)} XML-Datei(en) zum Verarbeiten gefunden.")
    for file_path in xml_files:
        print(f"\nVerarbeite Datei: {file_path}")
        update_xml_file(file_path)
    
    print("\nVerarbeitung abgeschlossen.")

# Beispiel-Nutzung
current_directory = os.getcwd()
process_directory(current_directory)