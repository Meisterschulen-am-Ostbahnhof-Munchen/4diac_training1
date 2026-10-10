# ELF-Libs / Deploy – welches Skript macht was

Alle Skripte liegen in `scripts_central/` und sind reines Python (Stdlib,
keine pip-Installation noetig) - kein Git Bash mehr erforderlich (fruehere
Bash-Versionen `elf_libs_manifest_lib.sh`/`make_libs_manifest.sh`/
`make_4diac_training1_deploy.sh`/`deploy_common.sh` sind entfernt, siehe
Git-Historie Branch `feature/elf-loader` bei Bedarf).

- **`scripts_central/make_libs_manifest.py`** – erzeugt/aktualisiert nur
  lokal `boot-files/<Knoten>.libs.json`. Reine Dateierzeugung, kein
  Netzwerkzugriff.
- **`scripts_central/make_4diac_training1_deploy.py`** – laedt `.fboot`
  (und bei `ENABLE_ELF_LIBS=True` zusaetzlich die benoetigten ELFs + das
  Manifest) per HTTP auf die Trainings-Knoten hoch. Rebootet NICHT
  automatisch – die hochgeladenen Dateien werden erst nach einem manuellen
  Neustart des Knotens aktiv (Reboot-Button auf `http://<ip>/`).

`scripts_central/deploy_common.py` ist KEIN eigenes Skript zum Ausfuehren,
sondern nur ein gemeinsames Modul (Knoten-IP ↔ Boot-Datei), das von den
beiden obigen importiert wird.

Fuer `test_AX` gibt es zusaetzlich das External Tool
`4diacIDE-workspace/test_AX/Launches/RunSkript_DeployAX.bat.launch`
(in der 4diac IDE unter Run As aufrufbar, `.bat` ruft nur noch `python`
auf), das beide Skripte nacheinander ausfuehrt (erst Manifest neu
erzeugen, dann deployen).

Die eigentliche Namensraum-/Abhaengigkeits-Logik (welcher 4diac-Typ gehoert
zu welcher Lib, requires aus MANIFEST.MF, Firmware-Limits wie MAX_REQ=8 und
max. 16 Libs) steht in `scripts_central/elf_libs_manifest_lib.py`.

**Vorsicht bei echten Deploys:** `make_4diac_training1_deploy.py` laedt
wirklich auf den Knoten hoch (kein Trockenlauf-Modus). Vor wiederholten
Testlaeufen gegen den echten Knoten den freien Speicher im Blick behalten
(`http://<ip>/` zeigt die Belegung) - ein fast volles LittleFS-Dateisystem
kann bei weiteren Uploads korrumpieren und wird beim naechsten Boot
automatisch neu formatiert (alle Dateien weg).
