"""
Setup configuration for AST SpaceMobile Analysis Library
"""

from setuptools import find_packages, setup

with open("README_LIBRARY.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ast-spacemobile",
    version="1.0.0",
    author="AST SpaceMobile Analysis Team",
    description="A modular library for analyzing AST SpaceMobile satellite trajectories and signal strength",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "pandas>=1.3.0",
        "requests>=2.26.0",
        "skyfield>=1.42",
        "matplotlib>=3.4.0",
    ],
    entry_points={
        "console_scripts": [
            "ast-trajectory=ast_spacemobile.cli.trajectory:main",
            "ast-passes=ast_spacemobile.cli.passes:main",
            "ast-pipeline=ast_spacemobile.cli.pipeline:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
