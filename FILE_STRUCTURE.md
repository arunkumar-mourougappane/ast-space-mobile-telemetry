# File Structure - AST SpaceMobile Analysis

This document describes the reorganized project structure.

## Directory Tree

```
ast_space_mobile_data/
├── ast_spacemobile/              # Main library package
│   ├── __init__.py              # Public API exports
│   ├── core/                    # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py           # Satellite catalog & configuration
│   │   ├── tle.py              # TLE data fetching from CelesTrak
│   │   └── calculations.py     # Trajectory & signal calculations
│   ├── analysis/                # Analysis tools
│   │   ├── __init__.py
│   │   ├── passes.py           # Pass identification
│   │   └── visualization.py    # Graph generation
│   ├── reports/                 # Report generation
│   │   ├── __init__.py
│   │   └── generator.py        # Report builders
│   └── cli/                     # Command-line interfaces
│       ├── __init__.py
│       ├── trajectory.py       # Trajectory report CLI
│       ├── passes.py           # Pass analysis CLI
│       └── pipeline.py         # Full pipeline CLI
│
├── docs/                        # Documentation
│   ├── README_LIBRARY.md       # Complete library documentation
│   ├── QUICK_START.md          # Quick reference guide
│   ├── MIGRATION_GUIDE.md      # Migration from old scripts
│   ├── LIBRARY_SUMMARY.md      # Project overview
│   └── BEFORE_AFTER.md         # Comparison with old structure
│
├── examples/                    # Usage examples
│   ├── README.md               # Examples index
│   ├── basic_trajectory.py     # Simple trajectory report
│   ├── custom_location.py      # Custom observer location
│   ├── signal_analysis.py      # Signal strength analysis
│   ├── track_single_satellite.py  # Single satellite tracking
│   └── fetch_tle.py            # TLE fetching example
│
├── scripts/                     # Legacy scripts (backward compatibility)
│   ├── ast_satellite_report.py # Original trajectory script
│   ├── generate_pass_report.py # Original pass analysis script
│   ├── run_analysis.py         # Original pipeline script
│   ├── generate_pdf_report.py  # PDF generation script
│   └── setup_venv.py           # Virtual environment setup
│
├── tests/                       # Unit tests (to be added)
│   └── (test files go here)
│
├── setup.py                     # Package configuration
├── requirements.txt             # Python dependencies
├── README.md                    # Main project documentation
└── FILE_STRUCTURE.md            # This file
```

## Directory Purposes

### `ast_spacemobile/` - Main Library
The core library package that can be installed and imported.

**Subdirectories:**
- **core/**: Fundamental functionality (config, TLE, calculations)
- **analysis/**: Analysis tools (pass identification, visualization)
- **reports/**: Report generation (trajectory, pass reports)
- **cli/**: Command-line interfaces for all tools

### `docs/` - Documentation
All project documentation, guides, and references.

**Files:**
- **README_LIBRARY.md**: Complete API documentation
- **QUICK_START.md**: Quick reference for common tasks
- **MIGRATION_GUIDE.md**: How to upgrade from legacy scripts
- **LIBRARY_SUMMARY.md**: High-level project overview
- **BEFORE_AFTER.md**: Comparison showing improvements

### `examples/` - Usage Examples
Practical code examples demonstrating library features.

**Examples:**
- Basic trajectory report generation
- Custom observer locations
- Signal strength analysis
- Single satellite tracking
- TLE data fetching

### `scripts/` - Legacy Scripts
Original scripts maintained for backward compatibility.

**Scripts:**
- Trajectory report generation
- Pass analysis and visualization
- Complete pipeline execution
- PDF report generation

### `tests/` - Unit Tests
Test suite for the library (to be implemented).

## Key Files

### Root Directory

| File | Purpose |
|------|---------|
| `README.md` | Main project documentation |
| `setup.py` | Package installation configuration |
| `requirements.txt` | Python dependencies |
| `FILE_STRUCTURE.md` | This file - project structure guide |

## Import Paths

### Using the Library

```python
# Top-level imports
from ast_spacemobile import generate_trajectory_report, generate_pass_report

# Core modules
from ast_spacemobile.core.config import AST_SATELLITES, OBSERVER_LOCATION
from ast_spacemobile.core.tle import fetch_tle_data
from ast_spacemobile.core.calculations import calculate_signal_strength

# Analysis modules
from ast_spacemobile.analysis.passes import identify_passes
from ast_spacemobile.analysis.visualization import create_signal_strength_graph
```

### Using CLI Tools

```bash
# Run via Python module
python -m ast_spacemobile.cli.trajectory
python -m ast_spacemobile.cli.passes
python -m ast_spacemobile.cli.pipeline

# Or use legacy scripts
python scripts/ast_satellite_report.py
python scripts/generate_pass_report.py
python scripts/run_analysis.py
```

## Benefits of This Structure

✅ **Clear Organization**: Logical separation of concerns
✅ **Easy Navigation**: Intuitive directory names
✅ **Discoverability**: Documentation and examples in dedicated folders
✅ **Maintainability**: Related code grouped together
✅ **Backward Compatibility**: Legacy scripts preserved in scripts/
✅ **Professionalism**: Follows Python packaging best practices

## Adding New Components

### Adding a New Module
1. Create file in appropriate subdirectory (`core/`, `analysis/`, etc.)
2. Add imports to `__init__.py` if it should be public
3. Update documentation in `docs/`
4. Add examples in `examples/`

### Adding Documentation
- Place in `docs/` directory
- Link from main `README.md`
- Update `docs/QUICK_START.md` if relevant

### Adding Examples
- Create in `examples/` directory
- Update `examples/README.md` index
- Include comments explaining the code

### Adding Tests
- Create in `tests/` directory
- Follow naming convention: `test_*.py`
- Run with `pytest tests/`

## File Counts

```
Library:      14 Python files (ast_spacemobile/)
Documentation: 5 Markdown files (docs/)
Examples:      6 files (examples/)
Scripts:       5 Python files (scripts/)
Tests:         TBD (tests/)
Root:          4 files (setup, requirements, README, this file)
```

## Next Steps

1. ✅ Library structure created
2. ✅ Documentation organized
3. ✅ Examples provided
4. ✅ Legacy scripts preserved
5. ⏭️ Add unit tests to tests/
6. ⏭️ Consider adding CI/CD configuration
7. ⏭️ Consider adding .gitignore, LICENSE files

---

**Last Updated**: 2025-12-28
**Version**: 1.0.0
