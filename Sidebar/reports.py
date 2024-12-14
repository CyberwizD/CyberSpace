import flet as ft

def main(page: ft.Page):
    page.title = "Reports"

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

    reports_content = ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Documents", size=24, weight="bold"),
                ft.Divider(height=10),
                ft.Row(
                    controls=[
                        ft.ElevatedButton("New"),
                        ft.ElevatedButton("Filters"),
                        ft.ElevatedButton("Sort By: Latest"),
                    ],
                ),
                ft.Divider(height=20),
                ft.Text("Folders", style="subtitle1"),
                ft.Row(
                    controls=[
                        ft.Card(
                            content=ft.Container(
                                width=150,
                                height=100,
                                alignment=ft.alignment.center,
                                content=ft.Text("Results 2023\n23 Files", size=16),
                            )
                        ),
                        ft.Card(
                            content=ft.Container(
                                width=150,
                                height=100,
                                alignment=ft.alignment.center,
                                content=ft.Text("Market Analysis\n8 Files", size=16),
                            )
                        ),
                        ft.Card(
                            content=ft.Container(
                                width=150,
                                height=100,
                                alignment=ft.alignment.center,
                                content=ft.Text("All Contracts\n37 Files", size=16),
                            )
                        ),
                    ],
                ),
                ft.Divider(height=20),
                ft.Text("Recent", style="subtitle1"),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.INSERT_DRIVE_FILE, color="black"),
                    title=ft.Text("Analysis Data July"),
                    subtitle=ft.Text("Aug 5, 2023 - 1.8 MB", size=10),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.INSERT_DRIVE_FILE, color="black"),
                    title=ft.Text("Q2 Results"),
                    subtitle=ft.Text("Jul 31, 2023 - 2.5 MB", size=10),
                ),
            ],
        ),
    )

    return ft.View(
       "/reports",
        controls=[
            ft.Row(
                controls=[
                    sidebar_content,
                    ft.VerticalDivider(width=1, color=ft.colors.TRANSPARENT),
                    reports_content,
                    ft.Container(
                        content=dark_btn,
                        alignment=ft.alignment.top_right,
                        padding=ft.padding.only(left=0, top=20),
                    ),
                ],
                alignment="start",
                expand=True
            )
        ]
    )
