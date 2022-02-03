"""Funciones para cifrado desdcifrado...

"""
import os
from pathlib import Path
import gnupg
import secrets
import string


def get_recipient() -> str:
    """Consigue keyid privada del ususario"""
    gpg = gnupg.GPG(use_agent=True)
    private_key = gpg.list_keys()
    return private_key[0]['keyid']


def descifrar_archivo(ruta: str) -> list:
    """Devuelve una lista con las líneas del archivo
    descifrado."""
    ruta = Path(ruta)
    gpg = gnupg.GPG(use_agent=True)
    gpg.encoding = 'utf-8'
    if not ruta.is_dir():
        with open(ruta, 'rb') as f_arch:
            datos_claro = gpg.decrypt_file(f_arch)
        if datos_claro.ok is True:
            if __debug__:
                print(str(datos_claro))
            return (str(datos_claro).split('\n'))

    return ['Error al descifrar archivo', datos_claro.status]


def generador(ndigit=8):
    """ Generar contraseña segura de n-digitos."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(ndigit))


def guardar_archivo(datos) -> bool | str:
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
