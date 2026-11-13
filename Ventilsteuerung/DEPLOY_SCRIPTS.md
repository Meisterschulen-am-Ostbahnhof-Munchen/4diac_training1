# Build- und Deploy-Skripte – welches Skript macht was

Alle Python-Skripte liegen in `scripts_central/`. Sie nutzen nur die
Standardbibliothek, eine pip-Installation ist nicht nötig, Git Bash auch
nicht. Die früheren Bash-Versionen (`elf_libs_manifest_lib.sh`,
`make_libs_manifest.sh`, `make_4diac_training1_deploy.sh`,
`deploy_common.sh`) sind entfernt. Bei Bedarf stehen sie in der Git-Historie,
Branch `feature/elf-loader`.

Die projektbezogenen Aufrufe liegen als dünne Wrapper in
`4diacIDE-workspace/test_*/scripts/` (`.bat` für Windows, teils `.sh` für
Linux). Die Python-Skripte enthalten keine festen Projektpfade.

## Deploy auf die Trainings-Knoten

| Skript | Wrapper (test_AX) | Was es tut |
|---|---|---|
| `make_libs_manifest.py` | `RunSkript_MakeLibsManifestAX.bat` | Erzeugt nur lokal `boot-files/<Knoten>.libs.json`. Kein Netzwerkzugriff. Mit `--out <Pfad>` lässt sich in eine andere Datei schreiben. |
| `make_4diac_training1_deploy.py` | `RunSkript_DeployAX.bat` (ruft beide Skripte nacheinander auf: erst Manifest, dann Deploy) | Lädt `.fboot` per HTTP auf die Trainings-Knoten. Bei `ENABLE_ELF_LIBS=True` kommen die benötigten ELFs und das Manifest dazu. |
| `make_4diac_training1_elf_preload.py` | `RunSkript_PreloadELF_AX.bat` | Bereitet einen Knoten für Online-Deploy aus der 4diac IDE vor, ganz ohne Bootfile (Details unten). |
| `make_4diac_training1_deploy_dido.py` | `RunSkript_Deploy_DIDO_AX.bat` (ohne `.launch`) | Deploy für den DIDO-Tester (Details unten). |

**`make_4diac_training1_elf_preload.py`** spielt die ELF-Grundausstattung
(`deploy_common.PRELOAD_LIBS` samt requires) nach `/data/elf-libs/`. Dazu legt
es das Manifest `elf_grundausstattung.libs.json` an, ohne `files`-Eintrag und
damit ohne Bindung an ein Bootfile. **Alle anderen `*.libs.json` und alle
`*.fboot` auf dem Knoten werden gelöscht.** Nach dem Neustart startet FORTE
leer, mit geladener Grundausstattung.

- Ziel: ohne Argument `logibus.local` per mDNS, sonst die angegebenen
  Hosts/IPs.
- Ein späteres normales Deploy ersetzt das Grundausstattungs-Manifest. Die
  ELFs bleiben liegen und werden per Hash übersprungen.

**`make_4diac_training1_deploy_dido.py`** ist für den DIDO-Tester
(`InputOutputTesterButton_DIDO_OPC_UA`) gedacht. Es lädt Bootfile,
Libs-Manifest und ELFs wie das normale Deploy hoch. Zusätzlich kommen nach
`/data/`:

- der VT-Pool `DefaultPool.iop`,
- die Sichtbarkeitstabelle `DefaultPool.vis.json` (aus `Workspace_DIDO`),
- der Web-Client `apixon-diodo.html`.

Ziel: Standard `logibus.local`, sonst als Argument. Das Skript baut nichts
selbst: Bootfile (4diac IDE), Pool (ISO-Designer) und Web-Client
(`npm run build`) müssen vorher aktuell sein.

**Für alle Deploy-Skripte gilt:**

- Sie rebooten **nicht**. Die hochgeladenen Dateien werden erst nach einem
  manuellen Neustart des Knotens aktiv (Reboot-Button auf `http://<ip>/`).
- Sie bauen nichts. Die Bootfiles müssen vorher aus der IDE exportiert sein.
- Die Architektur des Knotens fragen sie per `GET /deviceinfo/` ab.
  `NODE_ARCH` in `elf_libs_manifest_lib.py` gilt nur als Rückfall für ältere
  Firmware ohne diesen Endpunkt.

`deploy_common.py` ist **kein** eigenes Skript zum Ausführen. Es ist ein
gemeinsames Modul (Knoten-IP ↔ Boot-Datei, `PRELOAD_LIBS`), das die Skripte
oben importieren. Bekannt ist derzeit nur der AX-Knoten `192.168.178.45`.

