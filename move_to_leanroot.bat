@echo off
chcp 65001
cls

::input file

set "cur=%~dp0"
set "fbxFile=%~f1"
pushd %cur%
set "envPath=%cur%env\python39"
set "scriptPath=%cur%fbxScript"

:: add to sysPath
set path=%SystemRoot%;%path%
set path=%SystemRoot%\system32;%path%
set "path=%envPath%;%path%"
set "path=%envPath%\Scripts;%path%"

:: using script
%envPath%\python.exe %scriptPath%\move_back_lean_root.py %fbxFile%
