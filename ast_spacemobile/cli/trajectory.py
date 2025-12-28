#!/usr/bin/env python3
"""
Command-line interface for satellite trajectory report generation
"""

import argparse
import sys
from datetime import datetime

from ast_spacemobile.reports.generator import generate_trajectory_report


def main():
    """Main entry point for trajectory report CLI"""
    parser = argparse.ArgumentParser(
        description="Generate AST SpaceMobile satellite trajectory and signal strength report",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  # Use default dates (Dec 7-12, 2025)
  ast-trajectory

  # Custom date range
  ast-trajectory --start 2025-12-01 --end 2025-12-15

  # Single day analysis
  ast-trajectory --start 2025-12-10 --end 2025-12-10
        """,
    )

    parser.add_argument(
        "--start",
        type=str,
        default="2025-12-07",
        help="Start date in YYYY-MM-DD format (default: 2025-12-07)",
    )

    parser.add_argument(
        "--end",
        type=str,
        default="2025-12-12",
        help="End date in YYYY-MM-DD format (default: 2025-12-12)",
    )

    args = parser.parse_args()

    try:
        # Parse dates
        start_date = datetime.strptime(args.start, "%Y-%m-%d").replace(hour=0, minute=0, second=0)
        end_date = datetime.strptime(args.end, "%Y-%m-%d").replace(hour=23, minute=59, second=59)

        # Validate dates
        if end_date < start_date:
            print("❌ Error: End date must be after start date")
            sys.exit(1)

        # Generate report with custom dates
        data, report_file = generate_trajectory_report(start_date, end_date)
        print("\n✓ All files generated successfully!")
        print(f"\n📊 Main Report: {report_file}")
        print("📁 Data files created in current directory")
    except ValueError as e:
        print(f"\n❌ Error parsing dates: {e}")
        print("Please use YYYY-MM-DD format for dates")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error generating report: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
