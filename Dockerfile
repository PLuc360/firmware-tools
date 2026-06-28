FROM debian:latest

RUN apt-get update && apt-get install -y \
    bzip2 \
    xz-utils \
    tar \
    python3 \
    uncrustify \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /configuration
RUN mkdir /binaries
RUN mkdir /tools
RUN mkdir /resources

ENV CMAKE_VERSION=4.4.0-rc2
ARG CMAKE_LINK=https://github.com/Kitware/CMake/releases/download/v${CMAKE_VERSION}/cmake-${CMAKE_VERSION}-linux-x86_64.tar.gz
RUN curl -L ${CMAKE_LINK} -o /binaries/cmake-${CMAKE_VERSION}-linux-x86_64.tar.gz

ENV GCC_ARM_VERSION=15.2.rel1
ARG GCC_ARM_LINK=https://developer.arm.com/-/media/files/downloads/gnu/${GCC_ARM_VERSION}/binrel/arm-gnu-toolchain-${GCC_ARM_VERSION}-x86_64-arm-none-eabi.tar.xz
RUN curl -L ${GCC_ARM_LINK} -o /binaries/arm-gnu-toolchain-${GCC_ARM_VERSION}-x86_64-arm-none-eabi.tar.xz

COPY ./Tools/Uncrustify/uncrustify.cfg /configuration
COPY ./Tools/Binaries/ninja /usr/bin/ninja
COPY ./Tools/script.sh /tools/script.sh
COPY ./Tools/Python /tools/Python


WORKDIR /resources
ENTRYPOINT ["/tools/script.sh"]
CMD ["lint"]