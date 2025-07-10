#!/usr/bin/env python3
"""
Linux packaging module for Nxtscape Browser
Supports .tar.gz, .AppImage, and .deb package formats
"""

import os
import sys
import shutil
import tarfile
import subprocess
from pathlib import Path
from typing import Optional, List, Dict
from context import BuildContext
from utils import run_command, log_info, log_error, log_success, log_warning, join_paths, IS_LINUX


def package(ctx: BuildContext) -> bool:
    """Create Linux packages (.tar.gz, .AppImage, .deb if tools available)"""
    log_info("\n📦 Creating Linux packages...")
    
    if not IS_LINUX:
        log_warning("Linux packaging should be run on Linux for best results")
    
    success = True
    
    # Create tar.gz package (always available)
    if create_tarball(ctx):
        log_success("Tarball created successfully")
    else:
        log_error("Failed to create tarball")
        success = False
    
    # Try to create AppImage if tools are available
    if check_appimage_tools():
        if create_appimage(ctx):
            log_success("AppImage created successfully")
        else:
            log_warning("Failed to create AppImage (optional)")
    else:
        log_info("AppImage tools not available, skipping AppImage creation")
    
    # Try to create .deb if tools are available
    if check_deb_tools():
        if create_deb(ctx):
            log_success("DEB package created successfully")
        else:
            log_warning("Failed to create DEB package (optional)")
    else:
        log_info("DEB packaging tools not available, skipping DEB creation")
    
    return success


def create_tarball(ctx: BuildContext) -> bool:
    """Create .tar.gz package of the built application"""
    log_info("\n📦 Creating tarball package...")
    
    # Get paths
    build_output_dir = join_paths(ctx.chromium_src, ctx.out_dir)
    chrome_binary = build_output_dir / "chrome"
    
    if not chrome_binary.exists():
        log_error(f"Chrome binary not found at: {chrome_binary}")
        return False
    
    # Create output directory
    output_dir = ctx.root_dir / "dist"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate tarball filename with version and architecture
    tarball_name = f"{ctx.get_app_base_name()}_{ctx.get_nxtscape_version()}_{ctx.architecture}_linux.tar.gz"
    tarball_path = output_dir / tarball_name
    
    # Create a temporary directory structure for packaging
    temp_dir = ctx.root_dir / "tmp" / "linux_package"
    app_dir = temp_dir / ctx.get_app_base_name()
    
    try:
        # Clean and create temp directory
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        app_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy essential files
        log_info("Copying application files...")
        
        # Copy the main chrome binary
        shutil.copy2(chrome_binary, app_dir / "chrome")
        
        # Copy other essential files commonly needed
        essential_files = [
            "chrome_100_percent.pak",
            "chrome_200_percent.pak", 
            "resources.pak",
            "icudtl.dat",
            "chrome_crashpad_handler"
        ]
        
        for file_name in essential_files:
            src_file = build_output_dir / file_name
            if src_file.exists():
                shutil.copy2(src_file, app_dir / file_name)
                log_info(f"  Copied: {file_name}")
        
        # Copy locales directory if it exists
        locales_src = build_output_dir / "locales"
        if locales_src.exists():
            locales_dst = app_dir / "locales"
            shutil.copytree(locales_src, locales_dst)
            log_info("  Copied: locales/")
        
        # Copy swiftshader directory if it exists (GPU acceleration)
        swiftshader_src = build_output_dir / "swiftshader"
        if swiftshader_src.exists():
            swiftshader_dst = app_dir / "swiftshader"
            shutil.copytree(swiftshader_src, swiftshader_dst)
            log_info("  Copied: swiftshader/")
        
        # Create a simple launch script
        launch_script = app_dir / f"{ctx.get_app_base_name().lower()}"
        launch_script.write_text(f"""#!/bin/bash
# Nxtscape Browser launch script
SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
exec "$SCRIPT_DIR/chrome" "$@"
""")
        launch_script.chmod(0o755)
        log_info("  Created: launch script")
        
        # Create desktop file
        create_desktop_file(ctx, app_dir)
        
        # Create README
        readme_content = f"""Nxtscape Browser {ctx.get_nxtscape_version()}
==============================

Installation:
1. Extract this archive to your preferred location
2. Run './{ctx.get_app_base_name().lower()}' to start the browser
3. Optionally, install the desktop file for menu integration

For desktop integration:
  cp {ctx.get_app_base_name().lower()}.desktop ~/.local/share/applications/

System Requirements:
- Linux x86_64 or ARM64
- GTK 3.0+
- X11 or Wayland display server

Built on: {ctx.chromium_version}
Architecture: {ctx.architecture}
"""
        (app_dir / "README.txt").write_text(readme_content)
        
        # Create the tarball
        log_info(f"Creating tarball: {tarball_name}")
        with tarfile.open(tarball_path, 'w:gz') as tar:
            tar.add(app_dir, arcname=ctx.get_app_base_name())
        
        # Get file size for logging
        file_size = tarball_path.stat().st_size
        log_success(f"Tarball created: {tarball_name} ({file_size // (1024*1024)} MB)")
        
        return True
        
    except Exception as e:
        log_error(f"Failed to create tarball: {e}")
        return False
    finally:
        # Clean up temp directory
        if temp_dir.exists():
            shutil.rmtree(temp_dir)


