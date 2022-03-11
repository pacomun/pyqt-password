"""Instalador para el paquete pyqt_password"""


from setuptools import setup


long_description = (
    open("README.md").read()
    + '\n' +
    open("LICENSE").read()
    + '\n')


setup(
    name="pyqt_password",
    version='1.0',
    description='Aplicación para gestión de contraseñas',
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Gui',
        'Intended Audience :: Any',
        'License :: Apache',
        'Programming Language :: Python',
        'Programming Language :: Python 3.10 '
        'Operating System :: OS Independent'
    ],
    keywords='Gestor de contraseñas pyqt5',
    author='Francisco Muñoz Sánchez',
    author_email='pacomun.gm@gmail.com',
    url='https://github.com/pacomun/pyqt-password',
    download_url='https://github.com/pacomun/pyqt-password',
    license='Apache',
    platforms='Unix, Windows',
    packages=['pyqt_password', 'pyqt_password/helpGit'],
    include_package_data=True,
)
