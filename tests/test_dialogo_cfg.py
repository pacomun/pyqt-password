"""Test para verificar el funcionamiento de las
clases en dialogo.py"""
import sys
from helpGit.dialogos import DialogEdit, DialogoConfig
from PyQt5.QtWidgets import QApplication


app = QApplication(sys.argv)
win = DialogoConfig(title='Ventana de Configuración')
win.show()

sys.exit(app.exec())
