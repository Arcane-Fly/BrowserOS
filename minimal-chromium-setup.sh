#!/bin/bash
# Minimal Chromium Setup for BrowserOS
# This script sets up a minimal Chromium build environment

set -e  # Exit immediately if a command exits with a non-zero status

# Configuration
CHROMIUM_DIR=~/chromium-minimal

echo "🔧 Setting up minimal Chromium build environment in $CHROMIUM_DIR..."

# Clean up previous attempts if they exist
if [ -d "$CHROMIUM_DIR" ]; then
    echo "🧹 Removing existing Chromium directory..."
    rm -rf "$CHROMIUM_DIR"
fi

# Create fresh directory
mkdir -p "$CHROMIUM_DIR"
cd "$CHROMIUM_DIR"

# Set up depot_tools
echo "📥 Installing depot_tools..."
if [ ! -d "depot_tools" ]; then
    git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
else
    echo "✅ depot_tools already exists, skipping clone"
fi

export PATH="$PWD/depot_tools:$PATH"

# Check Chromium version compatibility with BrowserOS
echo "🔍 Checking Chromium version compatibility..."
CHROMIUM_VERSION=$(grep -oP 'CHROMIUM_VERSION ?= ?"\K[^"]+' /home/braden/Desktop/Dev/BrowserOS/build/config/version.gni 2>/dev/null || echo "UNKNOWN")
if [ "$CHROMIUM_VERSION" == "UNKNOWN" ]; then
    echo "⚠️  Could not determine required Chromium version from BrowserOS build config"
    CHROMIUM_VERSION="latest"
fi
echo "BrowserOS expects Chromium version: $CHROMIUM_VERSION"

echo "📦 This will download ~20-30GB (much less than full 100GB)"
read -p "Continue? (y/N) " response
if [[ "$response" =~ ^[Yy]$ ]]; then
    echo "🚀 Starting minimal Chromium sync..."
    
    # Configure git for better handling of large repos
    git config --global core.preloadIndex true
    git config --global core.fscache true
    git config --global gc.auto 256
    
    # Fetch the minimal Chromium source
    fetch --nohooks --no-history chromium
    
    # Navigate to src directory
    cd src
    
    # Run hooks to generate necessary files
    echo "🔄 Running hooks to generate build files..."
    gclient runhooks
    
    # Generate build files
    echo "⚙️  Configuring the build..."
    gn gen out/Default --args='is_debug=false enable_nacl=false is_component_build=false symbol_level=0'
    
    echo "✅ Minimal Chromium setup complete!"
    echo "📍 Chromium source location: $PWD"
    echo "🔧 To build BrowserOS:"
    echo "   1. Activate the Python virtual environment"
    echo "      cd /home/braden/Desktop/Dev/BrowserOS && source browseros-env/bin/activate"
    echo "   2. Build BrowserOS with:"
    echo "      cd /home/braden/Desktop/Dev/BrowserOS"
    echo "      python3 build/build.py --build --package --chromium-src $PWD --arch x64"
else
    echo "❌ Setup cancelled by user"
    exit 1
fi
