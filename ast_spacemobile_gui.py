#!/usr/bin/env python3
"""
AST SpaceMobile GTK GUI Application
Interactive application for satellite pass analysis with visualization
"""

import sys
from datetime import datetime, timedelta

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("GTK3Agg")
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.figure import Figure

from ast_spacemobile.core.config import AST_SATELLITES, OBSERVER_LOCATION
from ast_spacemobile.core.tle import fetch_tle_data, create_simulated_tle
from ast_spacemobile.core.calculations import generate_satellite_passes
from ast_spacemobile.analysis.passes import identify_passes
from skyfield.api import EarthSatellite, load, wgs84


class SatelliteAnalysisApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="AST SpaceMobile Satellite Analysis")
        self.set_default_size(1400, 900)
        self.set_border_width(10)

        # Data storage
        self.current_data = None
        self.current_passes = None

        # Create main layout
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(main_box)

        # Add title
        title_label = Gtk.Label()
        title_label.set_markup("<big><b>AST SpaceMobile Satellite Pass Analysis</b></big>")
        main_box.pack_start(title_label, False, False, 5)

        # Create paned window for input/output sections
        paned = Gtk.Paned(orientation=Gtk.Orientation.VERTICAL)
        main_box.pack_start(paned, True, True, 0)

        # Top section: Input controls
        input_frame = Gtk.Frame(label="Analysis Parameters")
        input_box = self.create_input_section()
        input_frame.add(input_box)
        paned.pack1(input_frame, False, False)

        # Bottom section: Results (notebook with tabs)
        results_frame = Gtk.Frame(label="Results")
        self.results_notebook = self.create_results_section()
        results_frame.add(self.results_notebook)
        paned.pack2(results_frame, True, True)

        # Status bar
        self.statusbar = Gtk.Statusbar()
        self.context_id = self.statusbar.get_context_id("status")
        main_box.pack_start(self.statusbar, False, False, 0)

        self.update_status("Ready")

    def create_input_section(self):
        """Create the input controls section"""
        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        grid.set_margin_top(10)
        grid.set_margin_bottom(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)

        row = 0

        # Location section
        location_label = Gtk.Label()
        location_label.set_markup("<b>Observer Location</b>")
        location_label.set_halign(Gtk.Align.START)
        grid.attach(location_label, 0, row, 4, 1)
        row += 1

        # Latitude
        lat_label = Gtk.Label(label="Latitude (°N):")
        lat_label.set_halign(Gtk.Align.END)
        grid.attach(lat_label, 0, row, 1, 1)

        self.lat_entry = Gtk.Entry()
        self.lat_entry.set_text(str(OBSERVER_LOCATION["latitude"]))
        self.lat_entry.set_width_chars(15)
        grid.attach(self.lat_entry, 1, row, 1, 1)

        # Longitude
        lon_label = Gtk.Label(label="Longitude (°E):")
        lon_label.set_halign(Gtk.Align.END)
        grid.attach(lon_label, 2, row, 1, 1)

        self.lon_entry = Gtk.Entry()
        self.lon_entry.set_text(str(OBSERVER_LOCATION["longitude"]))
        self.lon_entry.set_width_chars(15)
        grid.attach(self.lon_entry, 3, row, 1, 1)
        row += 1

        # Elevation
        elev_label = Gtk.Label(label="Elevation (m):")
        elev_label.set_halign(Gtk.Align.END)
        grid.attach(elev_label, 0, row, 1, 1)

        self.elev_entry = Gtk.Entry()
        self.elev_entry.set_text(str(OBSERVER_LOCATION["elevation_m"]))
        self.elev_entry.set_width_chars(15)
        grid.attach(self.elev_entry, 1, row, 1, 1)
        row += 1

        # Separator
        separator1 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(separator1, 0, row, 4, 1)
        row += 1

        # Date/Time section
        datetime_label = Gtk.Label()
        datetime_label.set_markup("<b>Date and Time Range</b>")
        datetime_label.set_halign(Gtk.Align.START)
        grid.attach(datetime_label, 0, row, 4, 1)
        row += 1

        # Start date
        start_label = Gtk.Label(label="Start Date:")
        start_label.set_halign(Gtk.Align.END)
        grid.attach(start_label, 0, row, 1, 1)

        self.start_date_entry = Gtk.Entry()
        default_start = datetime.now().strftime("%Y-%m-%d")
        self.start_date_entry.set_text(default_start)
        self.start_date_entry.set_placeholder_text("YYYY-MM-DD")
        grid.attach(self.start_date_entry, 1, row, 1, 1)

        # Start time
        start_time_label = Gtk.Label(label="Start Time:")
        start_time_label.set_halign(Gtk.Align.END)
        grid.attach(start_time_label, 2, row, 1, 1)

        self.start_time_entry = Gtk.Entry()
        self.start_time_entry.set_text("00:00:00")
        self.start_time_entry.set_placeholder_text("HH:MM:SS")
        grid.attach(self.start_time_entry, 3, row, 1, 1)
        row += 1

        # End date
        end_label = Gtk.Label(label="End Date:")
        end_label.set_halign(Gtk.Align.END)
        grid.attach(end_label, 0, row, 1, 1)

        self.end_date_entry = Gtk.Entry()
        default_end = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        self.end_date_entry.set_text(default_end)
        self.end_date_entry.set_placeholder_text("YYYY-MM-DD")
        grid.attach(self.end_date_entry, 1, row, 1, 1)

        # End time
        end_time_label = Gtk.Label(label="End Time:")
        end_time_label.set_halign(Gtk.Align.END)
        grid.attach(end_time_label, 2, row, 1, 1)

        self.end_time_entry = Gtk.Entry()
        self.end_time_entry.set_text("23:59:59")
        self.end_time_entry.set_placeholder_text("HH:MM:SS")
        grid.attach(self.end_time_entry, 3, row, 1, 1)
        row += 1

        # Separator
        separator2 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(separator2, 0, row, 4, 1)
        row += 1

        # Satellite selection
        satellite_label = Gtk.Label()
        satellite_label.set_markup("<b>Satellite Selection</b>")
        satellite_label.set_halign(Gtk.Align.START)
        grid.attach(satellite_label, 0, row, 4, 1)
        row += 1

        sat_select_label = Gtk.Label(label="Select Satellite:")
        sat_select_label.set_halign(Gtk.Align.END)
        grid.attach(sat_select_label, 0, row, 1, 1)

        # Create satellite dropdown
        self.satellite_combo = Gtk.ComboBoxText()
        for sat_name in AST_SATELLITES.keys():
            self.satellite_combo.append_text(sat_name)
        self.satellite_combo.set_active(0)
        grid.attach(self.satellite_combo, 1, row, 2, 1)
        row += 1

        # Separator
        separator3 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(separator3, 0, row, 4, 1)
        row += 1

        # Generate button
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        button_box.set_halign(Gtk.Align.CENTER)

        self.generate_button = Gtk.Button(label="Generate Analysis")
        self.generate_button.connect("clicked", self.on_generate_clicked)
        self.generate_button.get_style_context().add_class("suggested-action")
        button_box.pack_start(self.generate_button, False, False, 0)

        clear_button = Gtk.Button(label="Clear Results")
        clear_button.connect("clicked", self.on_clear_clicked)
        button_box.pack_start(clear_button, False, False, 0)

        grid.attach(button_box, 0, row, 4, 1)

        return grid

    def create_results_section(self):
        """Create the results notebook with tabs"""
        notebook = Gtk.Notebook()

        # Tab 1: Pass Table
        scrolled_table = Gtk.ScrolledWindow()
        scrolled_table.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.pass_table = self.create_pass_table()
        scrolled_table.add(self.pass_table)
        notebook.append_page(scrolled_table, Gtk.Label(label="Pass Summary"))

        # Tab 2: Detailed Data Table
        scrolled_data = Gtk.ScrolledWindow()
        scrolled_data.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.data_table = self.create_data_table()
        scrolled_data.add(self.data_table)
        notebook.append_page(scrolled_data, Gtk.Label(label="Detailed Data"))

        # Tab 3: Plots
        plot_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.plot_canvas = self.create_plot_section()
        plot_box.pack_start(self.plot_canvas, True, True, 0)
        notebook.append_page(plot_box, Gtk.Label(label="Visualization"))

        return notebook

    def create_pass_table(self):
        """Create the pass summary table"""
        # ListStore: Pass#, Start Time, End Time, Duration, Max Elev, Max Signal, Avg SNR
        liststore = Gtk.ListStore(int, str, str, str, float, float, float)
        treeview = Gtk.TreeView(model=liststore)

        columns = [
            ("Pass #", 0),
            ("Start Time (UTC)", 1),
            ("End Time (UTC)", 2),
            ("Duration", 3),
            ("Max Elev (°)", 4),
            ("Max Signal (dBm)", 5),
            ("Avg SNR (dB)", 6),
        ]

        for title, col_id in columns:
            if col_id in [4, 5, 6]:  # Numeric columns
                renderer = Gtk.CellRendererText()
                column = Gtk.TreeViewColumn(title, renderer, text=col_id)
                column.set_cell_data_func(renderer, self.format_float, col_id)
            else:
                renderer = Gtk.CellRendererText()
                column = Gtk.TreeViewColumn(title, renderer, text=col_id)
            column.set_resizable(True)
            column.set_sort_column_id(col_id)
            treeview.append_column(column)

        self.pass_liststore = liststore
        return treeview

    def create_data_table(self):
        """Create the detailed data table"""
        # ListStore: Time, Elevation, Azimuth, Range, Signal, SNR, Link Quality
        liststore = Gtk.ListStore(str, float, float, float, float, float, str)
        treeview = Gtk.TreeView(model=liststore)

        columns = [
            ("Timestamp (UTC)", 0),
            ("Elevation (°)", 1),
            ("Azimuth (°)", 2),
            ("Range (km)", 3),
            ("Signal (dBm)", 4),
            ("SNR (dB)", 5),
            ("Link Quality", 6),
        ]

        for title, col_id in columns:
            if col_id in [1, 2, 3, 4, 5]:  # Numeric columns
                renderer = Gtk.CellRendererText()
                column = Gtk.TreeViewColumn(title, renderer, text=col_id)
                column.set_cell_data_func(renderer, self.format_float, col_id)
            else:
                renderer = Gtk.CellRendererText()
                column = Gtk.TreeViewColumn(title, renderer, text=col_id)
            column.set_resizable(True)
            column.set_sort_column_id(col_id)
            treeview.append_column(column)

        self.data_liststore = liststore
        return treeview

    def create_plot_section(self):
        """Create the matplotlib plot section"""
        self.figure = Figure(figsize=(12, 8))
        canvas = FigureCanvas(self.figure)
        canvas.set_size_request(800, 600)
        return canvas

    def format_float(self, column, cell, model, iter, col_id):
        """Format float values in tables"""
        value = model.get_value(iter, col_id)
        if value is not None and not np.isnan(value):
            cell.set_property("text", f"{value:.2f}")
        else:
            cell.set_property("text", "N/A")

    def update_status(self, message):
        """Update the status bar"""
        self.statusbar.pop(self.context_id)
        self.statusbar.push(self.context_id, message)

    def on_generate_clicked(self, button):
        """Handle Generate button click"""
        try:
            self.update_status("Generating analysis...")
            self.generate_button.set_sensitive(False)

            # Process in idle to keep UI responsive
            GLib.idle_add(self.generate_analysis)

        except Exception as e:
            self.show_error_dialog(f"Error: {str(e)}")
            self.generate_button.set_sensitive(True)

    def generate_analysis(self):
        """Generate the satellite analysis"""
        try:
            # Get parameters
            latitude = float(self.lat_entry.get_text())
            longitude = float(self.lon_entry.get_text())
            elevation_m = float(self.elev_entry.get_text())

            start_date_str = self.start_date_entry.get_text()
            start_time_str = self.start_time_entry.get_text()
            end_date_str = self.end_date_entry.get_text()
            end_time_str = self.end_time_entry.get_text()

            start_datetime = datetime.strptime(f"{start_date_str} {start_time_str}", "%Y-%m-%d %H:%M:%S")
            end_datetime = datetime.strptime(f"{end_date_str} {end_time_str}", "%Y-%m-%d %H:%M:%S")

            satellite_name = self.satellite_combo.get_active_text()
            satellite_info = AST_SATELLITES[satellite_name]

            self.update_status(f"Fetching TLE data for {satellite_name}...")

            # Fetch TLE
            name, line1, line2 = fetch_tle_data(satellite_info["norad_id"])
            if not line1 or not line2:
                self.update_status(f"Could not fetch TLE, using simulated data...")
                name, line1, line2 = create_simulated_tle(satellite_info["norad_id"], satellite_name)

            # Create satellite object
            ts = load.timescale()
            satellite = EarthSatellite(line1, line2, name, ts)

            # Create observer
            observer = wgs84.latlon(latitude, longitude, elevation_m)

            self.update_status("Calculating satellite positions...")

            # Generate positions
            positions = generate_satellite_passes(satellite, observer, start_datetime, end_datetime)

            # Identify passes
            self.current_passes = identify_passes(positions)
            self.current_data = positions

            self.update_status(f"Found {len(self.current_passes)} passes. Updating display...")

            # Update displays
            self.update_pass_table()
            self.update_data_table()
            self.update_plots()

            self.update_status(f"Analysis complete. Found {len(self.current_passes)} passes over {satellite_name}.")

        except ValueError as e:
            self.show_error_dialog(f"Invalid input: {str(e)}")
        except Exception as e:
            self.show_error_dialog(f"Error during analysis: {str(e)}")
        finally:
            self.generate_button.set_sensitive(True)

        return False  # Don't repeat

    def update_pass_table(self):
        """Update the pass summary table"""
        self.pass_liststore.clear()

        for i, pass_data in enumerate(self.current_passes, 1):
            start_time = datetime.fromisoformat(pass_data[0]["timestamp"])
            end_time = datetime.fromisoformat(pass_data[-1]["timestamp"])
            duration_secs = len(pass_data) * 5
            duration_str = f"{duration_secs // 60}m {duration_secs % 60}s"

            max_elev = max(p["elevation_deg"] for p in pass_data)
            signal_powers = [p["received_power_dbm"] for p in pass_data if p["received_power_dbm"]]
            max_signal = max(signal_powers) if signal_powers else 0
            snr_values = [p["snr_db"] for p in pass_data if p["snr_db"]]
            avg_snr = np.mean(snr_values) if snr_values else 0

            self.pass_liststore.append([
                i,
                start_time.strftime("%Y-%m-%d %H:%M:%S"),
                end_time.strftime("%H:%M:%S"),
                duration_str,
                max_elev,
                max_signal,
                avg_snr,
            ])

    def update_data_table(self):
        """Update the detailed data table"""
        self.data_liststore.clear()

        # Show data from first pass (or all visible positions)
        if self.current_passes:
            data_to_show = self.current_passes[0]  # First pass
        else:
            data_to_show = [p for p in self.current_data if p["visible"]][:100]  # First 100 visible

        for pos in data_to_show:
            timestamp = datetime.fromisoformat(pos["timestamp"])
            self.data_liststore.append([
                timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                pos["elevation_deg"],
                pos["azimuth_deg"],
                pos["range_km"],
                pos["received_power_dbm"] if pos["received_power_dbm"] else 0,
                pos["snr_db"] if pos["snr_db"] else 0,
                pos["link_quality"],
            ])

    def update_plots(self):
        """Update the visualization plots"""
        self.figure.clear()

        if not self.current_passes:
            return

        # Plot first pass
        pass_data = self.current_passes[0]
        timestamps = [datetime.fromisoformat(p["timestamp"]) for p in pass_data]
        elevations = [p["elevation_deg"] for p in pass_data]
        signal_powers = [p["received_power_dbm"] if p["received_power_dbm"] else 0 for p in pass_data]
        snr_values = [p["snr_db"] if p["snr_db"] else 0 for p in pass_data]
        ranges = [p["range_km"] for p in pass_data]

        # Create 4 subplots
        ax1 = self.figure.add_subplot(2, 2, 1)
        ax1.plot(timestamps, elevations, "b-", linewidth=2)
        ax1.set_ylabel("Elevation (°)", fontsize=10)
        ax1.set_title("Elevation Angle", fontsize=11, fontweight="bold")
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis="x", rotation=45)

        ax2 = self.figure.add_subplot(2, 2, 2)
        ax2.plot(timestamps, signal_powers, "g-", linewidth=2)
        ax2.set_ylabel("Power (dBm)", fontsize=10)
        ax2.set_title("Received Signal Power", fontsize=11, fontweight="bold")
        ax2.grid(True, alpha=0.3)
        ax2.tick_params(axis="x", rotation=45)

        ax3 = self.figure.add_subplot(2, 2, 3)
        ax3.plot(timestamps, snr_values, "r-", linewidth=2)
        ax3.set_ylabel("SNR (dB)", fontsize=10)
        ax3.set_xlabel("Time (UTC)", fontsize=10)
        ax3.set_title("Signal-to-Noise Ratio", fontsize=11, fontweight="bold")
        ax3.grid(True, alpha=0.3)
        ax3.tick_params(axis="x", rotation=45)

        ax4 = self.figure.add_subplot(2, 2, 4)
        ax4.plot(timestamps, ranges, "m-", linewidth=2)
        ax4.set_ylabel("Range (km)", fontsize=10)
        ax4.set_xlabel("Time (UTC)", fontsize=10)
        ax4.set_title("Satellite Range", fontsize=11, fontweight="bold")
        ax4.grid(True, alpha=0.3)
        ax4.tick_params(axis="x", rotation=45)

        self.figure.tight_layout()
        self.plot_canvas.draw()

    def on_clear_clicked(self, button):
        """Handle Clear button click"""
        self.pass_liststore.clear()
        self.data_liststore.clear()
        self.figure.clear()
        self.plot_canvas.draw()
        self.current_data = None
        self.current_passes = None
        self.update_status("Results cleared")

    def show_error_dialog(self, message):
        """Show an error dialog"""
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text="Error",
        )
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()


def main():
    app = SatelliteAnalysisApp()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
