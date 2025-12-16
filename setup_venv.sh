#!/bin/bash

################################################################################
# AST SpaceMobile Telemetry - Virtual Environment Setup Script
################################################################################
# This script creates a Python virtual environment and installs all required
# dependencies for the AST SpaceMobile satellite tracking and reporting tools.
#
# Usage:
#   chmod +x setup_venv.sh
#   ./setup_venv.sh
#
# Created: December 15, 2025
################################################################################

set -e  # Exit on error

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     AST SpaceMobile Telemetry - Virtual Environment Setup         ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

# Check Python version
echo -e "${YELLOW}► Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 is not installed. Please install Python 3.8 or later.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓ Found Python $PYTHON_VERSION${NC}"

# Check if python3-venv is installed (required on some Linux distros)
if ! python3 -m venv --help &> /dev/null; then
    echo -e "${YELLOW}► python3-venv module not found. Installing...${NC}"
    if command -v apt-get &> /dev/null; then
        sudo apt-get update && sudo apt-get install -y python3-venv
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3-venv
    else
        echo -e "${RED}✗ Could not install python3-venv automatically.${NC}"
        echo -e "${RED}  Please install it manually for your system.${NC}"
        exit 1
    fi
fi

# Remove existing venv if requested
if [ -d "$VENV_DIR" ]; then
    echo ""
    echo -e "${YELLOW}⚠ Virtual environment already exists at: $VENV_DIR${NC}"
    read -p "Do you want to remove it and create a fresh one? (y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}► Removing existing virtual environment...${NC}"
        rm -rf "$VENV_DIR"
        echo -e "${GREEN}✓ Removed existing virtual environment${NC}"
    else
        echo -e "${YELLOW}► Using existing virtual environment${NC}"
    fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo ""
    echo -e "${YELLOW}► Creating virtual environment...${NC}"
    python3 -m venv "$VENV_DIR"
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo ""
echo -e "${YELLOW}► Activating virtual environment...${NC}"
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Upgrade pip
echo ""
echo -e "${YELLOW}► Upgrading pip...${NC}"
python -m pip install --upgrade pip
echo -e "${GREEN}✓ pip upgraded${NC}"

# Install dependencies
echo ""
echo -e "${YELLOW}► Installing required Python packages...${NC}"
echo ""

# Core dependencies
echo -e "${BLUE}  Installing core dependencies:${NC}"
pip install numpy pandas requests

# Orbital mechanics
echo ""
echo -e "${BLUE}  Installing orbital mechanics library:${NC}"
pip install skyfield

# Visualization
echo ""
echo -e "${BLUE}  Installing visualization libraries:${NC}"
pip install matplotlib

# Document generation
echo ""
echo -e "${BLUE}  Installing document generation libraries:${NC}"
pip install markdown weasyprint

echo ""
echo -e "${GREEN}✓ All dependencies installed successfully${NC}"

# Verify installation
echo ""
echo -e "${YELLOW}► Verifying installation...${NC}"
python << 'EOF'
import sys
import importlib

packages = {
    'numpy': 'NumPy',
    'pandas': 'Pandas',
    'requests': 'Requests',
    'skyfield': 'Skyfield',
    'matplotlib': 'Matplotlib',
    'markdown': 'Markdown',
    'weasyprint': 'WeasyPrint'
}

all_ok = True
for module, name in packages.items():
    try:
        mod = importlib.import_module(module)
        version = getattr(mod, '__version__', 'unknown')
        print(f"  ✓ {name:15} (v{version})")
    except ImportError:
        print(f"  ✗ {name:15} - MISSING!")
        all_ok = False

sys.exit(0 if all_ok else 1)
EOF

# shellcheck disable=SC2181
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ All packages verified${NC}"
else
    echo -e "${RED}✗ Some packages failed verification${NC}"
    exit 1
fi

# Create activation helper script
echo ""
echo -e "${YELLOW}► Creating activation helper script...${NC}"
cat > "$SCRIPT_DIR/activate.sh" << 'ACTIVATE_EOF'
#!/bin/bash
# Quick activation script for AST SpaceMobile Telemetry environment

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/.venv/bin/activate"

echo "AST SpaceMobile Telemetry environment activated"
echo "Python: $(python --version)"
echo ""
echo "Available scripts:"
echo "  - ast_satellite_report.py      : Generate satellite trajectory data"
echo "  - generate_pass_report.py      : Analyze passes and create report"
echo "  - generate_pdf_report.py       : Convert markdown to PDF"
echo ""
ACTIVATE_EOF

chmod +x "$SCRIPT_DIR/activate.sh"
echo -e "${GREEN}✓ Activation helper created: activate.sh${NC}"

# Summary
echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                    SETUP COMPLETE!                                 ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}Virtual environment is ready at: $VENV_DIR${NC}"
echo ""
echo -e "${YELLOW}To activate the environment:${NC}"
echo -e "  ${BLUE}source .venv/bin/activate${NC}"
echo -e "  ${BLUE}# or use the helper script:${NC}"
echo -e "  ${BLUE}source activate.sh${NC}"
echo ""
echo -e "${YELLOW}To deactivate:${NC}"
echo -e "  ${BLUE}deactivate${NC}"
echo ""
echo -e "${YELLOW}Installed scripts:${NC}"
echo -e "  ${BLUE}1. ast_satellite_report.py${NC}      - Generate satellite trajectory data"
echo -e "  ${BLUE}2. generate_pass_report.py${NC}      - Analyze passes and create report"
echo -e "  ${BLUE}3. generate_pdf_report.py${NC}       - Convert markdown to PDF"
echo ""
echo -e "${GREEN}Happy tracking! 🛰️${NC}"
echo ""
