import time
import threading
import flet as ft
import subprocess
import os
import json
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


class State:
    toggle = True


s = State()


def main(page: ft.Page):
    page.title = "Dashboard"

    # Define your metrics
    total_scans = 10
    high_severity_count = 2
    potential_loss_saved = 289

    def animate_number(target: ft.Text, end_value: int, duration: float, dollar_sign: bool = False):
        for i in range(end_value + 1):
            if dollar_sign:
                target.value = "$" + str(i)
            else:
                target.value = str(i)
            target.update()  # Update the UI immediately to reflect the new value
            time.sleep(duration / end_value)  # Adjust the speed of counting

    # Start the counting animations in a separate thread when the page is ready
    def start_counting():
        time.sleep(1)  # Optional delay before counting starts
        animate_number(total_scans_text, total_scans, 2.0)  # Count to total scans in 2 seconds
        animate_number(high_severity_text, high_severity_count, 2.0)  # Count to high severity in 2 seconds
        animate_number(potential_loss_text, potential_loss_saved, 2.0, dollar_sign=True)  # Count to potential loss in 2 seconds

    threading.Thread(target=start_counting, daemon=True).start()

    def on_signup_click(e):
        e.page.go("/signup")

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

    def dark_mode(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            dark_btn.icon = ft.icons.LIGHT_MODE
        else:
            page.theme_mode = ft.ThemeMode.DARK
            dark_btn.icon = ft.icons.DARK_MODE
        page.update()

    dark_btn = ft.IconButton(
        icon=ft.icons.DARK_MODE,
        icon_size=20,
        on_click=dark_mode,
    )

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
                    on_click=on_dashboard_click,
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.GPS_FIXED, color="white"),
                    title=ft.Text("Targets", color="white"),
                    on_click=on_manage_targets_click
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.SCANNER, color="white"),
                    title=ft.Text("Scans", color="white"),
                    on_click=on_start_scan_click
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.INTEGRATION_INSTRUCTIONS, color="white"),
                    title=ft.Text("Integrations", color="white"),
                    on_click=integration_click,
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.REPORT, color="white"),
                    title=ft.Text("Reports", color="white"),
                    on_click=reports_click
                ),
                ft.Divider(height=250, color=ft.colors.TRANSPARENT),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.ARROW_BACK_ROUNDED, color="white"),
                    title=ft.Text("Log Out", color="white"),
                    on_click=on_signup_click
                )
            ],
        ),
    )

    vulnerabilities_content = ft.Row(
        controls=[
            ft.ListView(
                height=300,
                padding=10,
                expand=True,
                auto_scroll=True,
                controls=[
                    ft.Card(
                        content=ft.Container(
                            padding=10,
                            content=ft.Column(
                                controls=[
                                    ft.Text("#8793 - Server Side Template Injection", weight=ft.FontWeight.BOLD),
                                    ft.Text("22 Jan, 12:11 PM"),
                                    ft.Row(
                                        controls=[
                                            ft.Text("Critical", color=ft.colors.RED),
                                            ft.Icon(ft.icons.WARNING, color=ft.colors.RED),
                                        ],
                                    ),
                                ],
                            ),
                        ),
                        width=200,  # Adjust width as needed
                    ),
                    ft.Card(
                        content=ft.Container(
                            padding=10,
                            content=ft.Column(
                                controls=[
                                    ft.Text("#8793 - PII Disclosure", weight=ft.FontWeight.BOLD),
                                    ft.Text("16 Jan, 4:18 PM"),
                                    ft.Row(
                                        controls=[
                                            ft.Text("Medium", color=ft.colors.ORANGE),
                                            ft.Icon(ft.icons.WARNING, color=ft.colors.ORANGE),
                                        ],
                                    ),
                                ],
                            ),
                        ),
                        width=200,
                    ),
                    ft.Card(
                        content=ft.Container(
                            padding=10,
                            content=ft.Column(
                                controls=[
                                    ft.Text("#8793 - .svn/entries Found", weight=ft.FontWeight.BOLD),
                                    ft.Text("21 Jun, 4:48 PM"),
                                    ft.Row(
                                        controls=[
                                            ft.Text("Low", color=ft.colors.GREEN),
                                            ft.Icon(ft.icons.INFO, color=ft.colors.GREEN),
                                        ],
                                    ),
                                ],
                            ),
                        ),
                        width=200,
                    ),
                    ft.Card(
                        content=ft.Container(
                            padding=10,
                            content=ft.Column(
                                controls=[
                                    ft.Text("#8793 - JSON Web Key Set Disclosed", weight=ft.FontWeight.BOLD),
                                    ft.Text("6 Feb, 9:18 AM"),
                                    ft.Row(
                                        controls=[
                                            ft.Text("High", color=ft.colors.ORANGE),
                                            ft.Icon(ft.icons.WARNING, color=ft.colors.ORANGE),
                                        ],
                                    ),
                                ],
                            ),
                        ),
                        width=200,
                    ),
                    ft.Card(
                        content=ft.Container(
                            padding=10,
                            content=ft.Column(
                                controls=[
                                    ft.Text("#8793 - WordPress Database Backup File Found", weight=ft.FontWeight.BOLD),
                                    ft.Text("6 Feb, 9:20 AM"),
                                    ft.Row(
                                        controls=[
                                            ft.Text("High", color=ft.colors.ORANGE),
                                            ft.Icon(ft.icons.WARNING, color=ft.colors.ORANGE),
                                        ],
                                    ),
                                ],
                            ),
                        ),
                        width=200,
                    ),
                ]
            )
        ],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,  # Adjust spacing as needed
    )

    total_scans_text = ft.Text("0", size=20, weight=ft.FontWeight.BOLD)
    high_severity_text = ft.Text("0", size=20, weight=ft.FontWeight.BOLD)
    potential_loss_text = ft.Text("$0", size=20, weight=ft.FontWeight.BOLD)

    dashboard_content = ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Dashboard Overview", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(height=10),
                ft.Text("Welcome to an overview of your dashboard.", size=16),
                ft.Divider(height=5, color=ft.colors.TRANSPARENT),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            "Start Scan",
                            on_click=on_start_scan_click,
                            style=ft.ButtonStyle(
                                shape={"": ft.RoundedRectangleBorder(radius=8)},
                                color={"": "black"},
                                bgcolor={"": "#7df6dd"},
                            )
                        ),
                        ft.VerticalDivider(width=2, color=ft.colors.TRANSPARENT),
                        ft.ElevatedButton(
                            "Manage Targets",
                            on_click=on_manage_targets_click,
                            style=ft.ButtonStyle(
                                shape={"": ft.RoundedRectangleBorder(radius=8)},
                                color={"": "black"},
                                bgcolor={"": "#7df6dd"},
                            )
                        )
                    ]
                ),
                ft.Divider(height=10),
                ft.Text("Quick Stats", size=18, weight=ft.FontWeight.BOLD),
                ft.Row(
                    controls=[
                        ft.Card(
                            content=ft.Container(
                                padding=20,
                                content=ft.Column(
                                    controls=[
                                        ft.Row([ft.Icon(ft.icons.FILE_OPEN, color=ft.colors.BLUE_ACCENT),
                                                ft.Text("Total Scans", size=16)]),
                                        total_scans_text
                                    ],
                                ),
                            )
                        ),
                        ft.Card(
                            content=ft.Container(
                                padding=20,
                                content=ft.Column(
                                    controls=[
                                        ft.Row([ft.Icon(ft.icons.WARNING, color=ft.colors.RED_ACCENT),
                                                ft.Text("High Severity", size=16)]),
                                        high_severity_text
                                    ],
                                ),
                            )
                        ),
                        ft.Card(
                            content=ft.Container(
                                padding=20,
                                content=ft.Column(
                                    controls=[
                                        ft.Row([ft.Icon(ft.icons.MONETIZATION_ON, color="green"),
                                                ft.Text("Potential Loss Saved", size=16)]),
                                        potential_loss_text
                                    ]
                                )
                            )
                        )
                    ],
                ),
                ft.Card(
                    content=ft.Container(
                        padding=20,
                        height=360,
                        width=590,
                        content=ft.Column(
                            controls=[
                                ft.Text("Vulnerabilities (5)", weight=ft.FontWeight.BOLD, size=16),
                                vulnerabilities_content
                            ]
                        )
                    )
                )
            ],
        ),
    )

    data_1 = [
        ft.LineChartData(
            data_points=[
                ft.LineChartDataPoint(1, 1),
                ft.LineChartDataPoint(3, 1.5),
                ft.LineChartDataPoint(5, 1.4),
                ft.LineChartDataPoint(7, 3.4),
                ft.LineChartDataPoint(10, 2),
                ft.LineChartDataPoint(12, 2.2),
                ft.LineChartDataPoint(13, 1.8),
            ],
            stroke_width=5,
            color=ft.colors.LIGHT_GREEN,
            curved=True,
            stroke_cap_round=True,
        ),
        ft.LineChartData(
            data_points=[
                ft.LineChartDataPoint(1, 1),
                ft.LineChartDataPoint(3, 2.8),
                ft.LineChartDataPoint(7, 1.2),
                ft.LineChartDataPoint(10, 2.8),
                ft.LineChartDataPoint(12, 2.6),
                ft.LineChartDataPoint(13, 3.9),
            ],
            color=ft.colors.PINK,
            below_line_bgcolor=ft.colors.with_opacity(0, ft.colors.PINK),
            stroke_width=5,
            curved=True,
            stroke_cap_round=True,
        ),
        ft.LineChartData(
            data_points=[
                ft.LineChartDataPoint(1, 2.8),
                ft.LineChartDataPoint(3, 1.9),
                ft.LineChartDataPoint(6, 3),
                ft.LineChartDataPoint(10, 1.3),
                ft.LineChartDataPoint(13, 2.5),
            ],
            color=ft.colors.CYAN,
            stroke_width=5,
            curved=True,
            stroke_cap_round=True,
        ),
    ]

    data_2 = [
        ft.LineChartData(
            data_points=[
                ft.LineChartDataPoint(1, 1),
                ft.LineChartDataPoint(3, 4),
                ft.LineChartDataPoint(5, 1.8),
                ft.LineChartDataPoint(7, 5),
                ft.LineChartDataPoint(10, 2),
                ft.LineChartDataPoint(12, 2.2),
                ft.LineChartDataPoint(13, 1.8),
            ],
            stroke_width=4,
            color=ft.colors.with_opacity(0.5, ft.colors.LIGHT_GREEN),
            stroke_cap_round=True,
        ),
        ft.LineChartData(
            data_points=[
                ft.LineChartDataPoint(1, 1),
                ft.LineChartDataPoint(3, 2.8),
                ft.LineChartDataPoint(7, 1.2),
                ft.LineChartDataPoint(10, 2.8),
                ft.LineChartDataPoint(12, 2.6),
                ft.LineChartDataPoint(13, 3.9),
            ],
            color=ft.colors.with_opacity(0.5, ft.colors.PINK),
            below_line_bgcolor=ft.colors.with_opacity(0.2, ft.colors.PINK),
            stroke_width=4,
            curved=True,
            stroke_cap_round=True,
        ),
        ft.LineChartData(
            data_points=[
                ft.LineChartDataPoint(1, 3.8),
                ft.LineChartDataPoint(3, 1.9),
                ft.LineChartDataPoint(6, 5),
                ft.LineChartDataPoint(10, 3.3),
                ft.LineChartDataPoint(13, 4.5),
            ],
            color=ft.colors.with_opacity(0.5, ft.colors.CYAN),
            stroke_width=4,
            stroke_cap_round=True,
        ),
    ]

    chart = ft.LineChart(
        data_series=data_1,
        border=ft.Border(
            bottom=ft.BorderSide(4, ft.colors.with_opacity(0.5, ft.colors.WHITE))
        ),
        left_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=1,
                    label=ft.Text("1", size=10, weight=ft.FontWeight.BOLD, color="white"),
                ),
                ft.ChartAxisLabel(
                    value=2,
                    label=ft.Text("2", size=10, weight=ft.FontWeight.BOLD, color="white"),
                ),
                ft.ChartAxisLabel(
                    value=3,
                    label=ft.Text("3", size=10, weight=ft.FontWeight.BOLD, color="white"),
                ),
                ft.ChartAxisLabel(
                    value=4,
                    label=ft.Text("4", size=10, weight=ft.FontWeight.BOLD, color="white"),
                ),
                ft.ChartAxisLabel(
                    value=5,
                    label=ft.Text("5", size=10, weight=ft.FontWeight.BOLD, color="white"),
                ),
                ft.ChartAxisLabel(
                    value=6,
                    label=ft.Text("6", size=10, weight=ft.FontWeight.BOLD, color="white"),
                ),
            ],
            labels_size=20,
        ),
        bottom_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=2,
                    label=ft.Container(
                        ft.Text(
                            "NOV",
                            size=10,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.with_opacity(0.5, ft.colors.WHITE),
                        ),
                        margin=ft.margin.only(top=10),
                    ),
                ),
                ft.ChartAxisLabel(
                    value=7,
                    label=ft.Container(
                        ft.Text(
                            "DEC",
                            size=10,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.with_opacity(0.5, ft.colors.WHITE),
                        ),
                        margin=ft.margin.only(top=10),
                    ),
                ),
                ft.ChartAxisLabel(
                    value=12,
                    label=ft.Container(
                        ft.Text(
                            "JAN",
                            size=10,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.with_opacity(0.5, ft.colors.WHITE),
                        ),
                        margin=ft.margin.only(top=10),
                    ),
                ),
            ],
            labels_size=32,
        ),
        tooltip_bgcolor=ft.colors.with_opacity(0.8, ft.colors.BLUE_GREY),
        min_y=0,
        max_y=4,
        min_x=0,
        max_x=14,
        # animate=5000,
        expand=True,
    )

    def toggle_data(e):
        if s.toggle:
            chart.data_series = data_2
            chart.data_series[2].point = True
            chart.max_y = 6
            chart.interactive = False
        else:
            chart.data_series = data_1
            chart.max_y = 4
            chart.interactive = True
        s.toggle = not s.toggle
        chart.update()

    progress_content = ft.Card(
        content=ft.Container(
            padding=20,
            bgcolor="#17171d",
            border_radius=10,
            width=300,  # Adjust width as necessary
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("Source", weight=ft.FontWeight.BOLD, size=18, color="white"),
                            ft.VerticalDivider(width=45),
                            ft.Text("Pending Review", color=ft.colors.GREEN_500),
                            ft.Icon(ft.icons.PENDING, color=ft.colors.GREEN_500),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ft.Text("Root Cause Analysis", size=14, color="white"),
                    ft.Text("Reason for Non-conformance: Limited Scope! Fully utilize the functionality of CyberSpace.", size=14, color="white"),
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                "Move to Immediate Action",
                                on_click=integration_click,
                                style=ft.ButtonStyle(
                                    shape={"": ft.RoundedRectangleBorder(radius=8)},
                                    color={"": "black"},
                                    bgcolor={"": "#7df6dd"},
                                )
                            ),
                            ft.IconButton(ft.icons.REFRESH, on_click=toggle_data),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Divider(height=3, color="transparent"),
                    # Additional Sections
                    chart
                ]
            ),
        )
    )

    prompt_view = ft.ListView(
        expand=True,
        controls=[
            progress_content
        ]
    )

    genai_view = ft.ListView(
        padding=10,
        expand=True,
        auto_scroll=True,
        controls=[
            # Gen AI output
        ]
    )

    def prompt_answer(input_text):
        prompt = f'{{"contents":[{{"parts":[{{"text": "{input_text}"}}]}}]}}'
        response = subprocess.run(
            ['curl',
             f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}',
             '-H', 'Content-Type: application/json', '-X', 'POST', '-d', prompt],
            capture_output=True, text=True
        )

        if response.returncode == 0:
            try:
                json_response = json.loads(response.stdout)
                # Extracting the text from the correct path in the response
                generated_text = json_response['candidates'][0]['content']['parts'][0]['text']
                genai_view.controls.append(ft.Text(generated_text))
                genai_view.visible = True
            except (json.JSONDecodeError, IndexError, KeyError) as e:
                prompt_view.controls.append(ft.Text(f"Error parsing response: {e}"))
        else:
            prompt_view.controls.append(ft.Text("Error retrieving response."))

        page.update()

    def prompting(e=None):
        prompt_view.visible = False
        prompt_answer(input.value)

    genai_view.visible = False
    ai_chat = ft.Card(
        content=ft.Container(
            padding=20,
            expand=True,
            width=350,
            content=ft.Column(
                controls=[
                    ft.Text("Chat with CyberSpace AI", weight=ft.FontWeight.BOLD, size=20),
                    ft.Divider(height=1, color=ft.colors.TRANSPARENT),
                    ft.Row(
                        controls=[
                            input := ft.TextField(label="Ask CyberSpace AI anything...", width=260, height=43),
                            ft.IconButton(
                                ft.icons.SEND,
                                icon_size=20,
                                on_click=prompting,
                                style=ft.ButtonStyle(
                                    shape={"": ft.RoundedRectangleBorder(radius=8)},
                                    color={"": "black"},
                                    bgcolor={"": "#7df6dd"},
                                )
                            )
                        ]
                    ),
                    ft.Divider(height=1, color=ft.colors.TRANSPARENT),
                    prompt_view,
                    genai_view
                ]
            )
        )
    )

    return ft.View(
        "/dashboard",
        controls=[
            ft.Row(
                controls=[
                    sidebar_content,
                    ft.VerticalDivider(width=1, color=ft.colors.TRANSPARENT),
                    dashboard_content,
                    ai_chat,
                    ft.Container(
                        content=dark_btn,
                        alignment=ft.alignment.top_right,
                        padding=ft.padding.only(left=0, top=20),
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                expand=True,
            ),
        ]
    )
