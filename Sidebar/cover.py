import flet as ft


def main(page: ft.Page):
    def on_get_started_click(e):
        # Navigate to login page
        page.go("/login")

    left_container = ft.Container(
        width=page.width,
        height=page.height,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("CyberSpace", size=50, weight="bold", color="white", italic=True),
                ft.Divider(height=20, color="transparent"),
                ft.ElevatedButton(
                    "Get Started",
                    on_click=on_get_started_click,
                    width=200,
                    height=50
                )
            ]
        )
    )

    return ft.View(
        "/",
        controls=[left_container]
    )



















# # Simulate the login page
# def main(page: ft.Page):
#     def on_sign_in_click(e):
#         # Navigate to dashboard page
#         page.go("/dashboard")
#
#     page.horizontal_alignment = "center"
#     page.vertical_alignment = "center"
#
#     return ft.View(
#         "/login",
#         controls=[
#             ft.Card(
#                 width=400,
#                 height=500,
#                 content=ft.Column(
#                     horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#                     controls=[
#                         ft.Text("Sign In", size=22, weight="bold"),
#                         ft.TextField(hint_text="Email"),
#                         ft.TextField(hint_text="Password", password=True),
#                         ft.ElevatedButton("Sign In", on_click=on_sign_in_click),
#                     ],
#                 ),
#             )
#         ]
#     )