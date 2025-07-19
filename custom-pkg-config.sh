#!/bin/bash

# Custom pkg-config wrapper to handle DRI driver directory query

# DRI driver directory path
DRI_DRIVER_DIR="/usr/lib/x86_64-linux-gnu/dri"

# Check if this is the DRI driver directory query
if [[ "$*" == *"--dridriverdir"* ]]; then
    # Return the DRI driver directory
    echo "${DRI_DRIVER_DIR}"
    exit 0
fi

# For all other queries, delegate to the real pkg-config
/usr/bin/pkg-config "$@"
