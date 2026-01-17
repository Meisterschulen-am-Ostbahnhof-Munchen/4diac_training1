import os
import glob

def rename_xml_to_adp():
    """
    Benennt .xml Dateien rekursiv in .adp um.
    HINWEIS: Dies betrifft alle .xml Dateien im Verzeichnisbaum.
    """
    files = glob.glob('**/*.xml', recursive=True)
    if not files:
        print("Keine .xml Dateien gefunden.")
        return
    
    for f in files:
        # Optional: Hier könnte man prüfen, ob die Datei ursprünglich eine .adp war
        # (z.B. durch Suchen nach <AdapterType> im Inhalt), um Standard-XMLs zu schützen.
        new_name = f[:-4] + '.adp'
        try:
            os.rename(f, new_name)
            print(f"Umbenannt: {f} -> {new_name}")
        except Exception as e:
            print(f"Fehler bei {f}: {e}")

if __name__ == "__main__":
    rename_xml_to_adp()
