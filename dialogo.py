"""Programa que muestra una ventana de diálogo con un boton
y una entrada de texto. Escribe en la caja de texto y te
mostrará un saludo
"""
import sys
from PySide6.QtWidgets import (QApplication,
                               QDialog,
                               QLineEdit,
                               QPushButton,
                               QVBoxLayout)


class Form(QDialog):
    """Clase diálogo de ejmplo."""
    def __init__(self, parent=None):
        """Constructor de la clase."""
        super().__init__(parent)
        self.setWindowTitle("Mi Formulario")
        self.resize(400, 300)
        # Creamos los widgets
        self.edit = QLineEdit("Escribe tu nombre aqui...")
        self.button = QPushButton("Mostrar saludo")
        # Crear una capa para organizar los widgets
        layout = QVBoxLayout(self)
        layout.addWidget(self.edit)
        layout.addWidget(self.button, 1)
        # Creamos la funcion para saludar y conectar el
        # botón
        self.button.clicked.connect(self.greetings)

    def greetings(self):
        "Ejecuta el saludo."
        print(f'Hola {self.edit.text()}')


if __name__ == '__main__':
    # Creamos la aplicacion Qt
    app = QApplication(sys.argv)
    # Crear y mostrar el formulario
    form = Form()
    form.show()

    # Correr el lazo Qt main
    sys.exit(app.exec())
