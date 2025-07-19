#!/bin/bash
# BrowserOS Docker Build Script
# This script creates a containerized build environment for BrowserOS

set -e

echo "🐳 Setting up BrowserOS Docker build environment..."

# Create Dockerfile for BrowserOS build
cat > Dockerfile << 'EOF'
FROM ubuntu:22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    wget \
    lsb-release \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Install depot_tools for Chromium
RUN git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git /opt/depot_tools
ENV PATH="/opt/depot_tools:${PATH}"

# Create build user
RUN useradd -m -s /bin/bash builder && \
    echo "builder ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER builder
WORKDIR /home/builder

# Set up Python virtual environment
RUN python3 -m venv browseros-env

# Copy BrowserOS source
COPY --chown=builder:builder . /home/builder/BrowserOS/
WORKDIR /home/builder/BrowserOS

# Install Python dependencies
RUN /home/builder/browseros-env/bin/pip install -r requirements.txt

# Expose build directory
VOLUME ["/home/builder/BrowserOS/out"]

CMD ["/bin/bash"]
EOF

echo "📦 Building Docker image..."
docker build -t browseros-build .

echo "🚀 Docker build environment ready!"
echo "To use:"
echo "  docker run -it --rm -v \$(pwd)/out:/home/builder/BrowserOS/out browseros-build"
echo "  # Then inside container:"
echo "  # source browseros-env/bin/activate"
echo "  # python build/build.py --build --package --arch x64"
