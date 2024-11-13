import flet as ft
import scans

class Sidebar(ft.UserControl):
    def build(self):
        return ft.Container(
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
                        on_click=lambda _: self.open_dashboard(),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.GPS_FIXED, color="white"),
                        title=ft.Text("Targets", color="white"),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.SCANNER, color="white"),
                        title=ft.Text("Scans", color="white"),
                        on_click=lambda _: self.open_scans(),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.INTEGRATION_INSTRUCTIONS, color="white"),
                        title=ft.Text("Integrations", color="white"),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.REPORT, color="white"),
                        title=ft.Text("Reports", color="white"),
                    ),
                ],
            ),
        )

    def open_dashboard(self):
        pass

    def open_scans(self):
        # Redirect to scans.py
        ft.app(target=scans.main)


def DashboardContent():
    return ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Dashboard Overview", size=24, weight="bold"),
                ft.Divider(height=10),
                ft.Text("Welcome to your dashboard. Here you can see an overview of your scans, targets, and more."),
                ft.Row(controls=[ft.ElevatedButton("Start Scan"), ft.ElevatedButton("Manage Targets")]),
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

def main(page: ft.Page):
    page.title = "Dashboard"

    sidebar = Sidebar()
    dashboard_content = DashboardContent()

    page.add(
        ft.Row(
            controls=[
                sidebar,
                ft.VerticalDivider(width=1, color="white"),
                dashboard_content,
            ],
        )
    )

if __name__ == "__main__":
    ft.app(target=main)






# import flet as ft
#
# def main(page: ft.Page):
#     def on_start_scan_click(e):
#         page.go("/scans")
#
#     def on_manage_targets_click(e):
#         page.go("/targets")
#
#     sidebar = ft.Container(
#         width=250,
#         content=ft.Column(
#             controls=[
#                 ft.ListTile(
#                     leading=ft.Icon(ft.icons.DASHBOARD),
#                     title=ft.Text("Dashboard"),
#                     on_click=lambda _: page.go("/dashboard"),
#                 ),
#                 ft.ListTile(
#                     leading=ft.Icon(ft.icons.GPS_FIXED),
#                     title=ft.Text("Targets"),
#                     on_click=lambda _: page.go("/targets"),
#                 ),
#                 ft.ListTile(
#                     leading=ft.Icon(ft.icons.SCANNER),
#                     title=ft.Text("Scans"),
#                     on_click=lambda _: page.go("/scans"),
#                 ),
#                 ft.ListTile(
#                     leading=ft.Icon(ft.icons.INTEGRATION_INSTRUCTIONS),
#                     title=ft.Text("Integrations"),
#                     on_click=lambda _: page.go("/integration"),
#                 ),
#                 ft.ListTile(
#                     leading=ft.Icon(ft.icons.REPORT),
#                     title=ft.Text("Reports"),
#                     on_click=lambda _: page.go("/reports"),
#                 ),
#             ]
#         ),
#     )
#
#     return ft.View(
#         "/dashboard",
#         controls=[
#             ft.Row(
#                 controls=[
#                     sidebar,
#                     ft.VerticalDivider(width=1),
#                     ft.Container(
#                         padding=20,
#                         content=ft.Column(
#                             controls=[
#                                 ft.Text("Dashboard", size=24, weight="bold"),
#                                 ft.Row(
#                                     controls=[
#                                         ft.ElevatedButton("Start Scan", on_click=on_start_scan_click),
#                                         ft.ElevatedButton("Manage Targets", on_click=on_manage_targets_click),
#                                     ]
#                                 ),
#                             ]
#                         )
#                     ),
#                 ]
#             )
#         ]
#     )