Die Namensraum- und Abhängigkeits-Logik steht in
`scripts_central/elf_libs_manifest_lib.py`:

- welcher 4diac-Typ zu welcher Lib gehört,
- requires aus `MANIFEST.MF`,
- Firmware-Limits wie `MAX_REQ=8` und höchstens 64 Libs.

**Vorsicht bei echten Deploys:** Die Deploy- und Preload-Skripte laden
wirklich auf den Knoten hoch, einen Trockenlauf gibt es nicht. Vor
wiederholten Testläufen den freien Speicher im Blick behalten:

- `http://<ip>/space/` zeigt die Belegung. Seit Firmware-Commit b1cd09e7
  steht sie nicht mehr auf der Hauptseite, weil die Berechnung die
  Dateiliste spürbar verlangsamt hat.
- Ein fast volles LittleFS-Dateisystem kann bei weiteren Uploads
  korrumpieren. Es wird dann beim nächsten Boot automatisch neu formatiert,
  und alle Dateien sind weg.

## Build: ISO-Designer-Pool → GCF-Konstanten

| Skript | Was es tut |
|---|---|
| `compile_iso_designer_project.py --pool-dir <Pool>` | Kompiliert ein ISO-Designer-Projekt über `ISODesigner.exe /Compile`. Es wartet auf `Output/CompileLog.txt` und beendet danach nur diesen einen Prozess. Andere offene ISO-Designer-Fenster bleiben unberührt. |
| `GcfScript.py` | Erzeugt aus `Output/<Pool>.iop.h` (optional mit `.jop`) die Konstanten-Datei `<Pool>.gcf` und `<Pool>_Numeric.gcf` unter `Uebungen/const/UT/`. Die erzeugten `.gcf` nie von Hand ändern, sondern Pool oder Skript ändern und neu erzeugen. |
| `list_mask_objects.py --pool-dir <Pool>` | Nur lesend. Listet je Maske die erreichbaren Objekte auf. Mit `--emit-visibility`/`--emit-visibility-json` schreibt es die Sichtbarkeitstabelle `<Pool>.vis.csv`/`.vis.json`. |

Wrapper je Pool:

- **`RunSkript_Build<Pool>_AX.bat`** (test_AX, z. B.
  `RunSkript_BuildAX.bat`, `RunSkript_BuildEmpty_AX.bat`): Kompilieren, alte
  GCF löschen, `GcfScript.py`, `list_mask_objects.py`. Bricht beim ersten
  Fehler ab.
- **`RunSkript_Workspace_<Pool>_*.bat/.sh`**: nur der GCF-Schritt, ohne
  Kompilieren. Unter Linux für test_AX, unter Windows und Linux für test_B
  und test_VV.
- **`RunSkript_ALL_AX.bat` / `RunSkript_ALL_B.bat/.sh`**: rufen alle Wrapper
  eines Projekts nacheinander auf.

## Prüfskripte

`check_mixed_numeric_pool_imports.py` (Wrapper
`RunSkript_CheckMixedPoolImports_AX.bat/.sh`) findet `.SUB`-Dateien, die
VT-Konstanten aus **mehreren verschiedenen** Pools importieren, etwa teils
aus `DefaultPool_AIC_Numeric` und teils aus `DefaultPool_AIC_3P_Numeric`.
Das ist ein typischer Copy-Paste-Rest.

## Launch-Arten in der 4diac IDE

Die `.launch`-Dateien in `test_*/Launches/` erscheinen in der IDE unter
Run As bzw. External Tools. Es gibt drei Arten:

| Art | Beispiel | Funktion |
|---|---|---|
| External Tool (`ProgramLaunchConfigurationType`) | `RunSkript_DeployAX.bat.launch`, `RunSkript_PreloadELF_AX.bat.launch`, `RunSkript_Build*.bat.launch` | Startet die gleichnamige `.bat` in `scripts/` und frischt danach das Projekt auf. |
| Deploy (`deployLaunch`) | `Deploy_App_AX.launch`, `Deploy_App_<Training>.launch` (test_VV) | Online-Deploy aus der IDE auf die ausgewählten Geräte/Ressourcen des Systems. |
| Gruppe (`GroupLaunchConfigurationType`) | `Launch_Deploy_App_AX.launch` | Führt mehrere Launches nacheinander aus, z. B. erst `RunSkript_BuildAX.bat` (wartet auf das Ende), dann `Deploy_App_AX`. |

Für das Online-Deploy aus der IDE muss die ELF-Grundausstattung auf dem
Knoten liegen, also einmal `RunSkript_PreloadELF_AX` laufen lassen und den
Knoten neu starten.
