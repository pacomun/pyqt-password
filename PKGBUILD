# Maintainer: Francisco Muñoz <pacomun.gm@gmail.com>
pkgname=pyqt-password
pkgver=1.2
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
makedepends=('git' 'python-setuptools')
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
         '2ce26e4d6f60ce0593e1fe5c137e2c49'
         '7eef4d94ad1d23ac29bea797d20b25dd')
prepare() {
    cd "$pkgname-$pkgver"
}

build() {
    cd "$pkgname-$pkgver"
    python setup.py build
}

check() {
    cd "$pkgname-$pkgver"
}

package() {
    cd "$pkgname-$pkgver"
    mkdir -p "$pkgdir"/usr/bin
    mkdir -p "$pkgdir"/usr/share/applications
    mkdir -p "$pkgdir"/usr/share/"$pkgname"
    python setup.py install --root="$pkgdir" --optimize=1
    cp ../pyqt-password.py "$pkgdir"/usr/bin
    cp ../pyqt-password.desktop "$pkgdir"/usr/share/applications
    cp LICENSE "$pkgdir"/usr/share/"$pkgname"
    cp README.md "$pkgdir"/usr/share/"$pkgname"
}
