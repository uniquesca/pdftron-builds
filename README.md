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
