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

def IntegrationContent():
    return ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Integrations", size=24, weight="bold"),
                ft.Divider(height=10),
                ft.Text("Unlock the full power of Astra with additional apps.", size=16),
                ft.Row(
                    controls=[
                        ft.ElevatedButton("Request Integration"),
                        ft.ElevatedButton("Help"),
                    ],
                ),
                ft.Divider(height=20),
                ft.TextField(hint_text="Search by integration name..."),
                ft.Divider(height=20),
                ft.Text("Connected Integrations", style="subtitle1"),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.SETTINGS, color="blue"),
                    title=ft.Text("Bitbucket"),
                    subtitle=ft.Text("Active", size=10),
                    trailing=ft.TextButton("Configure"),
                ),
                ft.Divider(height=20),
                ft.Text("CI/CD Integrations", style="subtitle1"),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.SCANNER, color="black"),
                    title=ft.Text("GitHub"),
                    trailing=ft.TextButton("Connect"),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.SCANNER_ROUNDED, color="black"),
                    title=ft.Text("GitLab"),
                    trailing=ft.TextButton("Connect"),
                ),
            ],
        ),
    )

def main(page: ft.Page):
    page.title = "Integrations"

    sidebar = Sidebar()
    integration_content = IntegrationContent()

    page.add(
        ft.Row(
            controls=[
                sidebar,
                ft.VerticalDivider(width=1, color="white"),
                integration_content,
            ],
        )
    )

if __name__ == "__main__":
    ft.app(target=main)




# import flet as ft
#
# def main(page: ft.Page):
#     return ft.View(
#         "/integration",
#         controls=[
#             ft.Text("Integration Page", size=24, weight="bold"),
#         ]
#     )