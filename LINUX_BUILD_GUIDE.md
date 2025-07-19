# EyeBrowserOS Linux Build Guide

## Overview

EyeBrowserOS (formerly Nxtscape) is an open-source, privacy-first browser with built-in AI capabilities. It's built on top of Chromium with custom patches that add AI agents, local chat functionality, and enhanced productivity features.

## Project Structure Analysis

### Core Components

- **Build System**: Sophisticated Python-based build orchestrator in `build/` directory
- **Patches**: Git patches in `patches/nxtscape/` that modify Chromium source
- **Resources**: AI extensions and browser assets in `resources/`
- **Chromium Integration**: Uses Chromium 137.0.7151.69 as the base

### Key Features Added via Patches

1. **Branding**: Renames Chromium to EyeBrowserOS throughout the codebase
2. **AI Chat Extension**: Built-in AI side panel with local model support
3. **Bug Reporter**: Integrated feedback system
4. **Enhanced Settings**: Custom settings UI for AI configuration
5. **Productivity Tools**: Agent automation capabilities

## Prerequisites

### System Requirements

- **Operating System**: Ubuntu 20.04+, Debian 11+, or Fedora 35+
- **Python**: Version 3.8 or higher
- **Git**: Latest version
- **Storage**: ~150GB free disk space (100GB for Chromium + 50GB for build artifacts)
- **RAM**: 16GB+ recommended (8GB minimum)
- **CPU**: Multi-core processor (build takes 2-4 hours)

### Required Tools

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip git curl build-essential

# Fedora
sudo dnf install python3 python3-pip git curl gcc-c++ make
```

## Step-by-Step Build Instructions

### 1. Install Chromium Build Tools

```bash
# Create a dedicated directory for the build
mkdir -p ~/browseros-build
cd ~/browseros-build

# Install depot_tools (Chromium's build tools)
git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
export PATH="$PWD/depot_tools:$PATH"
echo 'export PATH="$HOME/browseros-build/depot_tools:$PATH"' >> ~/.bashrc
```

### 2. Download Chromium Source

```bash
# Create Chromium source directory
mkdir chromium && cd chromium

# Initialize gclient
gclient config --name=src https://chromium.googlesource.com/chromium/src.git

# Sync to the exact version used by EyeBrowserOS (137.0.7151.69)
gclient sync --revision=137.0.7151.69

# This will take 30-60 minutes and download ~20GB
```

### 3. Install Build Dependencies

```bash
cd src

# Install Chromium build dependencies
./build/install-build-deps.sh

# Configure for Linux build
gn gen out/Default_x64 --args='is_debug=false target_cpu="x64"'
```

### 4. Clone and Setup EyeBrowserOS

```bash
# Go back to build directory
cd ~/browseros-build

# Clone EyeBrowserOS repository
git clone https://github.com/Arcane-Fly/EyeBrowserOS.git
cd EyeBrowserOS

# Install Python dependencies
pip3 install -r requirements.txt
```

### 5. Build EyeBrowserOS

```bash
# Build with patches, compilation, and packaging
python3 build/build.py \
    --chromium-src ~/browseros-build/chromium/src \
    --arch x64 \
    --build-type release \
    --apply-patches \
    --build \
    --package
```

### Build Options Explained

- `--chromium-src`: Path to Chromium source directory
- `--arch`: Target architecture (`x64` or `arm64`)
- `--build-type`: `debug` or `release`
- `--apply-patches`: Apply EyeBrowserOS modifications to Chromium
- `--build`: Compile the browser
- `--package`: Create Linux packages

## Package Formats

The build system creates multiple Linux package formats:

### 1. Tarball (.tar.gz)

- **Location**: `dist/EyeBrowserOS_<version>_<arch>_linux.tar.gz`
- **Installation**: Extract and run

```bash
tar -xzf EyeBrowserOS_*_linux.tar.gz
cd EyeBrowserOS
./browseros
```

### 2. DEB Package (.deb)

- **Location**: `dist/browseros_<version>_<arch>.deb`
- **Installation**: System package manager

```bash
sudo dpkg -i browseros_*.deb
browseros  # Launch from terminal or applications menu
```

### 3. AppImage (Future)

- Portable application format
- Single-file distribution

## Package Contents

Each package includes:

- **Main binary**: `chrome` (renamed to `browseros` in launcher)
- **Resources**: Localization files, GPU acceleration libraries
- **Extensions**: Built-in AI chat and bug reporter
- **Desktop integration**: `.desktop` file for menu entries
- **Launch script**: Wrapper script for easy execution

## Troubleshooting

### Common Build Issues

1. **Insufficient Disk Space**

   ```bash
   df -h  # Check available space
   # Need ~150GB total
   ```

2. **Missing Dependencies**

   ```bash
   # Re-run dependency installation
   cd chromium/src
   ./build/install-build-deps.sh
   ```

3. **Git Apply Failures**

   ```bash
   # Clean chromium source and re-sync
   cd chromium/src
   git clean -fd
   git reset --hard
   gclient sync --revision=137.0.7151.69
   ```

4. **Build Compilation Errors**

   ```bash
   # Check system resources
   free -h  # Ensure sufficient RAM
   nproc    # Check CPU cores for parallel building
   ```

### Performance Optimization

```bash
# Use all CPU cores for faster building
export GN_NUM_THREADS=$(nproc)

# Increase build parallelism
python3 build/build.py --chromium-src /path/to/src --build-args 'use_jumbo_build=true'
```

## Development Workflow

### Patch Development

```bash
# Make changes to Chromium source
cd chromium/src
# ... edit files ...

# Generate new patch
git diff > ../../EyeBrowserOS/patches/nxtscape/my-feature.patch

# Add to series file
echo "nxtscape/my-feature.patch" >> ../../EyeBrowserOS/patches/series
```

### Incremental Builds

```bash
# After making changes, rebuild quickly
python3 build/build.py \
    --chromium-src ~/browseros-build/chromium/src \
    --build  # Skip patches if already applied
```

## Advanced Configuration

### Build Arguments

The build system supports GN arguments for customization:

```bash
# Debug build with symbols
--build-type debug

# Enable proprietary codecs
--build-args 'proprietary_codecs=true ffmpeg_branding="Chrome"'

# Custom optimization
--build-args 'is_official_build=true optimize_for_size=true'
```

### Cross-Compilation

```bash
# Build for ARM64 on x64 host
--arch arm64 --build-args 'target_cpu="arm64"'
```

## Version Management

- **Chromium Version**: Defined in `CHROMIUM_VERSION` (137.0.7151.69)
- **EyeBrowserOS Version**: Defined in `build/config/NXTSCAPE_VERSION` (29)
- **Final Version**: Combines both as 137.0.7180.69 (7151 + 29 = 7180)

## File Locations

```
~/browseros-build/
├── depot_tools/          # Chromium build tools
├── chromium/src/         # Chromium source code
├── EyeBrowserOS/            # EyeBrowserOS build system and patches
└── dist/                 # Final packages
```

## Next Steps

1. **Test Installation**: Verify the packaged browser works correctly
2. **Extension Development**: Add custom AI agents or productivity tools
3. **Patch Contribution**: Submit improvements back to the project
4. **Automation**: Set up CI/CD for automated builds

## Support

- **Discord**: [Join the community](https://discord.gg/YKwjt5vuKr)
- **GitHub Issues**: Report bugs and request features
- **Documentation**: Check `docs/BUILD.md` for additional details

---

This build guide provides a complete pathway from system setup to running EyeBrowserOS on Linux. The modular build system makes it straightforward to customize, extend, and contribute to this privacy-focused, AI-enhanced browser.
