#!/bin/bash

rm -rf asherah/libasherah/

wget --content-disposition --directory-prefix asherah/libasherah/  \
  https://github.com/godaddy/asherah-cobhan/releases/download/current/libasherah-arm64.dylib \
  https://github.com/godaddy/asherah-cobhan/releases/download/current/libasherah-arm64.so \
  https://github.com/godaddy/asherah-cobhan/releases/download/current/libasherah-x64.dylib \
  https://github.com/godaddy/asherah-cobhan/releases/download/current/libasherah-x64.so \
  || exit 1
