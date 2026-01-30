import os

def xml_to_adp_reverse():
    """
    RÜCKWÄRTS-VARIANTE:
    Durchsucht rekursiv alle Ordner nach .xml Dateien
    und benennt sie zurück in .adp um.
    """
    # 1. Startverzeichnis bestimmen
    root_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Starte Rückbenennung (XML -> ADP) in: {root_dir}")
    print("-" * 40)

    count = 0
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            # ACHTUNG: Wir suchen jetzt nach .xml
            if filename.lower().endswith('.xml'):
                
                old_file_path = os.path.join(dirpath, filename)
                
                # Wir ändern die Endung zurück zu .adp
                base_name = os.path.splitext(old_file_path)[0]
                new_file_path = base_name + ".adp"
                
                try:
                    os.rename(old_file_path, new_file_path)
                    print(f"[RESTORE] {filename} -> .adp")
                    count += 1
                except Exception as e:
                    print(f"[FEHLER] Konnte {filename} nicht zurücksetzen. Grund: {e}")

    print("-" * 40)
    if count == 0:
        print("Keine .xml Dateien gefunden, die zurückgesetzt werden könnten.")
    else:
        print(f"Fertig! {count} Dateien wurden wieder zu .adp.")

if __name__ == "__main__":
    xml_to_adp_reverse()