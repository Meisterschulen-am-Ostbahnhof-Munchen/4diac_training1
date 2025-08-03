import xml.etree.ElementTree as ET
import glob
import os

def update_xml_file(filepath):
    """
    Aktualisiert eine XML-Datei, indem Attributwerte geändert und neue Elemente hinzugefügt werden.
    Args:
        filepath (str): Der Pfad zur zu aktualisierenden XML-Datei.
    """
    try:
        # Registrieren Sie den Standard-Namespace, um Präfixe wie ns0 in der Ausgabe zu vermeiden.
        ET.register_namespace('', 'http://www.w3.org/2001/XMLSchema-instance')
        
        # Parse the XML file
        tree = ET.parse(filepath)
        root = tree.getroot()

        # Update the 'DigitalOutput_Q1' FB block
        for fb in root.findall(".//FB[@Name='DigitalOutput_Q1']"):
            fb.set("Type", "logiBUS_QX")
            
            # Überprüfen Sie, ob der Parameter bereits existiert, um Duplikate zu vermeiden
            output_param_exists = any(p.get('Name') == 'Output' for p in fb.findall('Parameter'))
            if not output_param_exists:
                output_param = ET.Element("Parameter", Name="Output", Value="logiBUS_DO::Output_Q1")
                fb.append(output_param)
                print(f"  - Parameter 'Output' zu DigitalOutput_Q1 in {os.path.basename(filepath)} hinzugefügt.")

        # Update the 'DigitalInput_CLK_I1' FB block
        for fb in root.findall(".//FB[@Name='DigitalInput_CLK_I1']"):
            fb.set("Type", "logiBUS_IE")
            
            # Überprüfen Sie auf vorhandene Parameter, bevor Sie sie hinzufügen, um Duplikate zu vermeiden
            input_param_exists = any(p.get('Name') == 'Input' for p in fb.findall('Parameter'))
            if not input_param_exists:
                input_param = ET.Element("Parameter", Name="Input", Value="logiBUS_DI::Input_I1")
                fb.append(input_param)
                print(f"  - Parameter 'Input' zu DigitalInput_CLK_I1 in {os.path.basename(filepath)} hinzugefügt.")

            input_event_param_exists = any(p.get('Name') == 'InputEvent' for p in fb.findall('Parameter'))
            if not input_event_param_exists:
                input_event_param = ET.Element("Parameter", Name="InputEvent", Value="logiBUS_DI_Events::BUTTON_SINGLE_CLICK")
                fb.append(input_event_param)
                print(f"  - Parameter 'InputEvent' zu DigitalInput_CLK_I1 in {os.path.basename(filepath)} hinzugefügt.")

        # Speichern Sie die aktualisierte XML-Datei mit korrekter Formatierung
        # Verwendung von 'xml_declaration=True' und 'encoding='UTF-8''
        # hilft, die Formatierung konsistent zu halten.
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
    # Use glob to find all files ending with .xml
    # Adjust the pattern if your files have a different naming convention
    xml_files = glob.glob(os.path.join(directory_path, '*.SUB'))
    
    if not xml_files:
        print(f"Keine XML-Dateien im Verzeichnis gefunden: {directory_path}")
        return

    print(f"Es wurden {len(xml_files)} XML-Datei(en) zum Verarbeiten gefunden.")
    for file_path in xml_files:
        print(f"\nVerarbeite Datei: {file_path}")
        update_xml_file(file_path)
    
    print("\nVerarbeitung abgeschlossen.")

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