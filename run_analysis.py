#!/usr/bin/env python3
"""
AST SpaceMobile Complete Analysis Runner
Runs the full analysis pipeline with configurable date ranges
"""

import argparse
import subprocess
import sys
from datetime import datetime


def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n{'='*80}")
    print(f"{description}")
    print(f"{'='*80}\n")

    result = subprocess.run(cmd, shell=False)

    if result.returncode != 0:
        print(f"\n❌ Error: {description} failed with exit code {result.returncode}")
        return False

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Run complete AST SpaceMobile satellite analysis pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  # Use default dates (Dec 7-12, 2025)
  python run_analysis.py
  
  # Custom date range
  python run_analysis.py --start 2025-12-01 --end 2025-12-15
  
  # Generate only pass report from existing data
  python run_analysis.py --skip-data
  
  # Generate only PDF from existing markdown
  python run_analysis.py --skip-data --skip-passes
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
        start_date = datetime.strptime(args.start, "%Y-%m-%d")
        end_date = datetime.strptime(args.end, "%Y-%m-%d")

        if end_date < start_date:
            print("❌ Error: End date must be after start date")
            sys.exit(1)

        print("\n" + "=" * 80)
        print("AST SPACEMOBILE COMPLETE ANALYSIS PIPELINE")
        print("=" * 80)
        print(
            f"\nDate Range: {start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')}"
        )
        print(f"Duration: {(end_date - start_date).days + 1} days")

        # Step 1: Generate satellite data
        if not args.skip_data:
            cmd = [
                sys.executable,
                "ast_satellite_report.py",
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

            cmd = [sys.executable, "generate_pass_report.py"]

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

        # Success summary
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
