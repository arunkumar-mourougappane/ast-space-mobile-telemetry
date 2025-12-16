#!/usr/bin/env python3
"""
AST SpaceMobile Telemetry - Virtual Environment Setup Script (Python Version)
=============================================================================

This script creates a Python virtual environment and installs all required
dependencies for the AST SpaceMobile satellite tracking and reporting tools.

Usage:
    python setup_venv.py

Created: December 15, 2025
"""

import os
import platform
import subprocess
import sys
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output"""

    BLUE = "\033[0;34m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    RED = "\033[0;31m"
    NC = "\033[0m"  # No Color


def print_header(text):
    """Print a formatted header"""
    print(f"{Colors.BLUE}{'═' * 70}{Colors.NC}")
    print(f"{Colors.BLUE}{text.center(70)}{Colors.NC}")
    print(f"{Colors.BLUE}{'═' * 70}{Colors.NC}\n")


def print_step(text):
    """Print a step message"""
    print(f"{Colors.YELLOW}► {text}{Colors.NC}")


def print_success(text):
    """Print a success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.NC}")


def print_error(text):
    """Print an error message"""
    print(f"{Colors.RED}✗ {text}{Colors.NC}")


def run_command(cmd, description=None, check=True):
    """Run a shell command and handle errors"""
    if description:
        print(f"  {description}...")

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=check,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr


def check_python_version():
    """Check if Python version is sufficient"""
    print_step("Checking Python installation...")

    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_error(f"Python 3.8+ required, found {version_str}")
        return False

    print_success(f"Found Python {version_str}")
    return True


def create_venv(venv_path):
    """Create virtual environment"""
    if venv_path.exists():
        print(
            f"\n{Colors.YELLOW}⚠ Virtual environment already exists at: {venv_path}{Colors.NC}"
        )
        response = input("Remove and create fresh? (y/N): ").strip().lower()

        if response == "y":
            print_step("Removing existing virtual environment...")
            import shutil

            shutil.rmtree(venv_path)
            print_success("Removed existing virtual environment")
        else:
            print_step("Using existing virtual environment")
            return True

    print_step("Creating virtual environment...")
    success, stdout, stderr = run_command(
        f'"{sys.executable}" -m venv "{venv_path}"', check=False
    )

    if not success:
        print_error("Failed to create virtual environment")
        print(stderr)
        return False

    print_success("Virtual environment created")
    return True


def get_pip_executable(venv_path):
    """Get the pip executable path for the virtual environment"""
    if platform.system() == "Windows":
        return venv_path / "Scripts" / "pip.exe"
    else:
        return venv_path / "bin" / "pip"


def get_python_executable(venv_path):
    """Get the Python executable path for the virtual environment"""
    if platform.system() == "Windows":
        return venv_path / "Scripts" / "python.exe"
    else:
        return venv_path / "bin" / "python"


def upgrade_pip(pip_path):
    """Upgrade pip to latest version"""
    print_step("Upgrading pip...")
    success, _, _ = run_command(f'"{pip_path}" install --upgrade pip', check=False)

    if success:
        print_success("pip upgraded")
    else:
        print_error("Failed to upgrade pip (continuing anyway)")

    return success


def install_packages(pip_path):
    """Install required packages"""
    print_step("Installing required Python packages...\n")

    packages = {
        "Core dependencies": ["numpy", "pandas", "requests"],
        "Orbital mechanics": ["skyfield"],
        "Visualization": ["matplotlib"],
        "Document generation": ["markdown", "weasyprint"],
    }

    all_success = True

    for category, pkgs in packages.items():
        print(f"{Colors.BLUE}  Installing {category.lower()}:{Colors.NC}")

        for pkg in pkgs:
            success, _, stderr = run_command(
                f'"{pip_path}" install {pkg}', f"    {pkg}", check=False
            )

            if not success:
                print_error(f"Failed to install {pkg}")
                print(stderr)
                all_success = False

        print()

    return all_success


