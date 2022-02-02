"""Implementación de Widgets diálogos personalizados.

"""
import sys
from helpGit import helpgnupg
from PyQt5.QtWidgets import (QDialog, QPushButton, QLabel,
                             QLineEdit, QComboBox, QGridLayout,
                             QHBoxLayout, QApplication, QMenu,
                             QTextEdit)


class   DialogEdit(QDialog):
    """Ventana de diálogo para editar datos de la
    aplicación."""
    def __init__(self, title, parent=None, values=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        if values is None:
            values = []
        self.values = values
        self.combo = QComboBox()
        self.combo.setEditable(True)
        self.combo.addItems(self.get_carpetas())
        self.le_nombre = QLineEdit()
        self.le_password = QLineEdit()
        self.b_generar = QPushButton('Generar')
        self.b_generar.clicked.connect(self.generar)
        self.text_edit = QTextEdit(self)
        self.b_aceptar = QPushButton('Aceptar')
        self.b_cancelar = QPushButton('Cancelar')

        grid = QGridLayout(self)
        grid.setSpacing(10)
        hbox = QHBoxLayout()
        grid.addWidget(QLabel('Carpeta: '), 0, 0)
        grid.addWidget(self.combo, 0, 1)
        grid.addWidget(QLabel('Nombre: '), 1, 0)
        grid.addWidget(self.le_nombre, 1, 1)
        grid.addWidget(QLabel("password: "), 2, 0)
        grid.addWidget(self.le_password, 2, 1)
        grid.addWidget(self.b_generar, 2, 2)
        grid.addWidget(self.text_edit, 3, 0, 1, 3)
        hbox.addStretch(1)
        hbox.addWidget(self.b_aceptar)
        hbox.addWidget(self.b_cancelar)
        grid.addLayout(hbox, 4, 1)
        self.setContentsMargins(15, 20, 15, 20)

    def get_carpetas(self):
        """Extrae de values una lista con carpetas."""
        lstcarpetas = ['']
        for value in self.values:
            if isinstance(value, list):
                lstcarpetas.append(value[0].name)
        return lstcarpetas

    def generar(self):
        """Generamos password y cumplimentamos la entrada."""
        password = helpgnupg.generador()
        self.le_password.setText(password)
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = DialogEdit('Ventana de Diálogo')
    win.show()

    sys.exit(app.exec())
