# AST SpaceMobile Analysis - Project Summary

## Overview
This project contains comprehensive trajectory and signal strength analysis for all AST SpaceMobile satellites over Midland, TX from December 7-12, 2025.

## Generated Reports and Data Files

### 📊 Main Reports

1. **[AST_SpaceMobile_Detailed_Pass_Report.pdf](AST_SpaceMobile_Detailed_Pass_Report.pdf)** 🎯 **PROFESSIONAL PDF REPORT**
   - 30.1 MB stylized PDF with embedded images
   - Professional layout with title page, headers, and page numbers
   - All 228 satellite pass graphs embedded at full quality
   - Color-coded tables and sections
   - Optimized for printing and distribution
   - **Bonus:** [HTML version](AST_SpaceMobile_Detailed_Pass_Report.html) for web viewing

2. **[AST_SpaceMobile_Detailed_Pass_Report.md](AST_SpaceMobile_Detailed_Pass_Report.md)** ⭐ **SOURCE MARKDOWN**
   - 7,367 lines of detailed analysis
   - 228 individual satellite passes analyzed
   - Complete pass tables with local (CST) timestamps
   - Signal strength graphs for each pass
   - Detailed metrics and statistics per pass
   - **Size:** 233 KB

3. **[AST_SpaceMobile_Satellite_Report_Dec7-12-2025.md](AST_SpaceMobile_Satellite_Report_Dec7-12-2025.md)** - Executive Summary
   - Overview of AST SpaceMobile satellite fleet
   - Orbital parameters (TLE data)
   - Aggregate statistics
   - Methodology documentation
   - **Size:** 219 lines

### 📈 Visualizations

**[pass_graphs/](pass_graphs/)** directory contains 228 signal strength graphs
- One graph per satellite pass
- Each graph shows:
  - Signal power (dBm) vs time
  - Elevation angle vs time
  - SNR (dB) vs time with quality thresholds
- **Total Size:** 32 MB
- **Format:** PNG images (150 DPI)

### 📁 Data Files

**CSV Files (5-second interval data):**
- [ast_bluewalker_3_dec7-12.csv](ast_bluewalker_3_dec7-12.csv) - 103,681 records
- [ast_bluebird-1_dec7-12.csv](ast_bluebird-1_dec7-12.csv) - 103,681 records
- [ast_bluebird-2_dec7-12.csv](ast_bluebird-2_dec7-12.csv) - 103,681 records
- [ast_bluebird-3_dec7-12.csv](ast_bluebird-3_dec7-12.csv) - 103,681 records
- [ast_bluebird-4_dec7-12.csv](ast_bluebird-4_dec7-12.csv) - 103,681 records
- [ast_bluebird-5_dec7-12.csv](ast_bluebird-5_dec7-12.csv) - 103,681 records
- **Total:** 622,086 records across all satellites

**JSON Data:**
- [ast_satellite_data_dec7-12.json](ast_satellite_data_dec7-12.json) - Complete structured dataset

## Satellites Analyzed

| Satellite | NORAD ID | Passes | Description |
|-----------|----------|--------|-------------|
| **BLUEWALKER 3** | 53807 | 45 | Test satellite, largest commercial LEO communications array |
| **BLUEBIRD-1** | 60399 | 36 | First commercial Block 1 BlueBird satellite |
| **BLUEBIRD-2** | 60400 | 37 | Second commercial Block 1 BlueBird satellite |
| **BLUEBIRD-3** | 60401 | 37 | Third commercial Block 1 BlueBird satellite |
| **BLUEBIRD-4** | 60402 | 37 | Fourth commercial Block 1 BlueBird satellite |
| **BLUEBIRD-5** | 60403 | 36 | Fifth commercial Block 1 BlueBird satellite |
| **TOTAL** | - | **228** | - |

## Key Statistics

### Analysis Parameters
- **Location:** Midland, TX (31.9973°N, 102.0779°W, elevation 872m)
- **Date Range:** December 7-12, 2025 (6 days)
- **Measurement Interval:** 5 seconds
- **Total Data Points:** 622,086 across all satellites
- **Visible Observations:** 21,003 measurements
- **Total Passes:** 228 individual satellite passes

### Signal Performance Summary
- **Peak Signal Strength:** -54 to -57 dBm (closest approaches)
- **Average Visible Signal:** -66 to -70 dBm
- **Maximum Elevations:** 73-87° (excellent overhead passes)
- **SNR Range:** 33-53 dB during visible passes
- **Link Quality:** Predominantly "Excellent" to "Good"

## What's in the Detailed Pass Report?

The [AST_SpaceMobile_Detailed_Pass_Report.md](AST_SpaceMobile_Detailed_Pass_Report.md) contains:

