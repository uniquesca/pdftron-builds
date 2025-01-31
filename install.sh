#!/bin/bash

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
#   SO_TARGET_FOLDER: path to where so files will be located. If skipped,
#       the script will use paths from within this repo.
# Note: this scripts created PHP config file, but doesn't create links (it used to). For Ubuntu
# it might be necessary to created the links manually, i.e.
# $> ln -s /etc/php/8.2/mods-available/pdfnetphp.ini /etc/php/8.2/cli/conf.d/20-pdfnetphp.ini
# $> ln -s /etc/php/8.2/mods-available/pdfnetphp.ini /etc/php/8.2/apache2/conf.d/20-pdfnetphp.ini

if [ "$EUID" -ne 0 ]; then
  echo "Please run this script as root"
  exit
fi

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

SO_SOURCE_FOLDER="$SCRIPT_DIR/ubuntu-$1/php-$2"

if [ ! -d "$SO_SOURCE_FOLDER" ]; then
  echo "$SO_SOURCE_FOLDER does not exist, choose either another OS version, or another PHP version."
  exit 2
fi

PDFNETSO="$SO_SOURCE_FOLDER/PDFNetPHP.so"
LIBSO="$SO_SOURCE_FOLDER/libPDFNetC.so"

echo "Installing PDFNetPHP from $SO_SOURCE_FOLDER...";

if [ -z "$3" ]
then
      PHP_CONFIG_PATH="/etc/php/$2/mods-available"
else
      PHP_CONFIG_PATH=$3
fi

if [ -n "$4" ]
then
  echo "Target folder: $4"
  # Moving .so files into specified directory
  cp "$PDFNETSO" "$4"
  cp "$LIBSO" "$4"
  PDFNETSO="$4/PDFNetPHP.so"
  LIBSO="$4/libPDFNetC.so"
else
  echo "Target folder: $SO_SOURCE_FOLDER"
fi

if [ ! -d "$PHP_CONFIG_PATH" ]; then
  echo "$PHP_CONFIG_PATH does not exist, specify proper path to the php config folder."
  exit 2
fi

EXTENSION_INI="${PHP_CONFIG_PATH%/}/pdfnetphp.ini"

# Register extension
echo "extension=$PDFNETSO" > "$EXTENSION_INI"
echo "Module registered in $EXTENSION_INI"

# Enable the module for CLI
echo "> Skipping creating links for the PHP config file, please do it manually if necessary."
# ln -sf $EXTENSION_INI "${PHP_CONFIG_PATH%/}/cli/conf.d/20-pdfnetphp.ini"
# echo "> Module enabled for CLI in ${PHP_CONFIG_PATH%/}/cli/conf.d/20-pdfnetphp.ini"

# ln -sf $EXTENSION_INI "${PHP_CONFIG_PATH%/}/apache2/conf.d/20-pdfnetphp.ini"
# echo "> Module enabled for Apache in ${PHP_CONFIG_PATH%/}/apache2/conf.d/20-pdfnetphp.ini"

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

