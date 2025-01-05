import flet as ft
import firebase_admin
from firebase_admin import credentials, firestore, auth
import time
import os
from dotenv import load_dotenv
load_dotenv()

Account = os.getenv("database")
pic = os.getenv("pic")

# Initialize Firebase Admin
if not firebase_admin._apps:
    cred = credentials.Certificate(fr"{Account}")
    firebase_admin.initialize_app(cred)

db = firestore.client()


def main(page: ft.Page):
    # Set page alignment and properties
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.title = "Sign Up"
    # page.bgcolor = "#2f2f38"
    page.padding = 0
    page.spacing = 0

    # Create account function using Firebase
    def create_account(e):
        email = email_field.value
        password = password_field.value

        # Firebase logic to create the account
        try:
            user = auth.create_user(
                email=email,
                password=password
            )
            if user:
                page.snack_bar = ft.SnackBar(
                    ft.Column([
                        ft.Row([
                            ft.Text(f"Account created successfully!", size=30, color="black"),
                            ft.ProgressRing(color="black")
                        ], alignment=ft.MainAxisAlignment.CENTER)
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    bgcolor="#7df6dd"
                )
                page.snack_bar.open = True
                page.update()
                time.sleep(5)
                e.page.go("/dashboard")

        except Exception as error:
            internet_error = "HTTPSConnectionPool"
            error_str = str(error)

            if not email and not password:
                page.snack_bar = ft.SnackBar(
                    ft.Column([
                        ft.Row([
                            ft.Text("Error: Email and password fields must not be empty!", size=30, color="black"),
                            ft.ProgressRing(color="black")
                        ], alignment=ft.MainAxisAlignment.CENTER)
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    bgcolor="#7df6dd"
                )
                page.snack_bar.open = True
                page.update()

            elif internet_error in error_str:
                page.snack_bar = ft.SnackBar(
                    ft.Column([
                        ft.Row([
                            ft.Text(f"Error: No Internet Connection!", size=30, color="black"),
                            ft.ProgressRing(color="black")
                        ], alignment=ft.MainAxisAlignment.CENTER)
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    bgcolor="#7df6dd"
                )
                page.snack_bar.open = True
                page.update()

            else:
                page.snack_bar = ft.SnackBar(
                    ft.Column([
                        ft.Row([
                            ft.Text(f"Error creating account: {error}", size=30, color="black"),
                            ft.ProgressRing(color="black")
                        ], alignment=ft.MainAxisAlignment.CENTER)
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    bgcolor="#7df6dd"
                )
                page.snack_bar.open = True
                page.update()

    # Left part of the layout (Image, logo, and minimal text)
    left_column = ft.Container(
        content=ft.Stack(
            [
                # Background image
                ft.Image(
                    src=fr"{pic}",
                    width=500,
                    height=550,
                    fit=ft.ImageFit.COVER,
                    border_radius=10,
                ),
                # Logo at the top-left
                ft.Column(
                    controls=[
                        ft.Row([
                            ft.Container(
                                content=ft.Text(
                                    "CyberSpace",  # Logo text
                                    size=30,
                                    color="white",
                                    opacity=0.5,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                padding=ft.Padding(left=20, top=10, right=0, bottom=0),
                                alignment=ft.alignment.top_left,
                            ),
                            # "Back to website" button at the top-right
                            ft.Container(
                                content=ft.ElevatedButton(
                                    "Get Started",
                                    on_click=lambda e: e.page.go("/"),
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.colors.TRANSPARENT,
                                        color="white",
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                    ),
                                    opacity=0.5
                                ),
                                padding=ft.Padding(right=20, top=20, left=0, bottom=0),
                                alignment=ft.alignment.top_right,
                            ),
                        ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        # Centered text at the bottom
                        ft.Container(
                            content=ft.Text(
                                "Capturing Moments,\nCreating Memories",
                                color="white",
                                size=22,
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            padding=ft.Padding(bottom=6, top=365, right=0, left=0),
                            alignment=ft.alignment.bottom_center,
                        ),
                        # Pagination dots at the bottom
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Container(width=10, height=3, bgcolor=ft.colors.GREY),
                                    ft.Container(width=10, height=3, bgcolor="white"),
                                    ft.Container(width=10, height=3, bgcolor=ft.colors.GREY),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=5,
                            ),
                            alignment=ft.alignment.bottom_center,
                            padding=ft.Padding(bottom=10, top=0, right=0, left=0),
                        ),
                    ]
                )
            ]
        ),
        width=500,
        height=550,
        padding=10,
        bgcolor="#17171d",  # Background color matching the original style
        border_radius=10  # Set border radius for all corners
    )

    # Right part of the layout (Form section)
    email_field = ft.TextField(
        label="Email",
        width=400,
        bgcolor=ft.colors.TRANSPARENT,
        color="grey",
        label_style=ft.TextStyle(color="white"),
        border_color="grey"
    )
    password_field = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        width=400,
        bgcolor=ft.colors.TRANSPARENT,
        color="grey",
        label_style=ft.TextStyle(color="white"),
        border_color="grey"
    )

    # Right part of the layout (Form section)
    right_column = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Create an account",
                    size=35,
                    weight=ft.FontWeight.BOLD,
                    color="white",
                ),
                ft.Row([
                    ft.Text("Already have an account?", color="white", opacity=0.6),
                    ft.TextButton("Sign in", on_click=lambda e: e.page.go("/login")),
                ]),
                # Form fields
                ft.Row([
                    ft.TextField(
                        label="First Name",
                        width=195,
                        bgcolor=ft.colors.TRANSPARENT,
                        color="grey",
                        label_style=ft.TextStyle(color="white"),
                        border_color="grey"
                    ),
                    ft.TextField(
                        label="Last Name",
                        width=195,
                        bgcolor=ft.colors.TRANSPARENT,
                        color="grey",
                        label_style=ft.TextStyle(color="white"),
                        border_color="grey"
                    ),
                ]),
                email_field,
                password_field,
                ft.Row(
                    controls=[
                        ft.Checkbox(
                            label="I agree to the Terms & Conditions",
                            value=False,
                            label_style=ft.TextStyle(color="white"),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START
                ),
                ft.ElevatedButton(
                    "Create account",
                    bgcolor="#7df6dd",
                    color="black",
                    width=400,
                    height=50,
                    on_click=create_account,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                ),
                ft.Row([
                    ft.Container(width=140, height=3, bgcolor=ft.colors.GREY),
                    ft.Text("Or register with", color="white", opacity=0.6),
                    ft.Container(width=140, height=3, bgcolor=ft.colors.GREY),
                ],
                    alignment=ft.MainAxisAlignment.START
                ),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            content=ft.Row([
                                ft.Icon(ft.icons.VERIFIED_USER),
                                ft.Text("Google"),
                            ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            width=200,
                            color="white",
                            bgcolor=ft.colors.TRANSPARENT,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                            ),
                        ),
                        ft.ElevatedButton(
                            content=ft.Row([
                                ft.Icon(ft.icons.APPLE),
                                ft.Text("Apple"),
                            ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            width=200,
                            color="white",
                            bgcolor=ft.colors.TRANSPARENT,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=15,
        ),
        width=500,
        height=550,
        padding=20,
        # bgcolor="#2f2f38",
        # border_radius=10  # Set border radius for all corners
    )

    # Add the left and right columns into a row
    signup_content = ft.Container(
        content=ft.Row(
            controls=[left_column, right_column],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        border_radius=10,
        padding=5,
        width=1000,
        height=550,
        bgcolor="#17171d",
    )

    main_container = ft.Container(
        content=signup_content,
        alignment=ft.alignment.bottom_center,  # Center the signup_content within the main container
        width=5000,
        height=635,  # Adjust height as needed
    )

    return ft.View(
        "/signup",
        controls=[
            main_container
        ]
    )