def create_appimage(ctx: BuildContext) -> bool:
    """Create AppImage package (if tools are available)"""
    log_info("\n📦 Creating AppImage package...")
    
    # This is a simplified AppImage creation
    # In a full implementation, you'd use appimagetool and create proper AppDir structure
    log_warning("AppImage creation is not yet fully implemented")
    log_info("Would require appimagetool and proper AppDir structure")
    return False


def create_deb(ctx: BuildContext) -> bool:
    """Create .deb package (if tools are available)"""
    log_info("\n📦 Creating DEB package...")
    
    # Check for dpkg-deb
    if not shutil.which("dpkg-deb"):
        log_warning("dpkg-deb not found, cannot create DEB package")
        return False
    
    # This is a simplified DEB creation
    # In a full implementation, you'd create proper DEBIAN control structure
    log_warning("DEB package creation is not yet fully implemented")
    log_info("Would require proper DEBIAN/control file and package structure")
    return False


def create_desktop_file(ctx: BuildContext, app_dir: Path) -> bool:
    """Create .desktop file for Linux desktop integration"""
    desktop_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=Nxtscape Browser
Comment=Nxtscape Browser - Privacy-focused web browser
Exec={ctx.get_app_base_name().lower()}
Icon={ctx.get_app_base_name().lower()}
Terminal=false
Categories=Network;WebBrowser;
MimeType=text/html;text/xml;application/xhtml+xml;application/xml;application/vnd.mozilla.xul+xml;application/rss+xml;application/rdf+xml;image/gif;image/jpeg;image/png;x-scheme-handler/http;x-scheme-handler/https;x-scheme-handler/ftp;x-scheme-handler/chrome;video/webm;application/x-xpinstall;
StartupNotify=true
StartupWMClass=nxtscape-browser
"""
    
    desktop_file = app_dir / f"{ctx.get_app_base_name().lower()}.desktop"
    desktop_file.write_text(desktop_content)
    log_info("  Created: desktop file")
    return True


def check_appimage_tools() -> bool:
    """Check if AppImage creation tools are available"""
    return shutil.which("appimagetool") is not None


def check_deb_tools() -> bool:
    """Check if DEB package creation tools are available"""
    return shutil.which("dpkg-deb") is not None


def sign_packages(ctx: BuildContext, certificate_path: Optional[str] = None) -> bool:
    """Sign Linux packages (limited support)"""
    log_info("\n🔏 Signing Linux packages...")
    
    if not certificate_path:
        log_warning("No certificate specified, skipping package signing")
        return True
    
    # Linux package signing is less standardized than Windows/macOS
    # Different package managers have different signing mechanisms
    log_warning("Linux package signing is not yet implemented")
    log_info("Different Linux package managers use different signing mechanisms")
    return True


def package_universal(contexts: List[BuildContext]) -> bool:
    """Create universal Linux packages (multi-architecture support is limited)"""
    log_info("\n📦 Creating universal Linux packages...")
    
    # Linux doesn't have the same universal binary concept as macOS
    # Instead, we'd typically create separate packages for each architecture
    log_warning("Universal Linux binaries are not supported like macOS")
    log_info("Consider creating separate packages for each architecture (x64, arm64)")
    
    # For now, just package each architecture separately
    success = True
    for ctx in contexts:
        if not package(ctx):
            success = False
    
    return success


def get_linux_info() -> Dict[str, str]:
    """Get Linux distribution information"""
    info = {
        "distribution": "unknown",
        "version": "unknown",
        "codename": "unknown"
    }
    
    # Try to get distribution info from /etc/os-release
    try:
        with open("/etc/os-release", "r") as f:
            for line in f:
                if line.startswith("ID="):
                    info["distribution"] = line.split("=")[1].strip().strip('"')
                elif line.startswith("VERSION_ID="):
                    info["version"] = line.split("=")[1].strip().strip('"')
                elif line.startswith("VERSION_CODENAME="):
                    info["codename"] = line.split("=")[1].strip().strip('"')
    except FileNotFoundError:
        pass
    
    return info


def install_system_dependencies() -> bool:
    """Install system dependencies needed for packaging (if running as root)"""
    log_info("\n📋 Checking system dependencies...")
    
    if os.geteuid() != 0:
        log_warning("Not running as root, cannot install system dependencies")
        log_info("Consider installing manually: dpkg-dev, appimagetool")
        return True
    
    # This would install packaging tools on different distributions
    linux_info = get_linux_info()
    
    if linux_info["distribution"] in ["ubuntu", "debian"]:
        try:
            run_command(["apt", "update"])
            run_command(["apt", "install", "-y", "dpkg-dev", "fakeroot"])
            log_success("Installed Debian/Ubuntu packaging tools")
            return True
        except Exception as e:
            log_warning(f"Failed to install packaging tools: {e}")
            return False
    
    log_info(f"Unsupported distribution for auto-install: {linux_info['distribution']}")
    return True