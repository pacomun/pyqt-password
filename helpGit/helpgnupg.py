"""Funciones para cifrado desdcifrado...

"""
import os
from pathlib import Path
import gnupg


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

    return None
