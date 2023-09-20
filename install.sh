#!/usr/bin/env bash

# Installation script for PDFTron in the system.
# Has to be executed by the user with admin rights (sudo user)
# Usage: sudo ./install.sh UBUNTU_VERSION PHP_VERSION PHP_CONFIG_PATH PDFNETC_LINK_PATH
# Arguments:
#   UBUNTU_VERSION: should be 16.04 or 18.04 or 22.04
#   PHP_VERSION: should be 5.6 or 8.1
#   PHP_CONFIG_PATH: path to PHP configuration folder, in Debian-based systems it's
#       usually /etc/php/ or /etc/php/PHP_VERSION/. If skipped, /etc/php/PHP_VERSION
#       will be used.
#   PDFNETC_LINK_PATH: path to put link for the libPDFNetC library.
#       If skipped, /usr/lib will be used.


if [ "$EUID" -ne 0 ]
  then echo "Please run this script as root"
  exit
fi

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

TARGET_FOLDER="$SCRIPT_DIR/ubuntu-$1/php-$2"

if [ ! -d "$TARGET_FOLDER" ]; then
  echo "$TARGET_FOLDER does not exist, choose either another OS version, or another PHP version."
  exit 2
fi

PDFNETSO="$TARGET_FOLDER/PDFNetPHP.so"
LIBSO="$TARGET_FOLDER/libPDFNetC.so"

echo "Installing PDFNetPHP from $TARGET_FOLDER...";

if [ -z "$3" ]
then
      PHP_CONFIG_PATH="/etc/php/$2/"
else
      PHP_CONFIG_PATH=$3
fi

if [ ! -d "$PHP_CONFIG_PATH" ]; then
  echo "$PHP_CONFIG_PATH does not exist, specify proper path to the php config folder."
  exit 2
fi

EXTENSION_INI="${PHP_CONFIG_PATH%/}/mods-available/pdfnetphp.ini"

# Register extension
echo "extension=$PDFNETSO" > "$EXTENSION_INI"
echo "Module registered in $EXTENSION_INI"

# Enable the module for CLI
ln -sf $EXTENSION_INI "${PHP_CONFIG_PATH%/}/cli/conf.d/20-pdfnetphp.ini"
echo "> Module enabled for CLI in ${PHP_CONFIG_PATH%/}/cli/conf.d/20-pdfnetphp.ini"

ln -sf $EXTENSION_INI "${PHP_CONFIG_PATH%/}/apache2/conf.d/20-pdfnetphp.ini"
echo "> Module enabled for Apache in ${PHP_CONFIG_PATH%/}/apache2/conf.d/20-pdfnetphp.ini"

if [ -z "$4" ]
then
      PDFNETC_LINK_PATH="/usr/lib/"
else
      PDFNETC_LINK_PATH=$4
fi

if [ ! -d "$PDFNETC_LINK_PATH" ]; then
  echo "$PDFNETC_LINK_PATH does not exist, specify proper path to the library folder."
  exit 2
fi

ln -sf $LIBSO "${PDFNETC_LINK_PATH%/}/"
echo "> Created link for libPDFNetC in $PDFNETC_LINK_PATH"

echo "Installation complete!"

