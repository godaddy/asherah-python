#!/bin/bash

rm -rf asherah/libasherah/

wget --content-disposition --directory-prefix asherah/libasherah/  \
  https://github.com/godaddy/asherah-cobhan/releases/download/v0.3.1/libasherah-arm64.dylib \
  https://github.com/godaddy/asherah-cobhan/releases/download/v0.3.1/libasherah-arm64.so \
  https://github.com/godaddy/asherah-cobhan/releases/download/v0.3.1/libasherah-x64.dylib \
  https://github.com/godaddy/asherah-cobhan/releases/download/v0.3.1/libasherah-x64.so \
  || exit 1
