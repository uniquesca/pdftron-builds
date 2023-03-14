# PDFTron Builds

This repo contains builds of PDFTron for various PHP versions.

## Install

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
