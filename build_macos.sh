#!/bin/bash
# macOS Build Script for GPT Computer Agent
# Exit on any error
set -e

# Configuration
APP_NAME="GPT_Computer_Agent"
VERSION="1.0.0"
WORKDIR=$(pwd)
DIST_DIR="${WORKDIR}/dist"
DMG_DIR="${DIST_DIR}/dmg"
APP_BUNDLE="${DIST_DIR}/${APP_NAME}.app"
DMG_FILE="${DIST_DIR}/${APP_NAME}_${VERSION}.dmg"
ICON_PATH="gpt_computer_agent/utils/media/icon.icns"
MEDIA_DIR="gpt_computer_agent/utils/media"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# Check if running on macOS
if [[ "$(uname)" != "Darwin" ]]; then
    echo "This script is intended for macOS only."
    exit 1
fi

# Get Python version
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
info "Detected Python version: ${PYTHON_VERSION}"

# Install dependencies
info "Installing Python dependencies..."
pip install ".[base,agentic]" || {
    warn "Failed to install Python dependencies"
    exit 1
}

# Install Homebrew if not installed
if ! command -v brew &> /dev/null; then
    warn "Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" || {
        warn "Failed to install Homebrew"
        exit 1
    }
    # Add Homebrew to PATH if needed
    export PATH="/opt/homebrew/bin:$PATH"
fi

# Install create-dmg if not installed
if ! command -v create-dmg &> /dev/null; then
    info "Installing create-dmg..."
    brew install create-dmg || {
        warn "Failed to install create-dmg"
        exit 1
    }
fi

# Install appropriate PyInstaller version based on Python version
if [[ "$PYTHON_VERSION" == "3.13"* ]]; then
    PYINSTALLER_VERSION="6.14.2"  # Latest version for Python 3.13
elif [[ "$PYTHON_VERSION" == "3.12"* ]]; then
    PYINSTALLER_VERSION="6.9.0"   # Version for Python 3.12
else
    PYINSTALLER_VERSION="5.13.2"  # Version for Python 3.7-3.11
fi

info "Installing PyInstaller ${PYINSTALLER_VERSION}..."
pip install "pyinstaller==${PYINSTALLER_VERSION}" || {
    warn "Failed to install PyInstaller"
    exit 1
}

# Clean previous builds
info "Cleaning previous builds..."
rm -rf "${DIST_DIR}" "${WORKDIR}/build" "${WORKDIR}/__pycache__"

# Build the application
info "Building application with PyInstaller..."
pyinstaller \
    --recursive-copy-metadata gpt_computer_agent \
    run.py \
    --windowed \
    --add-data="${MEDIA_DIR}/*:${MEDIA_DIR}" \
    --icon="${ICON_PATH}" \
    --name="${APP_NAME}" \
    --clean \
    --noconfirm || {
    warn "PyInstaller build failed"
    exit 1
}

# Create DMG
info "Creating DMG file..."
mkdir -p "${DMG_DIR}"
rm -rf "${DMG_DIR}"/*

if [ -d "${APP_BUNDLE}" ]; then
    cp -R "${APP_BUNDLE}" "${DMG_DIR}/"
    
    # Create a symlink to Applications
    ln -s "/Applications" "${DMG_DIR}/Applications"
    
    # Create DMG
    create-dmg \
        --volname "${APP_NAME} ${VERSION}" \
        --volicon "${ICON_PATH}" \
        --window-pos 200 120 \
        --window-size 600 300 \
        --icon-size 100 \
        --icon "${APP_NAME}.app" 175 120 \
        --hide-extension "${APP_NAME}.app" \
        --app-drop-link 425 120 \
        --no-internet-enable \
        "${DMG_FILE}" \
        "${DMG_DIR}/"
    
    info "DMG created successfully at: ${DMG_FILE}"
else
    warn "Application bundle not found at: ${APP_BUNDLE}"
    exit 1
fi

info "Build process completed successfully!"