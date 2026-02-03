# Script PowerShell para lanzar la Calculadora Básica Accesible
# Navega al directorio src y ejecuta la calculadora

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -Path "$scriptPath\src"
python basic_calculathor.py
