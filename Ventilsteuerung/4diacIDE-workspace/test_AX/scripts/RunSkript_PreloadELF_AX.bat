::Script
:: Spielt die ELF-Grundausstattung (deploy_common.PRELOAD_LIBS) ohne Bootfile
:: und ohne Manifest auf die Trainings-Knoten - siehe
:: scripts_central/make_4diac_training1_elf_preload.py.

@echo off & setlocal

cd /d "%~dp0"

echo === Spiele ELF-Grundausstattung auf Trainings-Knoten auf (make_4diac_training1_elf_preload.py) ===
python ../../../scripts_central/make_4diac_training1_elf_preload.py < NUL
if errorlevel 1 exit /b 1
