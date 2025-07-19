# BrowserOS AI Coding Agent Instructions

## Project Overview
BrowserOS is a Chromium-based browser with AI superpowers, offering local AI agents and privacy-first browsing. The build system creates customized Chromium builds with BrowserOS-specific patches, branding, and AI extensions.

## Architecture & Build System

### Core Components
- **`build/build.py`**: Main orchestrator supporting multi-architecture builds, signing, and packaging
- **`build/modules/`**: Modular build steps (patches, compilation, packaging, signing)
- **`build/context.py`**: BuildContext dataclass holding all build state and paths
- **`patches/`**: Chromium modifications for AI features and BrowserOS branding
- **`chromium_src/`**: File replacements that override default Chromium files
- **`resources/`**: Assets, icons, and extensions bundled with the browser

### Build Process Flow
1. **Git Setup**: Checkout specific Chromium version from `CHROMIUM_VERSION`
2. **File Replacement**: Replace Chromium files with custom versions from `chromium_src/`
3. **String Replacement**: Apply branding changes via regex patterns
4. **Patch Application**: Apply `.patch` files from `patches/nxtscape/` (controlled by `patches/series`)
5. **Resource Copy**: Bundle extensions and assets
6. **Configuration**: Generate GN build files with platform-specific flags
7. **Compilation**: Build with `autoninja` using optimized parallel jobs
8. **Packaging**: Create platform packages (DMG, MSI, .tar.gz, .deb, AppImage)

## Key Patterns & Conventions

### Build Configuration
- **GN Flags**: Platform/build-type specific in `build/config/gn/flags.{platform}.{type}.gn`
- **Build Types**: `debug` (fast builds) vs `release` (optimized, official)
- **Multi-arch**: Use `architectures: [arm64, x64]` + `universal: true` for universal binaries
- **Configuration Files**: YAML configs in `build/config/` override CLI parameters

### File Organization
- **Build-specific variants**: Add `.debug` or `.release` suffix to files in `chromium_src/`
- **Platform conditionals**: Use `IS_MACOS`, `IS_WINDOWS`, `IS_LINUX` checks throughout
- **Modular structure**: Each build step is a separate module with consistent interfaces

### Error Handling & Logging
- Use `log_info()`, `log_error()`, `log_success()`, `log_warning()` from `utils.py`
- Always return boolean success/failure from module functions
- Fail fast with descriptive error messages for missing dependencies

## Critical Commands & Workflows

### Basic Build Commands
```bash
# Quick debug build (Linux)
python3 build/build.py --build --chromium-src /path/to/chromium/src --arch x64

# Full release build with packaging
python3 build/build.py --config build/config/release.yaml --chromium-src /path/to/chromium/src

# Universal binary (macOS)
python3 build/build.py --config build/config/release.yaml --chromium-src /path/to/chromium/src
```

### Development Workflows
```bash
# Add new file to replacements
python3 build/build.py --add-replace /path/to/chromium/file.cc --chromium-src /path/to/chromium/src

# Apply only string replacements
python3 build/build.py --string-replace --chromium-src /path/to/chromium/src

# Interactive patch application
python3 build/build.py --apply-patches --patch-interactive --chromium-src /path/to/chromium/src

# Merge two architecture builds
python3 build/build.py --merge app1.app app2.app --chromium-src /path/to/chromium/src
```

### Linux-Specific Setup
1. **Environment**: Use Python virtual environment (`browseros-env/`)
2. **Dependencies**: Install build tools, use custom pkg-config wrapper
3. **Chromium Setup**: Run `minimal-chromium-setup.sh` for development builds
4. **DRI Workaround**: `use_dri = false` in GN flags for compatibility

## Integration Points

### Chromium Integration
- **Version Pinning**: `CHROMIUM_VERSION` file specifies exact Chromium tag
- **Patch Management**: Patches in `patches/series` are applied in order
- **Build Variants**: Support debug vs release with different optimizations
- **File Overrides**: Files in `chromium_src/` completely replace Chromium originals

### Platform-Specific Details
- **macOS**: Sparkle updater, code signing, DMG packaging
- **Windows**: MSI packaging, Windows-specific signing
- **Linux**: Multiple formats (.tar.gz, .deb, AppImage), system library preferences

### AI Extensions
- **Side Panel AI**: Located in `resources/files/ai_side_panel/`
- **Bug Reporter**: Located in `resources/files/bug_reporter/`
- **Pinned Extensions**: Auto-pinned via patches for AI chat and agents

## Common Issues & Solutions

### Build Failures
- **Missing Chromium**: Ensure `--chromium-src` points to valid Chromium source
- **GN Flag Errors**: Check `build/config/gn/flags.{platform}.{type}.gn` for syntax
- **Patch Conflicts**: Use `--patch-interactive` to resolve conflicts manually
- **Missing Dependencies**: Install depot_tools, ensure Python environment active

### Linux-Specific Issues
- **DRI Dependencies**: Use `use_dri = false` and custom `dri.pc` file
- **System Libraries**: Prefer bundled versions to avoid conflicts
- **Packaging Tools**: Optional .deb/.AppImage require specific tools installed

### Development Tips
- **Fast Iteration**: Use debug builds during development
- **Clean Builds**: Use `--clean` flag when switching architectures
- **Parallel Builds**: Build system auto-detects CPU count for optimal parallelism
- **Config Files**: Use YAML configs instead of long CLI commands

## File Change Patterns

When modifying the build system:
1. **Add new modules** to `build/modules/` with consistent interface
2. **Update BuildContext** in `context.py` for new build parameters  
3. **Add platform checks** using utility functions from `utils.py`
4. **Follow error handling** patterns with proper logging
5. **Test across platforms** especially for cross-platform modules
