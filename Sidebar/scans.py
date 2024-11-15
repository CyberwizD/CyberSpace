import flet as ft
from datetime import date
import time

def main(page: ft.Page):
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

    def start_scan(e):
        e.page.go("/scanning")

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

    scans_content = ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Automated App Scan (Full)", size=24, weight="bold"),
                ft.Divider(height=10),
                ft.Row(
                    controls=[
                        ft.TextField(label="Enter a web url to scan"),
                        ft.ElevatedButton(
                            "Scan",
                            on_click=lambda e: start_scan(e),
                            style=ft.ButtonStyle(
                                shape={
                                    "": ft.RoundedRectangleBorder(radius=8),
                                },
                                color={
                                    "": "black",
                                },
                                bgcolor={"": "#7df6dd"},
                            ),
                        ),
                        # ft.TextButton("Reports"),
                    ]
                ),
                ft.Divider(height=10),
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text("Vulnerabilities", size=18, weight="bold"),
                                ft.Text(value="Some description goes here", height=200),
                            ]
                        ),
                        ft.VerticalDivider(width=500, color="transparent"),
                        ft.Column(
                            controls=[
                                ft.Text("Scan History", size=18, weight="bold"),
                                ft.Column(
                                    controls=[
                                        ft.DataTable(
                                            columns=[
                                                ft.DataColumn(ft.Text(f"Last Scanned - {date.today().strftime('%b-%d')}"))
                                            ],
                                            rows=[]
                                        )
                                    ]
                                ),
                            ]
                        )
                    ]
                )
            ],
        ),
    )

    return ft.View(
        "/scans",
        controls=[
            ft.Row(
                controls=[
                    sidebar_content,
                    ft.VerticalDivider(width=1, color=ft.colors.TRANSPARENT),
                    scans_content,
                ],
                alignment=ft.MainAxisAlignment.START,
                expand=True
            )
        ]
    )

if __name__ == '__main__':
    ft.app(target=main)