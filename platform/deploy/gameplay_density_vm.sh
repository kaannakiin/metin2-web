#!/bin/sh
set -eu
stage=${1:?candidate directory required}
case "$stage" in /usr/metin2-gameplay-[0-9]*-[0-9]*) ;; *) exit 2 ;; esac
cd "$stage"
test -f READY
test ! -e INSTALL_STARTED
test ! -e DENSITY_READY
tar -xzf density.tar.gz
sh gameplay_install_vm.sh append-density "$stage"
