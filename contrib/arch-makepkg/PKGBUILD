# Maintainer: Aleksy Grabowski <hurufu+arch@gmail.com>

pkgname=nexui-demo
pkgver=0.0.0
pkgrel=1
pkgdesc='NEXO-in-the-cloud demo'
arch=(any)
license=('custom:proprietary')
depends=(
    python-bitstruct
    python-timebudget
    python-pynng
    libsocket
    nexiod-cpp
)
source=(git+file:///srv/git/flask-nexui.git)
md5sums=('SKIP')

build() {
    cd "${srcdir}/flask-nexui"
    git submodule update --init
    python setup.py build
}

package() {
    builddir=
    cd "${srcdir}/flask-nexui"
    python setup.py install -O0 --root="$pkgdir" --skip-build
}
