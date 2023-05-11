# PDFTron Builds

This repo contains builds of PDFTron for various PHP versions.

## Install

Run install.sh script being root or install manually. 
Script usage:
```bash
# Usage: sudo ./install.sh UBUNTU_VERSION PHP_VERSION PHP_CONFIG_PATH
# Arguments:
#   UBUNTU_VERSION: should be 16.04 or 18.04 or 22.04
#   PHP_VERSION: should be 5.6 or 8.1
#   LIB_TARGET_PATH: path to put link for the libPDFNetC library.
#       If skipped, /usr/local/lib will be used.
#   PHP_CONFIG_PATH: path to PHP configuration folder, in Debian-based systems it's
#       usually /etc/php/ or /etc/php/PHP_VERSION/. If skipped, /etc/php/PHP_VERSION
#       will be used.
```

## Install manually

#### 1. Copy files

Copy files from the folder matching OS and PHP version to any folder on the server where PDFTron need to run.

#### 2. Register PHP extension PDFNetPHP.so

PHP extensions are enabled in different places depending on OS.

Ubuntu example:
```bash
# Register the module
sudo cat "extension=/absolute/path/to/pdfnetphpso" > /etc/php/%PHPVERSION%/mods-available/pdfnetphp.ini
# Enable the module for CLI
sudo ln -s /etc/php/%PHPVERSION%/mods-available/pdfnetphp.ini /etc/php/%PHPVERSION%/cli/conf.d/20-pdfnetphp.ini
# Enable the module for Apache
sudo ln -s /etc/php/%PHPVERSION%/mods-available/pdfnetphp.ini /etc/php/%PHPVERSION%/apache/conf.d/20-pdfnetphp.ini
```

#### 3. Register PDFNetC.so library

PHP extension PDFNetPHP.so requires dynamically loaded library PDFNetC.so, which should be discoverable by `ld`.
Therefore library has to be copied into one of the following directories:
`ld --verbose | grep SEARCH_DIR | tr -s ' ;' \\012`

Empirically known that not all the folders above will work, so different ones should be tried.
Once it's better known why not all of them work, this instruction should be updated.


### Example (Ubuntu 16, php 5.6):
Files were copied to `/usr/lib/php/20131226/` directory.
Apache's and cli configs were updated by adding `extension=/usr/lib/php/20131226/PDFNetPHP.so`
And `ln -s /usr/lib/php/20131226/libPDFNetC.so /usr/lib/libPDFNetC.so` was run to create a symlink.
