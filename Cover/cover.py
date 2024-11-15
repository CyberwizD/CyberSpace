import flet as ft
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def main(page: ft.Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    def on_get_started_click(e):
        # Show the sign-in form
        page.go("/login")

    left_container = ft.Container(
        width=page.width,
        height=page.height,
        image_src="CyberSpace.jpg",  # Your background image URL
        image_fit=ft.ImageFit.COVER,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("CyberSpace", size=50, weight="bold", color="white", italic=True),
                ft.Divider(height=20, color="transparent"),
                ft.ElevatedButton(
                    "Get Started",
                    on_click=on_get_started_click,
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

    # return ft.View(
    #     "/",
    #     controls=[left_container]
    # )

    # Main layout with both containers (left and right)
    # main_layout = ft.Column(
    #     controls=[left_container]
    # )

    page.add(left_container)
    page.update()

if __name__ == '__main__':
    ft.app(target=main)
