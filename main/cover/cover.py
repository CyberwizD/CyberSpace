import flet as ft
import sys
import os
from dotenv import load_dotenv
load_dotenv()

cover_pic = os.getenv("cover_pic")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def main(page: ft.Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    def on_signup_click(e):
        # Show the sign-in form
        page.go("/signup")

    cov_container = ft.Container(
        width=page.width,
        height=page.height,
        border_radius=10,
        image_src=fr"{cover_pic}",  # Your background image URL
        image_fit=ft.ImageFit.COVER,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row([
                    ft.Text("Cyber", size=50, weight=ft.FontWeight.NORMAL, color="white", opacity=0.8),
                    ft.Text("Space", size=50, weight="bold", color="white", opacity=0.8),
                ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Divider(height=20, color="transparent"),
                ft.ElevatedButton(
                    "Get Started",
                    on_click=on_signup_click,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        bgcolor=ft.colors.TRANSPARENT,
                        color=ft.colors.WHITE
                    ),
                    width=200,
                    height=50
                )
            ]
        )
    )

    cover_content = ft.Container(
        content=cov_container,
        alignment=ft.alignment.center,
        height=725
    )

    return ft.View(
        "/",
        controls=[cover_content]
    )

