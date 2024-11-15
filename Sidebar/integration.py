import flet as ft

def main(page: ft.Page):
    page.title = "Integrations"

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

    integration_content = ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Integrations", size=24, weight="bold"),
                ft.Divider(height=10),
                ft.Text("Unlock the full power of CyberSpace with additional apps.", size=16),
                ft.Divider(height=5),
                ft.Row(
                    controls=[
                        ft.ElevatedButton("Request Integration", color="white"),
                        ft.ElevatedButton("API Keys", color="white"),
                    ],
                ),
                ft.Divider(height=5),
                # ft.Row(
                #     controls=[
                #     ft.ElevatedButton(
                #         "Search",
                #         style=ft.ButtonStyle(
                #             shape={
                #                 "": ft.RoundedRectangleBorder(radius=8),
                #             },
                #             color={
                #                 "": "black",
                #             },
                #             bgcolor={"": "#7df6dd"},
                #         ),
                #     )
                #     ]
                # ),
                # ft.Divider(height=5),
                ft.Text("Connected Integrations", style="subtitle1"),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.API, color="blue"),
                    title=ft.Text("Nessus"),
                    subtitle=ft.Text("Active", size=10),
                    trailing=ft.TextButton("Configure"),
                ),
                ft.ListTile(
                leading=ft.Icon(ft.icons.APPS, color="blue"),
                    title=ft.Text("WPScan"),
                    subtitle=ft.Text("Inactive", size=10),
                    trailing=ft.TextButton("Configure"),
                ),
                ft.Divider(height=5),
                ft.Text("CLI scan Integrations", style="subtitle1"),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.SCANNER, color="#7df6dd"),
                    title=ft.Text("Wapiti"),
                    trailing=ft.TextButton("Connect"),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.SCANNER_ROUNDED, color="#7df6dd"),
                    title=ft.Text("SqlMap"),
                    trailing=ft.TextButton("Connect"),
                ),
            ],
        ),
    )

    return ft.View(
       "/integration",
        controls=[
            ft.Row(
                controls=[
                    sidebar_content,
                    ft.VerticalDivider(width=1, color=ft.colors.TRANSPARENT),
                    integration_content,
                ],
                alignment="start",
                expand=True
            )
        ]
    )
