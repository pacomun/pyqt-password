## arg 1:  the new package version
post_install() {
    update-desktop-database /usr/share/applications
    echo "Se actualizo la base de datos"
}
