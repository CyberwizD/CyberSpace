import time
import threading
import flet as ft

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
                ft.Text("CyberSpace", size=30, weight="bold", color="white"),
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
            ],
        ),
    )

    vulnerabilities_content = ft.Row(
        controls=[
            ft.ListView(
                height=300,
                padding=10,
                expand=True,
                controls=[
                    ft.Card(
                        content=ft.Container(
                            padding=10,
                            content=ft.Column(
                                controls=[
                                    ft.Text("#8793 - Server Side Template Injection", weight="bold"),
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
                                    ft.Text("#8793 - PII Disclosure", weight="bold"),
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
                                    ft.Text("#8793 - .svn/entries Found", weight="bold"),
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
                                    ft.Text("#8793 - JSON Web Key Set Disclosed", weight="bold"),
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
                                    ft.Text("#8793 - WordPress Database Backup File Found", weight="bold"),
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

    total_scans_text = ft.Text("0", size=20, weight="bold")
    high_severity_text = ft.Text("0", size=20, weight="bold")
    potential_loss_text = ft.Text("$0", size=20, weight="bold")

    dashboard_content = ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Dashboard Overview", size=24, weight="bold"),
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
                ft.Text("Quick Stats", size=18, weight="bold"),
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
                                ft.Text("Vulnerabilities (50)", weight="bold", size=16),
                                vulnerabilities_content
                            ]
                        )
                    )
                )
            ],
        ),
    )

    progress_content = ft.Card(
        content=ft.Container(
            padding=20,
            width=300,
            content=ft.Column(
                controls=[
                    ft.Text("Progress", weight="bold", size=20),
                    ft.Divider(height=10),
                    ft.Checkbox(label="Starting Scan", value=True),
                    ft.Checkbox(label="Vulnerability Scan", value=True),
                    ft.Checkbox(label="Connectivity Check", value=True),
                    ft.Checkbox(label="Crawling", value=True),
                    ft.Checkbox(label="Passive", value=True),
                    ft.Checkbox(label="Active", value=True),
                    ft.Checkbox(label="Emerging Threats", value=True),
                    ft.Checkbox(label="Penetration Testing", value=True),
                    ft.Checkbox(label="Bugs Verified", value=True),
                    ft.Checkbox(label="Bugs Reported", value=True),
                ]
            )
        )
    )

    prompt_view = ft.ListView(
        padding=10,
        expand=True,
        controls=[
            progress_content
        ]
    )

    def prompt_answer(input):
        prompt_view.controls.append(
            ft.Text(f"CyberSpace AI: {"Here's your reply"}"),
        )
        page.update()
        prompt_view.visible = True

    def prompting(e=None):
        prompt_view.visible = False
        prompt_answer(input.value)

    ai_chat = ft.Card(
        content=ft.Container(
            padding=20,
            expand=True,
            width=350,
            content=ft.Column(
                controls=[
                    ft.Text("Chat with CyberSpace AI", weight="bold", size=20),
                    ft.Divider(height=1, color=ft.colors.TRANSPARENT),
                    ft.Row(
                        controls=[
                            input := ft.TextField(label="Ask CyberSpace AI anything...", width=260, height=42),
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
                    prompt_view
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

'''

# Check to validate whether the input is empty or integers
        # if self.input.value != "" and self.input.value.isdigit():
            # Changing the input value to float
            # delta: float = float(self.input.value)
            # Checks which button is clicked
            # if event.control.data:
            #     self.counter += delta
            #     self.update_data_table(delta, sign=True)
            #     self._in.chart.create_data_point(
            #         x = self.x,
            #         y = delta
            #     )
            #
            #     self.x += 1
            # else:
            #     self.counter -= delta
            #     self.update_data_table(delta, sign=False)
            #     self._out.chart.create_data_point(
            #         x=self.x,
            #         y=delta
            #     )
            #
            #     self.x += 1

            # Updating the page
            # self.balance.value = locale.currency(self.counter, grouping=True)
            # self.balance.update()
            # self.input.value = ""  # Clears input field
            # self.input.update()

'''