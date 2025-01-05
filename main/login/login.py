import time
import flet as ft
from flet import Ref, TextField
import sys
from math import pi
import asyncio
import firebase_admin
from firebase_admin import credentials, firestore, auth
import os
from dotenv import load_dotenv
load_dotenv()

Auth = os.getenv("database")
pic = os.getenv("login_pic")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Initialize Firebase Admin
if not firebase_admin._apps:
    cred = credentials.Certificate(fr"{Auth}")
    firebase_admin.initialize_app(cred)

db = firestore.client()


class AnimatedBox(ft.UserControl):
    def __init__(self, border_color, bg_color, rotate_angle):
        # Create instances for each parameter
        self.border_color = border_color
        self.bg_color = bg_color
        self.rotate_angle = rotate_angle

        super().__init__()

    def build(self):
        # Two boxes that differ in rotation, color, and bgcolor will be passed
        # as arguments when the class is called
        return ft.Container(
            width=48,
            height=48,
            border=ft.border.all(2.5, self.border_color),
            bgcolor="#2f2f38",
            border_radius=2,
            rotate=ft.transform.Rotate(self.rotate_angle, ft.alignment.center),
            animate_rotation=ft.animation.Animation(700, "easeInOut"),  # Enable animation
        )


async def animate_boxes(page):
    # Create several variables for one box to go clockwise,
    # and the other anti-clockwise
    clockwise_rotation = pi / 4
    anti_clockwise_rotation = -pi * 2

    # Animating the rotation of the boxes
    # red_box = page.controls[0].content.content.controls[1].controls[0].controls[0]
    # blue_box = page.controls[0].content.content.controls[1].controls[1].controls[0]

    red_box = page.views[-1].controls[0].content.controls[0].content.content.controls[1].controls[0]
    blue_box = page.views[-1].controls[0].content.controls[0].content.content.controls[1].controls[1]

    # Implement a counter to reverse the rotation direction
    counter = 0
    while True:
        # rotate 4x before switching directions
        if 0 <= counter <= 4:
            red_box.rotate = ft.transform.Rotate(
                anti_clockwise_rotation, ft.alignment.center
            )
            blue_box.rotate = ft.transform.Rotate(
                clockwise_rotation, ft.alignment.center
            )

            # Trigger animation updates
            await red_box.update_async()
            await blue_box.update_async()

            clockwise_rotation += pi / 2
            anti_clockwise_rotation -= pi / 2

            counter += 1
            await asyncio.sleep(0.7)  # Non-blocking sleep

        # Reversing the boxes
        if 5 <= counter <= 10:
            # Make sure to reverse the rotation angles
            clockwise_rotation -= pi / 2
            anti_clockwise_rotation += pi / 2

            red_box.rotate = ft.transform.Rotate(
                anti_clockwise_rotation, ft.alignment.center
            )
            blue_box.rotate = ft.transform.Rotate(
                clockwise_rotation, ft.alignment.center
            )

            # Trigger animation updates
            await red_box.update_async()
            await blue_box.update_async()

            counter += 1
            await asyncio.sleep(0.7)  # Non-blocking sleep

        # Finally, reset the counter to 0 at 10
        if counter > 10:
            counter = 0


class UserInputField(ft.UserControl):
    def __init__(self, icon_name, text_hint, hide, function_emails: bool, function_check: bool,
                 input_ref: ft.Ref[ft.TextField] = None):
        self.icon_name = icon_name
        self.text_hint = text_hint
        self.hide = hide
        self.function_emails = function_emails
        self.function_check = function_check
        self.input_ref = input_ref  # Store the reference
        super().__init__()

    # Function to fill in email extension
    def return_email_prefix(self, e):
        email = self.controls[0].content.controls[1].value
        if e.control.data in email:
            pass
        else:
            self.controls[0].content.controls[1].value += e.control.data
            self.controls[0].content.controls[2].offset = ft.transform.Offset(0.5, 0)
            self.controls[0].content.controls[2].opacity = 0
            self.update()

    # Generating the email extensions when user types the email
    def prefix_email_containers(self):
        email_labels = ["@gmail.com", "@hotmail.com"]
        label_title = ["GMAIL", "MAIL"]
        __ = ft.Row(spacing=1, alignment=ft.MainAxisAlignment.END)
        for index, label in enumerate(email_labels):
            # Append a container for each email server
            __.controls.append(
                ft.Container(
                    width=45,
                    height=30,
                    alignment=ft.alignment.center,
                    data=label,
                    on_click=lambda e: self.return_email_prefix(e),
                    content=ft.Text(
                        label_title[index],
                        size=9,
                        color="white",
                        weight=ft.FontWeight.BOLD,
                    ),
                )
            )
        return ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.END,
            spacing=2,
            opacity=0,
            animate_opacity=200,
            offset=ft.transform.Offset(0.35, 0),
            animate_offset=ft.animation.Animation(400, 'decelerate'),
            controls=[__],
        )

    # Simulating a green 'OK' check mark used during status 'OK' authentication
    def off_focus_input_check(self):
        return ft.Container(
            opacity=0,
            offset=ft.transform.Offset(0, 0),
            animate=200,
            border_radius=6,
            width=18,
            height=18,
            alignment=ft.alignment.center,
            content=ft.Checkbox(
                fill_color="#7df6dd",
                check_color="black",
                disabled=True,
            ),
        )

    def get_prefix_emails(self, e):
        if self.function_emails:
            email = self.controls[0].content.controls[1].value
            if e.data:
                if "@gmail.com" in email or "@hotmail.com" in email:
                    self.controls[0].content.controls[2].offset = ft.transform.Offset(0, 0)
                    self.controls[0].content.controls[2].opacity = 0
                    self.update()
                else:
                    self.controls[0].content.controls[2].offset = ft.transform.Offset(-0.15, 0)
                    self.controls[0].content.controls[2].opacity = 1
                    self.update()
            else:
                self.controls[0].content.controls[2].offset = ft.transform.Offset(0.5, 0)
                self.controls[0].content.controls[2].opacity = 0
                self.update()

    # Simulating the green checks (updated to handle both email and password)
    def get_green_check(self):
        email = self.controls[0].content.controls[1].value
        password = self.controls[0].content.controls[1].password

        # Check if it's an email field or password field
        if self.function_check and (email or password):
            if (
                ("@gmail.com" in email or "@hotmail.com" in email) or password
            ):
                # Simulating a delay for authentication
                self.controls[0].content.controls[3].offset = ft.transform.Offset(-2, 0)
                self.controls[0].content.controls[3].opacity = 1
                self.controls[0].content.controls[3].content.value = True
                self.update()
            else:
                # Hide the check if validation fails
                self.controls[0].content.controls[3].offset = ft.transform.Offset(0, 0)
                self.controls[0].content.controls[3].opacity = 0
                self.controls[0].content.controls[3].content.value = False
                self.update()

    def build(self):
        return ft.Container(
            width=320,
            height=40,
            border=ft.border.only(bottom=ft.border.BorderSide(0.5, "white54")),
            content=ft.Row(
                spacing=20,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(
                        name=self.icon_name,
                        size=14,
                        opacity=0.85,
                    ),
                    ft.TextField(
                        ref=self.input_ref,  # Reference the TextField
                        border_color="transparent",
                        bgcolor="transparent",
                        color=ft.colors.WHITE,
                        label_style=ft.TextStyle(color="white"),
                        height=20,
                        width=200,
                        text_size=12,
                        content_padding=3,
                        cursor_color="white",
                        hint_text=self.text_hint,
                        hint_style=ft.TextStyle(size=11),
                        password=self.hide,
                        on_change=lambda e: self.get_prefix_emails(e),
                        on_blur=lambda e: self.get_green_check()  # Removed the event parameter
                    ),
                    self.prefix_email_containers(),
                    self.off_focus_input_check(),
                ],
            ),
        )

