# PDFTron Builds
This repo contains builds of PDFTron for various PHP versions.


## Available builds

| OS           | PHP versions       |
|--------------|--------------------|
| CentOS 7.9   | 8.1                |
| RedHat 8     | 8.2, 8.3, 8.4      |
| RedHat 9     | 8.2, 8.3, 8.4      |
| Ubuntu 16.04 | 5.6                |
| Ubuntu 18.04 | 5.6                |
| Ubuntu 22.04 | 8.1, 8.2, 8.3, 8.4 |
| Ubuntu 24.04 | 8.2, 8.3, 8.4      |

All builds are NTS (non-thread-safe). `install.sh` supports the Ubuntu builds only;
for RedHat/CentOS install manually (see below).


## Install
Run install.sh script being root or install manually. 
Script usage:
```bash
# Usage: sudo ./install.sh UBUNTU_VERSION PHP_VERSION PHP_CONFIG_PATH PDFNETC_LINK_PATH
# Arguments:
#   UBUNTU_VERSION: should be 16.04, 18.04, 22.04 or 24.04
#   PHP_VERSION: should be 5.6, 8.1, 8.2, 8.3 or 8.4 (see "Available builds" above)
#   PHP_CONFIG_PATH: path to PHP configuration folder. 
#       In Debian-based systems it's usually /etc/php/mods-available/ or /etc/php/PHP_VERSION/mods-available. 
#       If skipped, /etc/php/PHP_VERSION/mods-available/ will be used.
#   PDFNETC_LINK_PATH: path to put link for the libPDFNetC library.
#       If skipped, /usr/lib will be used.
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


### Examples:
#### Ubuntu 16 (php 5.6):
Files were copied to `/usr/lib/php/20131226/` directory.
Apache's and cli configs were updated by adding `extension=/usr/lib/php/20131226/PDFNetPHP.so`
And `ln -s /usr/lib/php/20131226/libPDFNetC.so /usr/lib/libPDFNetC.so` was run to create a symlink.

#### Redhat Enterprise Linux 8.7 (php 8.1):
1. Files were copied to:  
   `/usr/lib64/php/modules/PDFNetPHP.so`  
   and  
   `/usr/lib64/libPDFNetC.so`
2. Created a file /etc/php.d/pdfnetphp.ini with such content:  
   `extension=/usr/lib64/php/modules/PDFNetPHP.so`
3. Restart apache or php-fpm


### To test manually
Run `php test.php` (in the test dir), as a result -> `result.pdf` should be created in the `test_files` subdirectory.

### To install for php-fpm:
The example below is for PHP 8.2 from Remi. For PHP 8.3 or 8.4 replace `8.2` with `8.3`/`8.4`
and `php82` with `php83`/`php84`.

1. `sudo mkdir -p /opt/pdftron/php-8.2`  
`sudo cp /path/to/PDFNetPHP.so /opt/pdftron/php-8.2/`  
`sudo cp /path/to/libPDFNetC.so /opt/pdftron/php-8.2/`   
`sudo chown -R root:root /opt/pdftron/php-8.2`  
`sudo chmod 0755 /opt/pdftron/php-8.2`
`sudo tee /etc/opt/remi/php82/php.d/50-pdftron.ini >/dev/null <<'EOF'`  
`; PDFTron for PHP 8.2`  
`extension=/opt/pdftron/php-8.2/PDFNetPHP.so`  
`EOF`

2. Edit /etc/opt/remi/php82/php-fpm.d/www.conf and set (or confirm) these:  
`user = apache`  
`group = apache`
`; Use a UNIX socket (recommended)`  
`listen = /var/opt/remi/php82/run/php-fpm/www.sock`  
`listen.mode = 0660`  

3. `sudo mkdir -p /etc/systemd/system/php82-php-fpm.service.d`  
`sudo tee /etc/systemd/system/php82-php-fpm.service.d/override.conf >/dev/null <<'EOF'`  
`[Service]`  
`Environment=LD_LIBRARY_PATH=/opt/pdftron/php-8.2`  
`EOF`
`sudo systemctl daemon-reload`  
`sudo systemctl restart php82-php-fpm`

### To update for php-fpm:
`sudo cp /path/to/PDFNetPHP.so /opt/pdftron/php-8.2/`  
`sudo cp /path/to/libPDFNetC.so /opt/pdftron/php-8.2/`  
`sudo chown -R root:root /opt/pdftron/php-8.2`  
`sudo chmod 0755 /opt/pdftron/php-8.2`  
`sudo systemctl restart php82-php-fpm`

### To test in CI

Set the `PDFTRON_LICENSE_KEY` environment variable to your license key and run `php test.php` (in the test dir), as a result -> `result.pdf` should be created in the `test_files` subdirectory.