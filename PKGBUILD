pkgname=coursia
pkgver=0.5
pkgrel=1

pkgdesc="Enregistrement, transcription et révision universitaire avec Mistral AI"

arch=('x86_64')

url="https://github.com/Dofyx/CoursAI"

license=('CCPL')

depends=(
    'python'
    'python-pip'
    'portaudio'
)

source=()

sha256sums=()

package() {

    install -dm755 "$pkgdir/opt/coursia"

    cp -r "$startdir/source/"* \
          "$pkgdir/opt/coursia/"

    install -Dm755 \
        "$startdir/coursia.sh" \
        "$pkgdir/usr/bin/coursia"

    install -Dm644 \
        "$startdir/coursia.desktop" \
        "$pkgdir/usr/share/applications/coursia.desktop"

    install -Dm644 \
        "$startdir/source/assets/logo_icon_256.png" \
        "$pkgdir/usr/share/icons/hicolor/256x256/apps/coursia.png"
}
