import flet as ft
import scans

def main(page: ft.Page):
    page.title = "Dashboard"

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
                    on_click=lambda e: integration_click(e),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.REPORT, color="white"),
                    title=ft.Text("Reports", color="white"),
                    on_click=lambda e: reports_click(e)
                ),
            ],
        ),
    )

    dashboard_content = ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Dashboard Overview", size=24, weight="bold"),
                ft.Divider(height=10),
                ft.Text("Welcome to your dashboard. Here you can see an overview of your scans, targets, and more."),
                ft.Row(controls=[ft.ElevatedButton("Start Scan", on_click=lambda e: on_start_scan_click(e), color="white"),
                                 ft.ElevatedButton("Manage Targets", on_click=lambda e: on_manage_targets_click(e), color="white")]),
                ft.Divider(height=20),
                ft.Text("Quick Stats", size=18, weight="bold"),
                ft.Row(
                    controls=[
                        ft.Card(
                            content=ft.Container(
                                padding=20,
                                content=ft.Column(
                                    controls=[
                                        ft.Text("Total Scans", size=16),
                                        ft.Text("5", size=24, weight="bold"),
                                    ],
                                ),
                            )
                        ),
                        ft.Card(
                            content=ft.Container(
                                padding=20,
                                content=ft.Column(
                                    controls=[
                                        ft.Text("Open Vulnerabilities", size=16),
                                        ft.Text("2", size=24, weight="bold"),
                                    ],
                                ),
                            )
                        ),
                    ],
                ),
            ],
        ),
    )

    return ft.View(
        route="/dashboard",
        controls=[
            ft.Row(
                controls=[
                    sidebar_content,
                    ft.VerticalDivider(width=1, color=ft.colors.TRANSPARENT),
                    dashboard_content,
                ],
                alignment="start",
                expand=True,
            ),
        ],
    )
