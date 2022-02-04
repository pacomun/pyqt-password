"""Implementación de Widgets diálogos personalizados.

"""
import sys
from pathlib import Path
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
        self.b_aceptar.clicked.connect(self.boton_aceptar)
        self.b_cancelar = QPushButton('Cancelar')
        self.b_cancelar.clicked.connect(self.close)

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

    def boton_aceptar(self):
        """Recuperar datos cumplimentados. Si todo va bien, se guarda
        el archivo cifrado"""
        if __debug__:
            print('carpeta: ', self.combo.lineEdit().text())
            print('nombre: ', self.le_nombre.text())
            print('password: ', self.le_password.text())
            print('datos extra: ', self.text_edit.toPlainText())
        datos = [self.combo.lineEdit().text(),
                 self.le_nombre.text(),
                 self.le_password.text(),
                 self.text_edit.toPlainText()]
        archivo = helpgnupg.guardar_archivo(datos)
        helpgnupg.cifrar_archivo(archivo)
        self.accept()


class DialogModificar(DialogEdit):
    """Clase derivada de DialogoEdit para modificar una clave."""
    def __init__(self, archivo, title, parent=None, values=None ):
        super().__init__(title=title, parent=parent, values=values)
        self.archivo = Path(archivo)
        self.datos_iniciales = self.get_datos()
        self.combo.lineEdit().setText(self.datos_iniciales[0])
        self.le_nombre.setText(self.datos_iniciales[1])
        self.le_password.setText(self.datos_iniciales[2])
        self.text_edit.setText(self.datos_iniciales[3])

    def get_datos(self) -> list:
        """Devuelve lista con los siguiente valores: carpeta,
        nombre, password, y datos extra.

        """
        carpeta = self.archivo.parents[0].name
        if carpeta == Path.cwd().name:
            carpeta = ''
        nombre = self.archivo.stem
        lst_contenido = helpgnupg.descifrar_archivo(self.archivo)
        if len(lst_contenido) > 1:
            datos_extra = '\n'.join(lst_contenido[1:])
        else:
            datos_extra = ''
        password = lst_contenido[0]

        return [carpeta, nombre, password, datos_extra]

    def boton_aceptar(self):
        """Redefinición del método para poder borrar archivo
        modificado si procede"""
        datos = [self.combo.lineEdit().text(),
                 self.le_nombre.text(),
                 self.le_password.text(),
                 self.text_edit.toPlainText()]
        archivo = helpgnupg.guardar_archivo(datos)
        helpgnupg.cifrar_archivo(archivo)

        # Borrar archivo si se renombra o cambia ubicación
        if datos[:2] != self.datos_iniciales[:2]:
            Path(self.archivo).unlink()
        self.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = DialogEdit('Ventana de Diálogo')
    win.show()

    sys.exit(app.exec())
