@echo off
cd /d "%~dp0\.."
pipreqs --ignore .venv . --force