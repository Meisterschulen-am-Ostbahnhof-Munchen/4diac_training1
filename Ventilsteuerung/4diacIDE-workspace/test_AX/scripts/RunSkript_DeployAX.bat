::Script

@echo off & setlocal

cd /d "%~dp0"

echo === Erzeuge ELF-Libs-Manifest (make_libs_manifest.sh) ===
"C:\Program Files\Git\bin\bash.exe" ../../../make_libs_manifest.sh < NUL
if errorlevel 1 exit /b 1

echo === Spiele Boot-Dateien auf Trainings-Knoten auf (make_4diac_training1_deploy.sh) ===
"C:\Program Files\Git\bin\bash.exe" ../../../make_4diac_training1_deploy.sh < NUL
if errorlevel 1 exit /b 1
