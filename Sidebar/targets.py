import flet as ft

def main(page: ft.Page):
    page.title = "Targets"

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

    target_content = ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Workspaces and Targets", size=24, weight="bold"),
                ft.Divider(height=10),
                ft.Row(
                    controls=[
                        ft.Container(
                            width=200,
                            content=ft.Column(
                                controls=[
                                    ft.Text("Workspaces", size=18, weight="bold"),
                                    ft.TextField(hint_text="Search workspaces..."),
                                    ft.ListTile(
                                        leading=ft.Icon(ft.icons.PERSON, color="black"),
                                        title=ft.Text("Personal Space"),
                                    ),
                                    ft.Text("Recent", style="subtitle1"),
                                    ft.ListTile(
                                        leading=ft.Icon(ft.icons.WORK, color="black"),
                                        title=ft.Text("InterSans Design"),
                                    ),
                                    ft.Text("Workspaces", style="subtitle1"),
                                    ft.ListTile(
                                        leading=ft.Icon(ft.icons.WORK, color="black"),
                                        title=ft.Text("All Workspaces"),
                                    ),
                                    ft.ListTile(
                                        leading=ft.Icon(ft.icons.WORK, color="black"),
                                        title=ft.Text("Never Before Seen"),
                                    ),
                                ],
                            ),
                        ),
                        ft.VerticalDivider(width=1),
                        ft.Container(
                            width=400,
                            content=ft.Column(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Text("Targets", size=18, weight="bold"),
                                            ft.ElevatedButton("See All Targets"),
                                        ],
                                        alignment="spaceBetween"
                                    ),
                                    ft.TextField(hint_text="Search by email, target name..."),
                                    ft.Divider(height=10),
                                    ft.Text("Favorites", style="subtitle1"),
                                    ft.ListTile(
                                        leading=ft.Icon(ft.icons.APPS, color="black"),
                                        title=ft.Text("[Demo] Network Pentest"),
                                        subtitle=ft.Text("APIs - Delivery Completed", size=10),
                                    ),
                                    ft.Text("Pending Setup", style="subtitle1"),
                                    ft.ListTile(
                                        leading=ft.Icon(ft.icons.PENDING, color="black"),
                                        title=ft.Text("[No Name Target]"),
                                        subtitle=ft.Text("iOS App - Pending", size=10),
                                    ),
                                    ft.ListTile(
                                        leading=ft.Icon(ft.icons.PENDING, color="black"),
                                        title=ft.Text("[No Name Target]"),
                                        subtitle=ft.Text("Cloud Infra - Pending", size=10),
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ],
        ),
    )

    return ft.View(
        "/targets",
        controls=[
            ft.Row(
                controls=[
                    sidebar_content,
                    ft.VerticalDivider(width=1, color=ft.colors.TRANSPARENT),
                    target_content,
                ],
                alignment="start",
                expand=True
            )
        ]
    )
