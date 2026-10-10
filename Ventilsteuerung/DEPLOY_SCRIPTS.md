# ELF-Libs / Deploy – welches Skript macht was

Beide Skripte liegen hier in `Ventilsteuerung/` und werden normalerweise per
Doppelklick gestartet (oeffnet ein Git-Bash-Fenster, bleibt nach dem Lauf
offen bis Enter gedrueckt wird).

- **`make_libs_manifest.sh`** – erzeugt/aktualisiert nur lokal
  `boot-files/<Knoten>.libs.json`. Reine Dateierzeugung, kein
  Netzwerkzugriff.
- **`make_4diac_training1_deploy.sh`** – laedt `.fboot` (und bei
  `ENABLE_ELF_LIBS=1` zusaetzlich die benoetigten ELFs + das Manifest) per
  HTTP auf die Trainings-Knoten hoch. Rebootet NICHT automatisch – die
  hochgeladenen Dateien werden erst nach einem manuellen Neustart des
  Knotens aktiv (Reboot-Button auf `http://<ip>/`).

`deploy_common.sh` ist KEIN eigenes Skript zum Doppelklicken, sondern nur
eine gemeinsame Konfigurationsdatei (Knoten-IP ↔ Boot-Datei), die von den
beiden obigen per `source` eingebunden wird.

Fuer `test_AX` gibt es zusaetzlich das External Tool
`4diacIDE-workspace/test_AX/Launches/RunSkript_DeployAX.bat.launch`
(in der 4diac IDE unter Run As aufrufbar), das beide Skripte nacheinander
ausfuehrt (erst Manifest neu erzeugen, dann deployen).

Die eigentliche Namensraum-/Abhaengigkeits-Logik (welcher 4diac-Typ gehoert
zu welcher Lib, requires aus MANIFEST.MF, Firmware-Limits wie MAX_REQ=8 und
max. 16 Libs) steht in `elf_libs_manifest_lib.sh`.
