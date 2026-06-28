#!/bin/bash

set -e

cmd="${1:-}"
cmd_lower="$(echo "$cmd" | tr '[:upper:]' '[:lower:]')"

# Additional args are forwarded to the selected command.
shift || true
extra_args=("$@")

if [ -z "$cmd" ]; then
    echo "Usage: $0 {build|lint} [args...]"
    echo "Example lint: $0 lint -e Code/Drivers -e Code/FreeRTOS"
    exit 1
fi

if [ "$cmd_lower" == "build" ]; then
    echo "Extracting binaries..."

    tar -xf /binaries/arm-gnu-toolchain-${GCC_ARM_VERSION}-x86_64-arm-none-eabi.tar.xz -C /usr/bin/
    tar -xf /binaries/cmake-${CMAKE_VERSION}-linux-x86_64.tar.gz -C /usr/bin/

    export PATH="/usr/bin/cmake-${CMAKE_VERSION}-linux-x86_64/bin:/usr/bin:${PATH}"

    echo "Building..."

    cmake -B build -G Ninja
    ninja -C build

elif [ "$cmd_lower" == "lint" ]; then
    echo "Linting..."
    python3 /tools/Python/check_code_style.py -i . -b /usr/bin/uncrustify -c /configuration/uncrustify.cfg --recursive "${extra_args[@]}"
elif [ "$cmd_lower" == "format" ]; then
    echo "Formatting..."
    uncrustify -c /configuration/uncrustify.cfg "${extra_args[@]}"
else
    echo "Unknown command: $cmd"
    echo "Usage: $0 {build|lint|format} [args...]"
    exit 1
fi