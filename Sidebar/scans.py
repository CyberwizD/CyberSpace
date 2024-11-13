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

def ScansContent():
    return ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Automated App Scan (Full)", size=24, weight="bold"),
                ft.Divider(height=10),
                ft.Text("In Progress - #214 - 13 Oct 2023, 12:13 pm", size=16),
                ft.Row(
                    controls=[
                        ft.TextButton("Request Vetting"),
                        ft.TextButton("Get Certificate"),
                    ],
                ),
                ft.Divider(height=20),
                ft.Text("Vulnerabilities", size=18, weight="bold"),
                ft.Text("Some description goes here"),
                ft.Divider(height=20),
                ft.Text("Test Cases", size=18, weight="bold"),
                ft.Text("Some description goes here"),
            ],
        ),
    )

def main(page: ft.Page):
    page.title = "Scans"

    sidebar = Sidebar()
    scans_content = ScansContent()

    page.add(
        ft.Row(
            controls=[
                sidebar,
                ft.VerticalDivider(width=1, color="white"),
                scans_content,
            ],
        )
    )

if __name__ == "__main__":
    ft.app(target=main)




# import flet as ft
#
# def main(page: ft.Page):
#     return ft.View(
#         "/scans",
#         controls=[
#             ft.Text("Scans Page", size=24, weight="bold"),
#         ]
#     )