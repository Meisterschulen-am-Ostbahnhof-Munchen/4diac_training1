::Script
:: DIDO-Tester auf die Trainings-Platine: Bootfile + Libs-Manifest + ELFs,
:: DefaultPool.iop + DefaultPool.vis.json (Workspace_DIDO) und
:: apixon-diodo.html - siehe scripts_central/make_4diac_training1_deploy_dido.py.
:: Ziel Standard logibus.local, sonst als Argument (z.B. 169.254.50.85).
:: Danach neu starten.

@echo off & setlocal

cd /d "%~dp0"

echo === Deploy DIDO-Tester (make_4diac_training1_deploy_dido.py) ===
python ../../../scripts_central/make_4diac_training1_deploy_dido.py %* < NUL
if errorlevel 1 exit /b 1
