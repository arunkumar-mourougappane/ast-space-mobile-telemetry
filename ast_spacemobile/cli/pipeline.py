#!/usr/bin/env python3
"""
Command-line interface for running the complete analysis pipeline
"""

import argparse
import subprocess  # nosec B404 - Needed for running analysis pipeline
import sys
from datetime import datetime


def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n{'='*80}")
    print(f"{description}")
    print(f"{'='*80}\n")

    result = subprocess.run(cmd, shell=False)  # nosec B603 - Controlled command execution

    if result.returncode != 0:
        print(f"\n❌ Error: {description} failed with exit code {result.returncode}")
        return False

    return True


def validate_dates(start_str, end_str):
    """Validate and parse date strings"""
    start_date = datetime.strptime(start_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_str, "%Y-%m-%d")

    if end_date < start_date:
        print("❌ Error: End date must be after start date")
        sys.exit(1)

    return start_date, end_date


def print_success_summary(args, start_date, end_date):
    """Print success summary with generated files"""
    print("\n" + "=" * 80)
    print("✅ ANALYSIS PIPELINE COMPLETE")
    print("=" * 80)
    print("\nGenerated files:")

    if not args.skip_data:
        date_suffix = f"{start_date.strftime('%b%d').lower()}-{end_date.strftime('%b%d').lower()}"
        print(f"  📊 Data: ast_satellite_data_{date_suffix}.json")
        print(f"  📊 CSV files: ast_*_{date_suffix}.csv")

    if not args.skip_passes:
        print("  📄 Report: AST_SpaceMobile_Detailed_Pass_Report.md")
        print("  📈 Graphs: pass_graphs/*.png")

    if not args.skip_pdf:
        print("  📕 PDF: AST_SpaceMobile_Detailed_Pass_Report.pdf")

    print()


def run_analysis_pipeline(args, start_date, end_date):
    """Execute the analysis pipeline steps"""
    print("\n" + "=" * 80)
    print("AST SPACEMOBILE COMPLETE ANALYSIS PIPELINE")
    print("=" * 80)
    print(f"\nDate Range: {start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')}")
    print(f"Duration: {(end_date - start_date).days + 1} days")

    # Step 1: Generate satellite data
    if not args.skip_data:
        cmd = [
            sys.executable,
            "-m",
            "ast_spacemobile.cli.trajectory",
            "--start",
            args.start,
            "--end",
            args.end,
        ]

        if not run_command(cmd, "Step 1/3: Generating Satellite Trajectory Data"):
            sys.exit(1)
    else:
        print("\n⏭️  Skipping satellite data generation")

    # Step 2: Generate pass report
    if not args.skip_passes:
        # Check if satellite data files exist
        import glob

        json_files = glob.glob("ast_satellite_data_*.json")
        if not json_files:
            print("\n❌ Error: No satellite data files found")
            print("   Run without --skip-data to generate data first")
            sys.exit(1)

        cmd = [sys.executable, "-m", "ast_spacemobile.cli.passes"]

        if not run_command(cmd, "Step 2/3: Analyzing Passes and Generating Report"):
            sys.exit(1)
    else:
        print("\n⏭️  Skipping pass report generation")

    # Step 3: Generate PDF
    if not args.skip_pdf:
        cmd = [sys.executable, "generate_pdf_report.py"]

        if not run_command(cmd, "Step 3/3: Generating PDF Report"):
            sys.exit(1)
    else:
        print("\n⏭️  Skipping PDF generation")


def main():
    """Main entry point for pipeline CLI"""
    parser = argparse.ArgumentParser(
        description="Run complete AST SpaceMobile satellite analysis pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  # Use default dates (Dec 7-12, 2025)
  ast-pipeline

  # Custom date range
  ast-pipeline --start 2025-12-01 --end 2025-12-15

  # Generate only pass report from existing data
  ast-pipeline --skip-data

  # Generate only PDF from existing markdown
  ast-pipeline --skip-data --skip-passes
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

    parser.add_argument(
        "--skip-data",
        action="store_true",
        help="Skip satellite data generation (use existing data)",
    )

    parser.add_argument(
        "--skip-passes",
        action="store_true",
        help="Skip pass report generation (use existing report)",
    )

    parser.add_argument("--skip-pdf", action="store_true", help="Skip PDF generation")

    args = parser.parse_args()

    try:
        # Validate dates
        start_date, end_date = validate_dates(args.start, args.end)

        # Run the analysis pipeline
        run_analysis_pipeline(args, start_date, end_date)

        # Success summary
        print_success_summary(args, start_date, end_date)

    except ValueError as e:
        print(f"\n❌ Error parsing dates: {e}")
        print("Please use YYYY-MM-DD format for dates")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
