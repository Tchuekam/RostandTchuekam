@echo off
rem Hermes Agent Gateway - Messaging Platform Integration
cd /d D:\hermes-home\Tchuekam-agent
set "HERMES_HOME=D:\hermes-home"
set "PYTHONIOENCODING=utf-8"
set "HERMES_GATEWAY_DETACHED=1"
set "VIRTUAL_ENV=D:\hermes-home\Tchuekam-agent\venv"
D:\hermes-home\Tchuekam-agent\venv\Scripts\pythonw.exe -m hermes_cli.main gateway run
exit /b 0
