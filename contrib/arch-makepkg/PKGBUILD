# Maintainer: Aleksy Grabowski <hurufu+arch@gmail.com>

pkgname=nexui-demo
pkgver=0.0.1
pkgrel=1
pkgdesc='NEXO-in-the-cloud demo'
arch=(any)
license=('custom:proprietary')
depends=(
    python-bitstruct
    python-timebudget
    python-pynng
    libsocket
    nexoid-fat
)
makedepends=(
    git
)
source=(
    git+file:///srv/git/flask-nexui.git
    git+git://github.com/AlainCouthures/declarative4all.git
)
md5sums=(
    SKIP
    SKIP
)

build() {
    cd "$srcdir/flask-nexui"
    git submodule init
    git config submodule.'XSLTForms1.5'.url "$srcdir/declarative4all"
    git submodule update
    python setup.py build
}

package() {
    builddir=
    cd "${srcdir}/flask-nexui"
    python setup.py install -O1 --root="$pkgdir" --skip-build
}
