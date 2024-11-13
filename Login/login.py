import flet as ft
import time
import sys
import os
from math import pi
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class SignInButton(ft.UserControl):
    def __init__(self, btn_name):
        self.btn_name = btn_name
        super().__init__()

    def build(self):
        return ft.Container(
            content=ft.ElevatedButton(
                content=ft.Text(
                    self.btn_name,
                    size=13,
                    weight="bold"
                ),
                # Custom styling
                style = ft.ButtonStyle(
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
        )

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
            bgcolor=self.bg_color,
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
    red_box = page.controls[0].content.content.controls[1].controls[0].controls[0]
    blue_box = page.controls[0].content.content.controls[1].controls[1].controls[0]

    # Implement a counter to reverse the rotation direction
    counter = 0
    while True:
        # rotate 4x before switching directions
        if counter >= 0 and counter <= 4:
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
        if counter >= 5 and counter <= 10:
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
    def __init__(self, icon_name, text_hint, hide, function_emails: bool, function_check: bool):
        self.icon_name = icon_name
        self.text_hint = text_hint
        self.hide = hide
        self.function_emails = function_emails
        self.function_check = function_check
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
                        weight="bold",
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
                        border_color="transparent",
                        bgcolor="transparent",
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

def main(page: ft.Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.title = "Sign In"
    # page.bgcolor = "#F3F4F6"

    page.add(
        ft.Card(
            width=1000,
            height=600,
            elevation=15,
            # color="#F3F4F6",
            content=ft.Container(
                border_radius=6,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Divider(height=40, color='transparent'),
                        ft.Stack(
                            controls=[
                                AnimatedBox("#e9665a", None, 0),
                                AnimatedBox("#7df6dd", "23262a", pi / 4),
                            ]
                        ),
                        ft.Divider(height=20, color='transparent'),
                        ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=5,
                            controls=[
                                ft.Text("Sign In", size=22, weight="bold"),
                                ft.Text(
                                    "Web Vulnerability Scanner",
                                    size=13,
                                    weight="bold",
                                ),
                            ],
                        ),
                        ft.Divider(height=20, color='transparent'),
                        UserInputField(
                            ft.icons.PERSON_ROUNDED,
                            "Email",
                            False,
                            True,
                            True,
                        ),
                        ft.Divider(height=2, color='transparent'),
                        UserInputField(
                            ft.icons.LOCK_OPEN_ROUNDED,
                            "Password",
                            True,
                            False,
                            True,
                        ),
                        ft.Divider(height=2, color="transparent"),
                        ft.Row(
                            width=320,
                            alignment=ft.MainAxisAlignment.END,
                            controls=[
                                ft.TextButton("Forget Password?", scale=0.8),
                            ],
                        ),
                        ft.Divider(height=45, color="transparent"),
                        SignInButton("Sign In"),
                        ft.Divider(height=45, color="transparent"),
                        ft.Text("CyberSpace @Copyright", size=10, color="white54")
                    ],
                ),
            ),
        )
    )

    page.update()
    asyncio.run(animate_boxes(page))

if __name__ == '__main__':
    ft.app(target=main)
