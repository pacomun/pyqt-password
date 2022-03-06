#!/usr/bin/env bash

# Script para lanzar la aplicación pyqt-pass dentro
# de su entorno virtual.
cd /usr/share/pyqt-password
source .Venv/bin/activate
exec  python mvc.py
