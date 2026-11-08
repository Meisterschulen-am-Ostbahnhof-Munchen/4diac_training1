::Script

@echo off & setlocal

cd /d "%~dp0"

echo === Erzeuge ELF-Libs-Manifest (make_libs_manifest.py) ===
python ../../../scripts_central/make_libs_manifest.py
if errorlevel 1 exit /b 1

echo === Spiele Boot-Dateien auf Trainings-Knoten auf (make_4diac_training1_deploy.py) ===
python ../../../scripts_central/make_4diac_training1_deploy.py < NUL
if errorlevel 1 exit /b 1