email_ref = Ref[ft.TextField]()  # Reference for the email field
password_ref = Ref[ft.TextField]()  # Reference for the password field


def main(page: ft.Page):
    # Set page alignment and properties
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.title = "Sign In"
    # page.bgcolor = "#2f2f38"
    page.padding = 0
    page.spacing = 0

    def on_sign_in_click(e):
        try:
            email = email_ref.current.value  # Access email input using the reference
            password = password_ref.current.value  # Access password input using the reference
            user = auth.get_user_by_email(email)
            if user:
                page.snack_bar = ft.SnackBar(
                    ft.Column([
                        ft.Row([
                            ft.Text(f"Signing In", size=30, color="black"),
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
                            ft.Text(f"Error signing in: {error}", size=30, color="black"),
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
    right_column = ft.Card(
            width=500,
            height=page.height,
            elevation=20,
            color="#17171d",
            content=ft.Container(
                border_radius=6,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Divider(height=20, color='transparent'),
                        ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=5,
                            controls=[
                                ft.Row([
                                    ft.VerticalDivider(width=170, color=ft.colors.TRANSPARENT),
                                    ft.Text("Sign In", size=35, weight=ft.FontWeight.BOLD, color="white"),
                                ]),
                                ft.Row([
                                    ft.VerticalDivider(width=150, color=ft.colors.TRANSPARENT),
                                    ft.Text(
                                        "Web Vulnerability Scanner",
                                        size=13,
                                        color="white",
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                ])
                            ],
                        ),
                        ft.Divider(height=20, color='transparent'),
                        UserInputField(
                            ft.icons.PERSON_ROUNDED,
                            "Email",
                            False,
                            True,
                            True,
                            input_ref=email_ref
                        ),
                        ft.Divider(height=2, color='transparent'),
                        UserInputField(
                            ft.icons.LOCK_OPEN_ROUNDED,
                            "Password",
                            True,
                            False,
                            True,
                            input_ref=password_ref
                        ),
                        ft.Divider(height=2, color="transparent"),
                        ft.Row(
                            width=320,
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.TextButton("Create Account", scale=0.8, on_click=lambda e: e.page.go("/signup")),
                                ft.TextButton("Forget Password?", scale=0.8),
                            ],
                        ),
                        ft.Divider(height=45, color="transparent"),
                        ft.Container(
                            content=ft.ElevatedButton(
                                on_click=lambda e: on_sign_in_click(e),
                                content=ft.Text(
                                    "Sign In",
                                    size=13,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                # Custom styling
                                style=ft.ButtonStyle(
                                    shape={
                                        "": ft.RoundedRectangleBorder(radius=8),
                                    },
                                    color={
                                        "": "black",
                                    },
                                    bgcolor={"": "#7df6dd"},
                                ),
                                height=42,
                                width=320
                            )
                        ),
                        ft.Divider(height=45, color="transparent"),
                        ft.Text("CyberSpace @Copyright", size=10, color="white54")
                    ],
                ),
            ),
        )

    # Add the left and right columns into a row
    signin_content = ft.Container(
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
        content=signin_content,
        alignment=ft.alignment.bottom_center,  # Center the signup_content within the main container
        width=5000,
        height=635,  # Adjust height as needed
    )

    return ft.View(
        "/login",
        controls=[
            main_container
        ]
    )
