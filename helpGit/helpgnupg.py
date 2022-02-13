"""Funciones para cifrado desdcifrado...

"""
import os
from pathlib import Path
import gnupg
import secrets
import string
import subprocess


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


def guardar_archivo(datos) -> str:
    """Recibe lista/tupla con 4 elementos. Con
    estos escribe en archivo."""
    if len(datos) != 4:
        return False

    carpeta, nombre, cont, extra = datos
    w_dir = Path.cwd()
    arch = w_dir
    if carpeta != '':
        arch = arch / carpeta
        if __debug__:
            print('valor de arch: ', arch)
        if arch.exists() is False:
            if __debug__:
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
    carpeta, nombre, cont, extra = datos
    del cont, extra
    arch = Path.cwd()
    if carpeta != '':
        arch = arch.joinpath(carpeta)
    arch = arch.joinpath(nombre)
    os.remove(arch)


def cifrar_archivo(archivo):
    """cifra un archivo con la clave por defecto
    del usuario"""
    gpg = gnupg.GPG(use_agent=True)
    gpg.encoding = 'utf-8'
    private_key = gpg.list_keys(True)
    bandeja = private_key[0]['keyid']
    if __debug__:
        print('recipients: ', bandeja)

    # Lectura de archivo en claro y cifrado
    n_arch = archivo.parent
    name_archivo = archivo.stem + '.gpg'
    n_arch = n_arch.joinpath(name_archivo)
    f_arch = open(archivo, 'r', encoding='utf-8')
    texto_claro = f_arch.read()
    if __debug__:
        print('texto leído ', texto_claro)
    f_arch.close()
    encrypted_ascii_data = gpg.encrypt(
        texto_claro,
        bandeja,
        output=n_arch
    )
    if __debug__:
        print('datos cifrados', str(encrypted_ascii_data))

    if encrypted_ascii_data.ok is True:
        os.remove(archivo)
    else:
        print(encrypted_ascii_data.status)


def traer_del_servidor():
    """Hace pull al servidor repo"""
    return subprocess.run([
        'git',
        'pull',
    ], check=False)


def subir_al_servidor():
    """Hace Push al servidor repo"""
    return subprocess.run([
        'git',
        'push',
    ], check=False)


def hacer_commit():
    """Añade archivos y crea el commit"""
    subprocess.run([
        'git',
        'add',
        '.',
    ], check=False)

    return subprocess.run([
        'git',
        'commit',
        '--allow-empty-message',
        '-m',
        '',
    ], check=False)
