# Build Apryse/PDFTron PHP extension (RHEL/UBI 8 & 9, PHP 8.1–8.5 via Remi, NTS)

This Dockerfile builds the two runtime artifacts for Apryse/PDFTron’s PHP wrapper:
 - libPDFNetC.so
 - PDFNetPHP.so

## Parameters
 - `UBI_MAJOR` - 8 or 9 (build on RHEL/UBI 8 or 9 userspace)
 - `PHP_VER` - 81 | 82 | 83 | 84 | 85 (PHP version to target)
 
> Output files are written using --output type=local,dest=...  
> E.g. `dest=redhat9-php84` - name of the directory, where the generated libPDFNetC.so and PDFNetPHP.so will be saved to

# Examples

## RedHat 9
    docker buildx build --no-cache --build-arg UBI_MAJOR=9 --build-arg PHP_VER=85 --target artifact --output type=local,dest=redhat9-php85 .  
    docker buildx build --no-cache --build-arg UBI_MAJOR=9 --build-arg PHP_VER=84 --target artifact --output type=local,dest=redhat9-php84 .  
    docker buildx build --no-cache --build-arg UBI_MAJOR=9 --build-arg PHP_VER=83 --target artifact --output type=local,dest=redhat9-php83 .  
    docker buildx build --no-cache --build-arg UBI_MAJOR=9 --build-arg PHP_VER=82 --target artifact --output type=local,dest=redhat9-php82 .  
    docker buildx build --no-cache --build-arg UBI_MAJOR=9 --build-arg PHP_VER=81 --target artifact --output type=local,dest=redhat9-php81 .  

## RedHat 8
    docker buildx build --no-cache --build-arg UBI_MAJOR=8 --build-arg PHP_VER=85 --target artifact --output type=local,dest=redhat8-php85 .  
    docker buildx build --no-cache --build-arg UBI_MAJOR=8 --build-arg PHP_VER=84 --target artifact --output type=local,dest=redhat8-php84 .  
    docker buildx build --no-cache --build-arg UBI_MAJOR=8 --build-arg PHP_VER=83 --target artifact --output type=local,dest=redhat8-php83 .  
    docker buildx build --no-cache --build-arg UBI_MAJOR=8 --build-arg PHP_VER=82 --target artifact --output type=local,dest=redhat8-php82 .  
    docker buildx build --no-cache --build-arg UBI_MAJOR=8 --build-arg PHP_VER=81 --target artifact --output type=local,dest=redhat8-php81 .  


# Notes
 - Thread safety: Builds NTS by default.
 - Non-Remi runtime: These .so files will work with non-Remi PHP on the same OS major if ABI matches (same PHP minor, NTS/ZTS, non-debug).