#!/usr/bin/env python3
"""
Command-line interface for pass analysis and report generation
"""

import argparse
import sys

from ast_spacemobile.reports.generator import generate_pass_report


def main():
    """Main entry point for pass report CLI"""
    parser = argparse.ArgumentParser(
        description="Generate detailed pass analysis report with visualizations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  # Auto-detect latest satellite data file
  ast-passes

  # Specify satellite data file
  ast-passes --data ast_satellite_data_dec7-12.json

  # Specify output directory for graphs
  ast-passes --output-dir my_graphs
        """,
    )

    parser.add_argument(
        "--data",
        type=str,
        default=None,
        help="Path to satellite data JSON file (auto-detected if not specified)",
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="pass_graphs",
        help="Directory for graph outputs (default: pass_graphs)",
    )

    args = parser.parse_args()

    try:
        report_file = generate_pass_report(
            satellite_data_file=args.data,
            output_dir=args.output_dir,
        )
        print("\n✓ All files generated successfully!")
        print(f"\n📄 Report: {report_file}")
        print(f"📈 Graphs: {args.output_dir}/")
    except Exception as e:
        print(f"\n❌ Error generating report: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
