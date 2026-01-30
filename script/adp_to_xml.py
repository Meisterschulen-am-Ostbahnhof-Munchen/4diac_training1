import os

def rename_recursive_deep():
    """
    Durchsucht rekursiv alle Ordner und Unterordner nach .adp Dateien
    und benennt sie in .xml um.
    """
    # 1. Startverzeichnis bestimmen (dort wo dieses Skript liegt)
    root_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Starte tiefe Suche in: {root_dir}")
    print("-" * 40)

    count = 0
    
    # 2. os.walk geht Schritt für Schritt durch den gesamten Baum
    # dirpath: Der Pfad zum aktuellen Ordner, den er gerade anschaut
    # dirnames: Liste der Unterordner im aktuellen Ordner
    # filenames: Liste der Dateien im aktuellen Ordner
    for dirpath, dirnames, filenames in os.walk(root_dir):
        
        for filename in filenames:
            # Wir prüfen die Endung (case-insensitive durch .lower())
            if filename.lower().endswith('.adp'):
                
                # Den vollen Pfad zur Datei bauen
                old_file_path = os.path.join(dirpath, filename)
                
                # Neuen Namen bauen (Endung tauschen)
                base_name = os.path.splitext(old_file_path)[0]
                new_file_path = base_name + ".xml"
                
                try:
                    os.rename(old_file_path, new_file_path)
                    print(f"[OK] {filename} -> .xml")
                    count += 1
                except Exception as e:
                    print(f"[FEHLER] Konnte {filename} nicht umbenennen. Grund: {e}")

    print("-" * 40)
    if count == 0:
        print("Keine .adp Dateien in den Unterordnern gefunden.")
    else:
        print(f"Fertig! {count} Dateien wurden umbenannt.")

if __name__ == "__main__":
    rename_recursive_deep()