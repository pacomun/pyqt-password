"""Módulo de funciones de ayuda.
"""

import os
from pathlib import Path
from gnupg import GPG
from configparser import ConfigParser

gpg = GPG()


def get_idkey() -> str:
    """Crea un objeto gnupg.GPG, y devuelve una cadena con e Id
    de la primera clave privada que se encuentre en el
    anillo.

    En caso de fallo levantara un Error por definir..

    """
    private_keys = gpg.list_keys(secret=True)
    return private_keys[0]['keyid']


def cfg_inicial() -> dict:
    """Crear archivo de configuración por defecto. Devuelve un
    diccionario con variables: user, editor, home,
    password_store, os, pypass_cfg, keyid

    """
    uname = os.name  # Sistema operativo

    # Consigo la variable USER
    try:
        user = os.environ['USER']
    except KeyError:
        try:
            user = os.environ['USERNAME']
        except KeyError:
            user = None

    # Busco el editor de texto.
    try:
        editor = os.environ['EDITOR']
    except KeyError:
        editor = 'notepad.exe'

    # Recogo HOME y PASSWORD_STORE
    try:
        if uname == 'nt':
            home = Path(os.environ['USERPROFILE'])
            password_store = Path(os.environ['APPDATA']).joinpath('password-store')
        elif uname == 'posix':
            home = Path(os.environ['HOME'])
            password_store = home.joinpath('.password-store')
    except KeyError:
        home = ''

    # Inicializo el depósito si no existe.
    if password_store.exists() is False:
        print('Creando depósito vacío...', password_store)
        os.mkdir(password_store)

    # Clave para cifrar y descifrar
    keyid = get_idkey()

    # Archivo de configuración.
    pypass_cfg = home.joinpath('.pypass.cfg')

    d_cfg = {'user': user, 'editor': editor, 'home': home,
             'password_store': password_store,
             'keyid': keyid, 'os': uname, 'pypass_cfg': pypass_cfg
             }

    return d_cfg


def write_cfg(seccion='info', **d_cfg) -> True:
    """Recibe un diccionario con las variables devueltas por la
    funcion 'cfg_inicial()

    Devuelve True en caso de escribir en el archivo, de lo
    contrario devuelve False.

    """
    config = ConfigParser()
    cfg_data = {seccion: d_cfg}
    config.read_dict(cfg_data)

    try:
        with open(Path(d_cfg['home']).joinpath('.pypass.cfg'),
                  'w', encoding='utf-8') as f_cfg:
            config.write(f_cfg)

    except FileNotFoundError as err:
        print('Error: No se ha escrito la configuración', err)
        return False
    return None


def read_cfg(path_cfg) -> dict:
    """Si existe el archivo de configuración carga el diccionario
    d_cfg y lo devuelve. En caso de no leer devuelve None."""
    config = ConfigParser()
    if Path(path_cfg).exists():
        config.read(path_cfg)
        d_cfg = {}
        for key, value in config['info'].items():
            d_cfg[key] = value
        return d_cfg
    return None


if __name__ == '__main__':
    d_config = cfg_inicial()
    for clave, valor in d_config.items():
        print(clave, '=', valor)

    write_cfg(**d_config)

    d_leido = read_cfg(Path(d_config['home']).joinpath('pypass.cfg'))
    for clave, valor in d_leido.items():
        print(clave, '=', valor)
