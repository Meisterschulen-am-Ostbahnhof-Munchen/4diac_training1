::Script
:: Erzeugt/aktualisiert nur lokal boot-files/<fboot-name>.libs.json - kein
:: Netzwerkzugriff. Siehe scripts_central/make_libs_manifest.py.

@echo off & setlocal

cd /d "%~dp0"
python ../../../scripts_central/make_libs_manifest.py
