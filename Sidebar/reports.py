import flet as ft

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
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.GPS_FIXED, color="white"),
                        title=ft.Text("Targets", color="white"),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.SCANNER, color="white"),
                        title=ft.Text("Scans", color="white"),
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

def ReportsContent():
    return ft.Container(
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

def main(page: ft.Page):
    page.title = "Reports"

    sidebar = Sidebar()
    reports_content = ReportsContent()

    page.add(
        ft.Row(
            controls=[
                sidebar,
                ft.VerticalDivider(width=1, color="white"),
                reports_content,
            ],
        )
    )

if __name__ == "__main__":
    ft.app(target=main)




# import flet as ft
#
# def main(page: ft.Page):
#     return ft.View(
#         "/reports",
#         controls=[
#             ft.Text("Reports Page", size=24, weight="bold"),
#         ]
#     )