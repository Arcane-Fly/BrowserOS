#!/bin/bash
# Build wrapper for BrowserOS on Linux

# Set environment variables
export PATH="$PWD:$PWD/depot_tools:$PATH"

# Use our custom pkg-config wrapper
export PKG_CONFIG="$PWD/custom-pkg-config.sh"

# Activate Python virtual environment
if [ -f "browseros-env/bin/activate" ]; then
    source browseros-env/bin/activate
fi

# Run the build script with the correct parameters
python3 build/build.py --build --package --chromium-src /home/braden/chromium-minimal/src --arch x64 "$@"
