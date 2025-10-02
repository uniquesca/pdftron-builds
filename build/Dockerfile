# -------- Build args (choose at build time) --------
ARG UBI_MAJOR=9          # 8 or 9
ARG PHP_VER=83           # 81, 82, 83, 84, 85
ARG PDFTRON_SDK_URL=http://www.pdftron.com/downloads/PDFNetC64.tar.gz
ARG WRAPPERS_REF=master
ARG SWIG_VERSION=4.1.1

# Base depends on UBI_MAJOR
FROM registry.access.redhat.com/ubi${UBI_MAJOR}/ubi AS builder

# Re-declare args in-stage if we want to echo them, etc. (not strictly needed)
ARG PHP_VER
ARG PDFTRON_SDK_URL
ARG WRAPPERS_REF
ARG SWIG_VERSION

USER 0

# Base toolchain + EPEL/Remi (detect OS major from /etc/os-release to avoid unbound var)
RUN set -eux; \
  . /etc/os-release; \
  os_major="${VERSION_ID%%.*}"; \
  dnf -y update || true; \
  dnf -y install dnf-plugins-core wget git cmake make gcc gcc-c++ which tar \
                 openssl-devel zlib-devel libtool autoconf automake \
                 ca-certificates || true; \
  (dnf -y install pcre2-devel || dnf -y install libpcre2-devel || true); \
  rpm -Uvh --nodigest --nofiledigest \
    "https://dl.fedoraproject.org/pub/epel/epel-release-latest-${os_major}.noarch.rpm" || true; \
  rpm -Uvh --nodigest --nofiledigest \
    "https://rpms.remirepo.net/enterprise/remi-release-${os_major}.rpm" || true; \
  dnf clean all || true

# Install chosen Remi PHP version (NTS). For ZTS, swap to php${PHP_VER}-php-zts + matching devel.
RUN set -eux; \
  dnf -y install \
    php${PHP_VER}-php-cli \
    php${PHP_VER}-php-devel \
    php${PHP_VER}-php-json \
    php${PHP_VER}-php-mbstring; \
  dnf clean all || true

# Put Remi's PHP first on PATH so php/php-config point to the selected version
ENV REMI_ROOT=/opt/remi/php${PHP_VER}/root
ENV PATH="${REMI_ROOT}/usr/bin:${PATH}"
RUN ln -sf "${REMI_ROOT}/usr/bin/php" /usr/bin/php && ln -sf "${REMI_ROOT}/usr/bin/php-config" /usr/bin/php-config

# Build SWIG
WORKDIR /opt/build
RUN wget "https://prdownloads.sourceforge.net/swig/swig-${SWIG_VERSION}.tar.gz" && \
    tar xzf "swig-${SWIG_VERSION}.tar.gz" && \
    cd "swig-${SWIG_VERSION}" && \
    ./configure && make -j"$(nproc)" && make install && ldconfig && swig -version

# Clone Apryse wrappers
WORKDIR /opt
RUN git clone --depth=1 --branch "${WRAPPERS_REF}" https://github.com/ApryseSDK/PDFNetWrappers.git /opt/PDFTron/PDFNetWrappers

# Drop Apryse C/C++ SDK under PDFNetC/
WORKDIR /opt/PDFTron/PDFNetWrappers/PDFNetC
RUN wget -O PDFNetC64.tar.gz "${PDFTRON_SDK_URL}" && \
    tar xzf PDFNetC64.tar.gz && \
    if [ -d PDFNetC64/Headers ] && [ -d PDFNetC64/Lib ]; then \
      mv PDFNetC64/Headers ./Headers && mv PDFNetC64/Lib ./Lib; \
    else \
      find . -maxdepth 2 -type d -name Headers -exec bash -lc 'src=$(dirname {}) && cp -r "$src/Headers" ./Headers && cp -r "$src/Lib" ./Lib' \;; \
    fi && \
    rm -rf PDFNetC64 PDFNetC64.tar.gz

# Build PHP wrapper
WORKDIR /opt/PDFTron/PDFNetWrappers
RUN cmake -S . -B Build -D BUILD_PDFNetPHP=ON && \
    cmake --build Build -j"$(nproc)" && \
    cmake --install Build

# Collect artifacts at image root (clean export)
RUN set -eux; \
  cp /opt/PDFTron/PDFNetWrappers/PDFNetC/Lib/libPDFNetC.so /libPDFNetC.so; \
  EXT_DIR="$(php-config --extension-dir || true)"; \
  if [ -n "$EXT_DIR" ] && [ -f "$EXT_DIR/PDFNetPHP.so" ]; then \
    cp "$EXT_DIR/PDFNetPHP.so" /PDFNetPHP.so; \
  elif [ -f /opt/PDFTron/PDFNetWrappers/PDFNetC/Lib/PDFNetPHP.so ]; then \
    cp /opt/PDFTron/PDFNetWrappers/PDFNetC/Lib/PDFNetPHP.so /PDFNetPHP.so; \
  else \
    echo "ERROR: PDFNetPHP.so not found" >&2; exit 2; \
  fi; \
  ls -l /

# Final stage exposes just the two files
FROM scratch AS artifact
COPY --from=builder /libPDFNetC.so /PDFNetPHP.so /
