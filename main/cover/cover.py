import flet as ft
# from login import animate_boxes
# import asyncio


def main(page: ft.Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.padding = 0
    page.spacing = 0

    # async \
    def on_get_started_click(e: ft.ControlEvent):
        # Navigate to login page
        page.go("/login")
        # await animate_boxes(e.page)

    # Outer container that expands to fill the screen
    cover_content = ft.Container(
        expand=True,  # Ensures it fills the available space
        alignment=ft.alignment.center,  # Centers the inner content both horizontally and vertically
        content=ft.Container(
            width=600,  # Fixed width
            height=1000,  # Fixed height
            shadow=ft.BoxShadow(  # This adds a shadow to simulate elevation
                spread_radius=10,
                blur_radius=10,
                color=ft.colors.BLACK12,
                offset=ft.Offset(2, 2),
            ),
            border_radius=8,  # Rounds the corners slightly
            alignment=ft.alignment.center,  # Centers the content inside the container
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,  # Centers vertically
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centers horizontally
                controls=[
                    ft.Text("CyberSpace", size=50, weight=ft.FontWeight.BOLD, color="white32", italic=True),
                    ft.Divider(height=20, color="transparent"),
                    ft.ElevatedButton(
                        "Get Started",
                        on_click=on_get_started_click,
                        width=200,
                        height=42,
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
                ],
            ),
        ),
    )

    # Adding the main container to the page
    return ft.View(
        "/",
        controls=[
            cover_content
        ]
    )
