@echo off
rem Baut alle apixon-*-client Web-Clients (Vite/Vue).
rem Aufruf: build_all.bat          -> npm install (nur falls node_modules fehlt) + npm run build
rem         build_all.bat clean    -> immer npm ci vor dem Build
setlocal enabledelayedexpansion

set "ROOT=%~dp0"
set "CLEAN=0"
if /i "%~1"=="clean" set "CLEAN=1"

set "OKLIST="
set "FAILLIST="

for /d %%D in ("%ROOT%apixon-*-client") do (
    echo.
    echo ==== %%~nxD ====
    pushd "%%D"
    set "STEP_OK=1"

    if "!CLEAN!"=="1" (
        call npm ci
        if errorlevel 1 set "STEP_OK=0"
    ) else if not exist node_modules (
        call npm install
        if errorlevel 1 set "STEP_OK=0"
    )

    if "!STEP_OK!"=="1" (
        call npm run build
        if errorlevel 1 set "STEP_OK=0"
    )

    if "!STEP_OK!"=="1" (
        set "OKLIST=!OKLIST! %%~nxD"
    ) else (
        set "FAILLIST=!FAILLIST! %%~nxD"
    )
    popd
)

echo.
echo ==== Zusammenfassung ====
echo OK:   !OKLIST!
echo FAIL: !FAILLIST!

if defined FAILLIST exit /b 1
exit /b 0
