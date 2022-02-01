"""Funciones varias para ayunda.

"""
import os
from pathlib import Path
import gnupg


def get_datos(treeview):
    """Recibe un objeto Gtk.TreeView y
    devuelve lista con datos extraidos"""
    gpg = gnupg.GPG(use_agent=True)
    gpg.encoding = 'utf-8'
    modelo = treeview.get_model()
    fila, columna = treeview.get_cursor()
    del columna
    dict_datos = {
        'carpeta': '',
        'nombre': modelo[fila][0],
        'cont': '',
        'extra': '',
    }
    archivo = Path(modelo[fila][1])
    archivo = archivo.resolve()
    dir_work = Path.cwd()
    if archivo.is_file() is True:
        if dir_work.samefile(os.path.dirname(archivo)):
            dict_datos['carpeta'] = ''
        else:
            dict_datos['carpeta'] = Path(archivo.parent).name
        with open(archivo, 'rb') as f_rb:
            d_descifrado = gpg.decrypt_file(f_rb)
        contenido_arch = str(d_descifrado).split('\n')
        dict_datos['cont'] = contenido_arch[0]
        dict_datos['extra'] = ''
        if len(contenido_arch) > 1:
            for c_extra in contenido_arch[1:]:
                dict_datos['extra'] += c_extra
        print('Datos conseguidos en get_datos: ', dict_datos)
    return list(dict_datos.values())


def get_carpetas():
    """Devuelve lista con carpetas"""
    w_path = os.getcwd()
    listado = os.scandir(w_path)
    carpetas = []
    for i_list in listado:
        if i_list.is_dir() is True:
            if i_list.name[0] != '.':
                if i_list.name[0] != '_':
                    carpetas.append(i_list)
    return carpetas


def guardar_archivo(datos):
    """Recibe lista/tupla con 4 elementos. Con
    estos escribe en archivo."""
    if len(datos) != 4:
        return False

    carpeta, nombre, cont, extra = datos
    w_dir = Path.cwd()
    arch = w_dir
    if carpeta != '':
        arch = arch / carpeta
        print('valor de arch: ', arch)
        if arch.exists() is False:
            print('Se crea la carpeta: ', arch)
            os.mkdir(arch)
    arch = arch / nombre
    try:
        with open(arch, 'w', encoding='utf-8') as f_w:
            f_w.write(cont)
            if extra != '':
                f_w.write('\n')
            f_w.write(extra)
    except FileNotFoundError as file_no_found:
        print('Carpeta no existe', file_no_found)
    return arch


def borra_archivo_modificado(datos):
    """Borra archivo que construye con los
    datos pasados."""
    print('llamada a borrar archivo...')
    carpeta, nombre, cont, extra = datos
    del cont, extra
    arch = Path.cwd()
    if carpeta != '':
        arch = arch.joinpath(carpeta)
    arch = arch.joinpath(nombre)
    os.remove(arch)


def get_recipient():
    """Consigue keyid privada del ususario"""
    gpg = gnupg.GPG(use_agent=True)
    private_key = gpg.list_keys()
    return private_key[0]['keyid']


def cifrar_archivo(archivo):
    """cifra un archivo con la clave por defecto
    del usuario"""
    gpg = gnupg.GPG(use_agent=True)
    gpg.encoding = 'utf-8'
    private_key = gpg.list_keys(True)
    bandeja = private_key[0]['keyid']
    print('recipients: ', bandeja)

    # Lectura de archivo en claro y cifrado
    n_arch = archivo.parent
    name_archivo = archivo.stem + '.gpg'
    n_arch = n_arch.joinpath(name_archivo)
    f_arch = open(archivo, 'r', encoding='utf-8')
    texto_claro =f_arch.read()
    print('texto leído ', texto_claro)
    f_arch.close()
    encrypted_ascii_data = gpg.encrypt(
        texto_claro,
        bandeja,
        output=n_arch
    )
    print('datos cifrados', str(encrypted_ascii_data))

    if encrypted_ascii_data.ok is True:
        os.remove(archivo)
    else:
        print(encrypted_ascii_data.status)


if __name__ == '__main__':
    lista = get_carpetas()
    for i in lista:
        print(i.path)

    with open('archivo', 'w', encoding='utf-8') as f:
        f.write('Texto a cifrar')

    recipients = get_recipient()
    cifrar_archivo('archivo')
    print(get_recipient())
