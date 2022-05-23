@echo off
chcp 65001
cls

:: add to sysPath
set "path=%SystemRoot%;%path%"
set "path=%SystemRoot%\system32;%path%"
set "path=%envPath%;%path%"
set "path=%envPath%\Scripts;%path%"

:: input file
set "cur=%~dp0"
set "fbxFile=%~f1"
pushd %cur%

set "scriptPath=%cur%fbxScript"

:: check python env
set "pythonEnvPath=%cur%env\python39"
if exist %pythonEnvPath% do (
    set "pythonExec=%pythonEnvPath%\python.exe"
) else (
    set "pythonExec=python.exe"
)

:: using script
set "scriptName=move_back_lean_root.py"
%pythonExec% %scriptPath%\%scriptName% %fbxFile%

pause
:EOF