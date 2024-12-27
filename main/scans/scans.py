import flet as ft
import firebase_admin
from firebase_admin import credentials, firestore
import re
import time
import locale  # Used to format balance and numbers
from datetime import date
import subprocess
import random
import threading
import os
from dotenv import load_dotenv
load_dotenv()

WP_API_TOKEN = os.getenv("WP_API_TOKEN")
OWASP_ZAP_API_KEY = os.getenv("OWASP_ZAP_API_KEY")
database = os.getenv("database")

locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

# Initialize Firebase Admin
if not firebase_admin._apps:
    cred = credentials.Certificate(fr"{database}")
    firebase_admin.initialize_app(cred)

db = firestore.client()


# Function to save a new folder to Firebase
def save_folder_to_firebase(folder_name):
    doc_ref = db.collection("Cyber-Folders").document()
    doc_ref.set({"name": folder_name})
    return doc_ref.id


def main(page: ft.Page) -> None:
    page.title = "Scans"

    def on_dashboard_click(e):
        e.page.go("/dashboard")

    def on_start_scan_click(e):
        e.page.go("/scans")

    def on_manage_targets_click(e):
        e.page.go("/targets")

    def integration_click(e):
        e.page.go("/integration")

    def reports_click(e):
        e.page.go("/reports")

    base_chart_style: dict = {
        "expand": True,
        "tooltip_bgcolor": ft.colors.with_opacity(0.8, ft.colors.WHITE),
        "left_axis": ft.ChartAxis(labels_size=50, show_labels=False),  # Set label color to black
        "bottom_axis": ft.ChartAxis(labels_interval=1, labels_size=40, show_labels=False),
        # Set label color to black
        "horizontal_grid_lines": ft.ChartGridLines(
            interval=10, color=ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE),
            width=1,
        ),
    }

    class BaseChart(ft.LineChart):
        def __init__(self, line_color: str) -> None:
            super().__init__(**base_chart_style)

            self.points: list = []
            self.min_x = (
                int(min(self.points, key=lambda x: x[0][0])) if self.points else None
            )

            self.max_x = (
                int(min(self.points, key=lambda x: x[0][0])) if self.points else None
            )

            self.line = ft.LineChartData(
                color=line_color,
                stroke_width=2,
                curved=True,
                stroke_cap_round=True,
                below_line_gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                    colors=[
                        ft.colors.with_opacity(0.25, line_color),
                        "transparent"
                    ],
                ),
            )

            self.line.data_points = self.points
            self.data_series = [self.line]

        def create_data_point(self, x, y):
            self.points.append(
                ft.LineChartDataPoint(
                    x, y,
                    selected_below_line=ft.ChartPointLine(
                        width=0.5, color="white54", dash_pattern=[2, 4]
                    ),
                    selected_point=ft.ChartCirclePoint(stroke_width=1),
                ),
            )

            self.update()

    in_style: dict = {
        "expand": True,
        # "bgcolor": "#17171d",
        "border_radius": 10,
        "padding": 30,
    }

    class GraphIn(ft.Container):
        def __init__(self) -> None:
            super().__init__(**in_style)
            self.chart = BaseChart(line_color="teal600")
            self.content = self.chart

    out_style: dict = {
        "expand": True,
        "bgcolor": "#17171d",
        "border_radius": 10,
        "padding": 30,
    }

    class GraphOut(ft.Container):
        def __init__(self) -> None:
            super().__init__(**out_style)
            self.content = ft.Container(
                ft.Column(
                    controls=[
                        ft.Text("Last Scan", size=18, weight=ft.FontWeight.BOLD, color="white"),
                        ft.Text("Policy:  API Security Tests", color="white"),
                        ft.Text("Status:  Completed", color="white"),
                        ft.Text("Security Base:  CVSS v1.0", color="white"),
                        ft.Text("Scanner:  Local Scanner", color="white"),
                        ft.Text(f"Start:  {date.today().strftime('%b-%d')} at {time.strftime('%H:%M %p', time.localtime())}", color="white"),
                        ft.Text(f"End:  {date.today().strftime('%b-%d')}", color="white"),
                        ft.Text("Elapsed:  23 mins", color="white"),
                        ft.Divider(height=20),
                    ]
                ),
            )

        def update_scan_details(self):
            self.content = self.create_scan_details()  # Update with scan details
            self.update()  # Refresh the container

        def create_scan_details(self) -> ft.Column:
            return ft.Column(
                controls=[
                    ft.Text("Scan Details", size=18, weight=ft.FontWeight.BOLD, color="white"),
                    ft.Column(
                        controls=[
                            ft.Text("Policy:  Web Application Tests", color="white"),
                            ft.Text("Status:  Completed", color="white"),
                            ft.Text("Security Base:  CVSS v3.0", color="white"),
                            ft.Text("Scanner:  Local Scanner", color="white"),
                            ft.Text(f"Start:  {date.today().strftime('%b-%d')} at {time.strftime('%H:%M %p', time.localtime())}", color="white"),
                            ft.Text(f"End:  {date.today().strftime('%b-%d')}", color="white"),
                            ft.Text("Elapsed:  2 mins", color="white"),
                            ft.Divider(height=20),
                        ]
                    ),
                ]
            )

    tracker_style: dict = {
        "main": {
            "expand": True,
            "bgcolor": "#17181d",
            "border_radius": 10
        },
        "balance": {
            "size": 48,
            "weight": "bold",
        },
        "input": {
            "width": 220,
            "height": 40,
            "border_color": "white12",
            "cursor_height": 16,
            "cursor_color": "white12",
            "content_padding": 10,
            "text_align": "center",
        },
        "add": {
            "icon": ft.icons.ADD,
            "bgcolor": "#1f2128",
            "icon_size": 16,
            "icon_color": "teal600",
            "scale": ft.transform.Scale(0.8),
        },
        "subtract": {
            "icon": ft.icons.REMOVE,
            "bgcolor": "#1f2128",
            "icon_size": 16,
            "icon_color": "red600",
            "scale": ft.transform.Scale(0.8),
        },
        "data_table": {
            "columns": [
                ft.DataColumn(ft.Text("Timestamp", weight=ft.FontWeight.W_900)),
                ft.DataColumn(ft.Text("Amount", weight=ft.FontWeight.W_900), numeric=True),
            ],
            "width": 380,
            "heading_row_height": 35,
            "data_row_max_height": 40,
        },
        "data_table_container": {
            "expand": True,
            "width": 450,
            "padding": 10,
            "border_radius": ft.border_radius.only(top_left=10, top_right=10),
            "shadow": ft.BoxShadow(
                spread_radius=8,
                blur_radius=15,
                color=ft.colors.with_opacity(0.15, "black"),
                offset=ft.Offset(4, 4),
            ),
            "bgcolor": ft.colors.with_opacity(0.75, "#1f2128"),
        },
    }

    class Tracker(ft.Container):
        def __init__(self, _in: object, _out: object) -> None:
            super().__init__(**tracker_style.get("main"))
            self._in: object = _in
            self._out: object = _out

            self.counter = 0.0
            self.balance = ft.Text(
                locale.currency(self.counter, grouping=True),
                **tracker_style.get("balance")
            )

            self.input = ft.TextField(**tracker_style.get("input"))
            self.add = ft.IconButton(
                **tracker_style.get("add"),
                data=True,
                on_click=lambda e: self.update_balance(e),
            )
            self.subtract = ft.IconButton(
                **tracker_style.get("subtract"),
                data=False,
                on_click=lambda e: self.update_balance(e),
            )

            self.table = ft.DataTable(**tracker_style.get("data_table"))

            self.content = ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Divider(height=15, color="transparent"),
                    ft.Text("Balance", size=11, weight=ft.FontWeight.W_900),
                    ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[self.balance]),
                    ft.Divider(height=15, color="transparent"),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            self.subtract,
                            self.input,
                            self.add
                        ],
                    ),
                    ft.Divider(height=25, color="transparent"),
                    ft.Container(
                        **tracker_style.get("data_table_container"),
                        content=ft.Column(
                            expand=True,
                            controls=[
                                self.table
                            ]
                        )
                    )
                ]
            )

            self.x = 0
            self.stop_event = threading.Event()  # Create a stop event

        def update_data_table(self, amount: float, sign: bool) -> None:
            timestamp = int(time.time())
            data = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(timestamp)),
                    ft.DataCell(
                        ft.Text(
                            locale.currency(amount, grouping=True),
                            color="teal" if sign else "red",
                        )
                    ),
                ]
            )

            self.table.rows.append(data)

            return timestamp

        def update_balance(self):
            while not self.stop_event.is_set():  # Check if the stop event is set
                delta = random.randrange(0, 10)
                self.counter += delta
                time.sleep(2)
                self.update_data_table(delta, sign=True)
                self._in.chart.create_data_point(
                    x=self.x,
                    y=delta
                )

                self.x += 1

                # Updating the page
                self.balance.value = locale.currency(self.counter, grouping=True)
                self.input.value = ""  # Clears input field

    def dark_mode(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            dark_btn.icon = ft.icons.LIGHT_MODE  # Update the icon to indicate light mode
        else:
            page.theme_mode = ft.ThemeMode.DARK
            dark_btn.icon = ft.icons.DARK_MODE  # Update the icon to indicate dark mode
        page.update()

    dark_btn = ft.IconButton(
        icon=ft.icons.DARK_MODE,
        icon_size=20,
        on_click=dark_mode,
    )

    graph_in: ft.Container = GraphIn()
    graph_out: ft.Container = GraphOut()
    tracker: ft.Container = Tracker(_in=graph_in, _out=graph_out)

    sidebar_content = ft.Container(
        width=250,
        bgcolor="#1e1e2f",
        padding=20,
        border_radius=ft.border.only(right=ft.border.BorderSide(1, "white")),
        content=ft.Column(
            controls=[
                ft.Text("CyberSpace", size=30, weight=ft.FontWeight.BOLD, color="white"),
                ft.Divider(height=20, color="transparent"),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.DASHBOARD, color="white"),
                    title=ft.Text("Dashboard", color="white"),
                    on_click=lambda e: on_dashboard_click(e),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.GPS_FIXED, color="white"),
                    title=ft.Text("Targets", color="white"),
                    on_click=lambda e: on_manage_targets_click(e)
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.SCANNER, color="white"),
                    title=ft.Text("Scans", color="white"),
                    on_click=lambda e: on_start_scan_click(e)
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.INTEGRATION_INSTRUCTIONS, color="white"),
                    title=ft.Text("Integrations", color="white"),
                    on_click=lambda e: integration_click(e)
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.REPORT, color="white"),
                    title=ft.Text("Reports", color="white"),
                    on_click=lambda e: reports_click(e)
                ),
            ],
        ),
    )

    scan_content = ft.Column(
        controls=[
            ft.Column(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text("Critical", color="red"),
                            ft.Text("Server Side Template Injection", size=14),
                            ft.Text("22 Jan, 2024", size=12),
                            ft.Text("8.3", size=12),
                        ],
                    ),
                    ft.Divider(height=10, color="transparent"),
                    ft.Column(
                        controls=[
                            ft.Text("Critical", color="red"),
                            ft.Text("Pharmacy Information Schema Disclosure", size=14),
                            ft.Text("16 Jan, 2024", size=12),
                            ft.Text("8.0", size=12),
                        ],
                    ),
                    ft.Divider(height=10, color="transparent"),
                    ft.Column(
                        controls=[
                            ft.Text("Critical", color="red"),
                            ft.Text(".env/files Found", size=14),
                            ft.Text("2 Feb, 2024", size=12),
                            ft.Text("7.9", size=12),
                        ],
                    ),
                    ft.Divider(height=10, color="transparent"),
                    ft.Column(
                        controls=[
                            ft.Text("High", color="orange"),
                            ft.Text("PII Disclosure", size=14),
                            ft.Text("1 Feb, 2024", size=12),
                            ft.Text("5.8", size=12),
                        ],
                    ),
                    ft.Divider(height=10, color="transparent"),
                    ft.Column(
                        controls=[
                            ft.Text("High", color="orange"),
                            ft.Text("Source Code Disclosure - File Inclusion", size=14),
                            ft.Text("1 Feb, 2024", size=12),
                            ft.Text("4.7", size=12),
                        ],
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            ),
            ft.Divider(height=10, color="transparent"),  # Final Divider
        ]
    )

    scan_output_view = ft.ListView(  # Using ListView to enable scrolling
        height=400,
        width=600,
        padding=10,
        expand=True,
        controls=[
            scan_content
        ]
    )

    def start_scan(e):
        graph_out.content = ft.Container(
            bgcolor="#2c2f38",  # Dark background for the container
            border_radius=10,
            padding=10,
            content=ft.Column(
                controls=[
                    ft.Text("Scanning Target", size=24, weight=ft.FontWeight.BOLD, color="white"),  # Increased font size and weight
                    ft.Divider(height=10, color="white"),  # Divider for separation
                    ft.Row(
                        controls=[
                            ft.Icon(ft.icons.API, size=20, color="white"),  # Scanner icon
                            ft.Text(f"{input_field.value}", size=18, color="white"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                    ft.ProgressBar(width=300),
                    ft.Divider(height=30, color=ft.colors.TRANSPARENT),
                    ft.Text("Scanning in progress...", size=16, color="white", weight="medium"),  # Status message
                    ft.Text("Please wait while we gather the results...", size=14, color="white"),
                    # Additional info
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,  # Space between controls
            ),
        )
        page.update()  # Update the page to reflect changes

        threading.Thread(target=tracker.update_balance).start()

        page.snack_bar = ft.SnackBar(
            ft.Column([
                ft.Row([
                    ft.Text("Scanning... Please wait!", size=30, color="black"),
                    ft.ProgressRing(color="black")
                ], alignment=ft.MainAxisAlignment.CENTER)
            ], alignment=ft.MainAxisAlignment.CENTER),
            bgcolor="#7df6dd"
        )
        page.snack_bar.open = True
        page.update()

        def strip_ansi_codes(text):
            ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
            return ansi_escape.sub("", text)

        # Run the scan
        rapidscan_path = r"C:\Users\WISDOM\Documents\rapidscan-master\rapidscan.py"
        target_url = tracker.input.value

        _output = subprocess.run(
            f"py {rapidscan_path} http://hackthissite.com --skip nmap",
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        clean_output = strip_ansi_codes(_output.stdout)

        # Clear previous results and update the scan_output_view with the actual results
        scan_output_view.controls.clear()  # Clear any previous output
        scan_output_view.controls.append(
            ft.Text(value=clean_output, size=15, selectable=True)
        )
        page.update()

        # Stop the update_balance loop
        tracker.stop_event.set()  # Signal to stop the loop

        # Update the graph_out with scan details
        graph_out.update_scan_details()

        page.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Scan Complete"),
            content=ft.Text(f"Scan saved with ID: {232}"),
            actions=[
                ft.TextButton(
                    "OK",
                    on_click=close_dialog
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog.open = True
        page.update()

    # Function to close the dialog
    def close_dialog(e=None):
        page.dialog.open = False  # Close the dialog
        page.update()  # Update the page to reflect the changes

    # Create the TextField separately
    input_field = ft.TextField(label="Enter a web URL to scan")

    scans_content = ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Automated App Scan (Full)", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(height=10),
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                input_field,
                                ft.ElevatedButton(
                                    "Scan",
                                    on_click=start_scan,
                                    style=ft.ButtonStyle(
                                        shape={"": ft.RoundedRectangleBorder(radius=8)},
                                        color={"": "black"},
                                        bgcolor={"": "#7df6dd"},
                                    ),
                                ),
                            ]
                        ),
                        ft.Divider(height=5),
                        ft.Row(
                            controls=[
                                ft.Text("In Progress -", size=16),
                                ft.ElevatedButton(f"Date: {date.today().strftime('%b-%d-%Y')}", color="black",
                                                  bgcolor="#7df6dd"),
                                ft.ElevatedButton(f"Time: {time.strftime('%H:%M %p', time.localtime())}", color="black",
                                                  bgcolor="#7df6dd")
                            ]
                        ),
                    ]
                ),
                ft.Divider(height=5),
                ft.Text("Major Identified Risks", size=18, weight=ft.FontWeight.BOLD),  # Title
                ft.Divider(height=5, color="transparent"),  # Divider
                scan_output_view
            ],
        ),
    )

    page.update()

    return ft.View(
        "/scans",
        controls=[
            ft.Row(
                controls=[
                    sidebar_content,
                    ft.VerticalDivider(width=1, color=ft.colors.TRANSPARENT),
                    scans_content,
                    ft.Column(
                        expand=True,
                        controls=[graph_in, graph_out]
                    ),
                    ft.Container(
                        content=dark_btn,
                        alignment=ft.alignment.top_right,
                        padding=ft.padding.only(left=0, top=20),
                    ),
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.START,
            )
        ]
    )