def verify_installation(python_path):
    """Verify that all packages are installed correctly"""
    print_step("Verifying installation...\n")

    verification_script = """
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
"""

    result = subprocess.run(
        [str(python_path), "-c", verification_script], capture_output=True, text=True
    )

    print(result.stdout)

    if result.returncode == 0:
        print_success("All packages verified")
        return True
    else:
        print_error("Some packages failed verification")
        return False


def create_activation_helper(script_dir):
    """Create a helper script for activating the environment"""
    print_step("Creating activation helper script...")

    if platform.system() == "Windows":
        activate_script = script_dir / "activate.bat"
        content = """@echo off
echo AST SpaceMobile Telemetry environment activated
call .venv\\Scripts\\activate.bat
python --version
echo.
echo Available scripts:
echo   - ast_satellite_report.py      : Generate satellite trajectory data
echo   - generate_pass_report.py      : Analyze passes and create report
echo   - generate_pdf_report.py       : Convert markdown to PDF
echo.
"""
    else:
        activate_script = script_dir / "activate.sh"
        content = """#!/bin/bash
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
"""

    activate_script.write_text(content)

    if platform.system() != "Windows":
        os.chmod(activate_script, 0o755)

    print_success(f"Activation helper created: {activate_script.name}")


def print_summary(venv_path):
    """Print setup summary"""
    print(f"\n{Colors.BLUE}{'═' * 70}{Colors.NC}")
    print(f"{Colors.BLUE}{'SETUP COMPLETE!'.center(70)}{Colors.NC}")
    print(f"{Colors.BLUE}{'═' * 70}{Colors.NC}\n")

    print(f"{Colors.GREEN}Virtual environment is ready at: {venv_path}{Colors.NC}\n")

    if platform.system() == "Windows":
        print(f"{Colors.YELLOW}To activate the environment:{Colors.NC}")
        print(f"  {Colors.BLUE}.venv\\Scripts\\activate{Colors.NC}")
        print(f"  {Colors.BLUE}# or use the helper script:{Colors.NC}")
        print(f"  {Colors.BLUE}activate.bat{Colors.NC}\n")
    else:
        print(f"{Colors.YELLOW}To activate the environment:{Colors.NC}")
        print(f"  {Colors.BLUE}source .venv/bin/activate{Colors.NC}")
        print(f"  {Colors.BLUE}# or use the helper script:{Colors.NC}")
        print(f"  {Colors.BLUE}source activate.sh{Colors.NC}\n")

    print(f"{Colors.YELLOW}To deactivate:{Colors.NC}")
    print(f"  {Colors.BLUE}deactivate{Colors.NC}\n")

    print(f"{Colors.YELLOW}Installed scripts:{Colors.NC}")
    print(
        f"  {Colors.BLUE}1. ast_satellite_report.py{Colors.NC}      - Generate satellite trajectory data"
    )
    print(
        f"  {Colors.BLUE}2. generate_pass_report.py{Colors.NC}      - Analyze passes and create report"
    )
    print(
        f"  {Colors.BLUE}3. generate_pdf_report.py{Colors.NC}       - Convert markdown to PDF\n"
    )

    print(f"{Colors.GREEN}Happy tracking! 🛰️{Colors.NC}\n")


def main():
    """Main setup function"""
    print_header("AST SpaceMobile Telemetry - Virtual Environment Setup")

    # Get paths
    script_dir = Path(__file__).parent.resolve()
    venv_path = script_dir / ".venv"

    # Check Python version
    if not check_python_version():
        sys.exit(1)

    # Create virtual environment
    print()
    if not create_venv(venv_path):
        sys.exit(1)

    # Get executables
    pip_path = get_pip_executable(venv_path)
    python_path = get_python_executable(venv_path)

    # Upgrade pip
    print()
    upgrade_pip(pip_path)

    # Install packages
    print()
    if not install_packages(pip_path):
        print_error("Some packages failed to install")
        sys.exit(1)

    print_success("All dependencies installed successfully")

    # Verify installation
    print()
    if not verify_installation(python_path):
        sys.exit(1)

    # Create activation helper
    print()
    create_activation_helper(script_dir)

    # Print summary
    print_summary(venv_path)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Setup interrupted by user{Colors.NC}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