### For Each Satellite:
1. **Pass Summary Table** - Overview of all passes with:
   - Start/End times in local CST
   - Duration (mm:ss)
   - Maximum elevation
   - Signal strength metrics
   - Peak SNR

2. **Detailed Pass Analysis** - For each individual pass:
   - **Embedded graph** showing signal strength and elevation over time
   - **Comprehensive metrics table**:
     - Duration and elevation range
     - Distance (range) to satellite
     - Signal power statistics (peak, min, average)
     - SNR statistics
     - Link quality assessment
   - **Sample position data table** - Key moments during the pass

## CSV Data Columns

Each CSV file contains the following columns:
- `timestamp` - ISO 8601 UTC timestamp
- `unix_timestamp` - Unix epoch time
- `elevation_deg` - Satellite elevation angle (degrees)
- `azimuth_deg` - Satellite azimuth angle (degrees, 0°=North)
- `range_km` - Distance from Midland to satellite (km)
- `satellite_lat` - Satellite sub-point latitude
- `satellite_lon` - Satellite sub-point longitude
- `satellite_alt_km` - Satellite altitude above Earth (km)
- `visible` - Boolean, true if above horizon
- `received_power_dbm` - Estimated signal power (dBm)
- `snr_db` - Signal-to-Noise Ratio (dB)
- `link_quality` - Qualitative assessment (Excellent/Good/Fair/Poor/Very Poor)
- `path_loss_db` - Total path loss
- `atmospheric_loss_db` - Atmospheric attenuation

## Technical Methodology

### Orbital Calculations
- **TLE Data:** Current Two-Line Element sets from Celestrak
- **Propagator:** SGP4 orbital mechanics model via Skyfield library
- **Precision:** Sub-kilometer accuracy for trajectory calculations

### Signal Strength Model
- **Frequency:** ~2 GHz (cellular bands)
- **Satellite EIRP:** 55 dBW (assumed)
- **Ground Station Gain:** 15 dBi
- **Path Loss:** Free Space Path Loss + atmospheric attenuation
- **Noise Floor:** -110 dBm

### Link Quality Thresholds
- **Excellent:** SNR ≥ 20 dB
- **Good:** SNR ≥ 15 dB
- **Fair:** SNR ≥ 10 dB
- **Poor:** SNR ≥ 5 dB
- **Very Poor:** SNR < 5 dB

## Scripts

- **[ast_satellite_report.py](ast_satellite_report.py)** - Initial data collection and basic report generation
- **[generate_pass_report.py](generate_pass_report.py)** - Detailed pass analysis and visualization
- **[generate_pdf_report.py](generate_pdf_report.py)** - PDF generation with professional styling

## Usage Examples

### View a Specific Pass
To analyze a specific pass, open the detailed report and navigate to the satellite section. For example, BLUEWALKER 3 Pass #16 on 12/09 shows:
- 11:20 minute duration
- Maximum elevation: 51.7°
- Peak signal: -58.6 dBm
- Peak SNR: 51.4 dB (Excellent quality)

### Extract Pass Data
To get raw data for a specific pass, use the CSV files and filter by timestamp. For example, BLUEBIRD-1's first pass on 12/06 at 19:19-19:30 CST can be extracted from the CSV.

### Compare Satellites
Use the pass summary tables to compare performance across satellites. All satellites show similar signal characteristics when at comparable elevations.

## Time Zone Note
⚠️ **Important:** 
- All timestamps in CSV and JSON files are in **UTC**
- All timestamps in the detailed pass report are in **CST (UTC-6)**
- Midland, TX is in Central Standard Time during December

## Report Generation
- **Generated:** December 15, 2025
- **Software:** AST SpaceMobile Satellite Analysis Tool v1.0
- **Python Libraries:** Skyfield, NumPy, Pandas, Matplotlib, Requests

## Quick Navigation

### Want to see all passes at a glance?
→ Open [AST_SpaceMobile_Detailed_Pass_Report.md](AST_SpaceMobile_Detailed_Pass_Report.md) and scroll to any satellite's "Pass Summary" table

### Want detailed analysis of a specific pass?
→ Find the pass in the summary table, then scroll down to the "Detailed Pass Analysis" section

### Want to analyze raw data?
→ Use the CSV files with your preferred data analysis tool (Excel, Python, R, etc.)

### Want to see orbital parameters?
→ Check [AST_SpaceMobile_Satellite_Report_Dec7-12-2025.md](AST_SpaceMobile_Satellite_Report_Dec7-12-2025.md) for TLE data

### Want to see signal graphs?
→ All graphs are embedded in the detailed report and saved in [pass_graphs/](pass_graphs/)

---

**For questions or additional analysis, refer to the methodology sections in the reports or examine the Python scripts.**
