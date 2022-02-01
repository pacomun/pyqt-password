"""Llamadas a sistema para ejecutar comandos de Git.

"""

import secrets
import os
import string
import subprocess


class  ErrorStore(Exception):
    """Excepción para almacén no encontrado."""
    def __init__(self):
        Exception.__init__(self)

        print('El almacén no se podido encontrar...')


def almacen_get():
    """Devuelve la ruta al almacén de contraseñas."""
    HOME = os.environ.get('HOME')
    if os.path.exists(HOME + '/password-store') is True:
        almacen = HOME + '/password-store'
    elif os.path.exists(HOME + '/.password-store') is True:
        almacen = HOME + '/.password-store'
    else:
        raise ErrorStore()
    return almacen


def generador(ndigit=8):
    """ Generar contraseña segura de n-digitos."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(ndigit))


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



if __name__ == '__main__':
    contrasegna = generador(12)
    os.chdir('/tmp/gitejemplo')

    print(contrasegna)
    print('La ruta al almacén de contraseñas es: ',
          almacen_get())
    salida = traer_del_servidor()
    print(salida.returncode)
    print(salida.stdout)

    salida = hacer_commit()
    print(salida.returncode)
    print(salida.stdout)

    salida = subir_al_servidor()
    print(salida.returncode)
    print(salida.stdout)
