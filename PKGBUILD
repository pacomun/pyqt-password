# Maintainer: Francisco Muñoz <pacomun.gm@gmail.com>
pkgname=pyqt-password
pkgver=1.1
pkgrel=0
epoch=
pkgdesc="Aplicación gui para gestion de contraseñas."
arch=('any')
url="https://github.com/pacomun/pyqt-password"
license=('GPL')
groups=()
depends=('python>=3.0'
         'python-gnupg'
         'python-qtpy'
        )
makedepends=('git')
checkdepends=()
optdepends=()
provides=()
conflicts=()
replaces=()
backup=()
options=()
install="install.sh"
changelog=
noextract=()
validpgpkeys=()
source=("$pkgname-$pkgver"::"git+https://github.com/pacomun/pyqt-password.git"
        "pyqt-password.desktop" "pyqt-password.py")
md5sums=('SKIP'
         '4b57699f5bb6362a06539832f9364339'
         'c0289b0fe512f418344280312563ee89')
prepare() {
    cd "$pkgname-$pkgver"
}

build() {
    cd "$pkgname-$pkgver"
    echo "Creando entorno virtual"
    python -m venv .Venv/
    echo "Entrando en el entorno creado"
    source .Venv/bin/activate
    echo "Instalando requisitos"
    pip install -r requirenments.txt
    echo "Desactivado el entorno"
    deactivate
	}

check() {
    cd "$pkgname-$pkgver"
}

package() {
    cd "$pkgname-$pkgver"
    mkdir -p "$pkgdir"/usr/bin
    mkdir -p "$pkgdir"/usr/share/"$pkgname"/.Venv
    mkdir -p "$pkgdir"/usr/share/applications
    cp -r .Venv/* "$pkgdir"/usr/share/"$pkgname"/.Venv
    cp -r * "$pkgdir"/usr/share/"$pkgname"
    cp ../pyqt-pass.sh "$pkgdir"/usr/bin
    cp ../pyqt-password.desktop "$pkgdir"/usr/share/applications
}
