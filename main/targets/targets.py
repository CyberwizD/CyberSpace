import flet as ft
import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

load_dotenv()

database = os.getenv("database")

# Initialize Firebase Admin
if not firebase_admin._apps:
    cred = credentials.Certificate(fr"{database}")
    firebase_admin.initialize_app(cred)

db = firestore.client()


def main(page: ft.Page):
    page.title = "Targets"

    def on_signup_click(e):
        e.page.go("/signup")

    def on_dashboard_click(e):
        e.page.go("/dashboard")

    def on_start_scan_click(e):
        e.page.go("/scans")

    def on_manage_targets_click(e):
        e.page.go("/targets")

    def integration_click(e):
        e.page.go("/integration")

    def reports_click(e):
        e.page.go("/reports")

    def dark_mode(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            dark_btn.icon = ft.icons.LIGHT_MODE  # Update the icon to indicate light mode
        else:
            page.theme_mode = ft.ThemeMode.DARK
            dark_btn.icon = ft.icons.DARK_MODE  # Update the icon to indicate dark mode
        page.update()

    dark_btn = ft.IconButton(
        icon=ft.icons.DARK_MODE,
        icon_size=20,
        on_click=dark_mode,
    )

    sidebar_content = ft.Container(
        width=250,
        bgcolor="#1e1e2f",
        padding=20,
        border_radius=ft.border.only(right=ft.border.BorderSide(1, "white")),
        content=ft.Column(
            controls=[
                ft.Text("CyberSpace", size=30, weight=ft.FontWeight.BOLD, color="white"),
                ft.Divider(height=20, color="transparent"),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.DASHBOARD, color="white"),
                    title=ft.Text("Dashboard", color="white"),
                    on_click=lambda e: on_dashboard_click(e),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.GPS_FIXED, color="white"),
                    title=ft.Text("Targets", color="white"),
                    on_click=lambda e: on_manage_targets_click(e)
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.SCANNER, color="white"),
                    title=ft.Text("Scans", color="white"),
                    on_click=lambda e: on_start_scan_click(e)
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.INTEGRATION_INSTRUCTIONS, color="white"),
                    title=ft.Text("Integrations", color="white"),
                    on_click=lambda e: integration_click(e)
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.REPORT, color="white"),
                    title=ft.Text("Reports", color="white"),
                    on_click=lambda e: reports_click(e)
                ),
                ft.Divider(height=250, color=ft.colors.TRANSPARENT),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.ARROW_BACK_ROUNDED, color="white"),
                    title=ft.Text("Log Out", color="white"),
                    on_click=on_signup_click
                )
            ],
        ),
    )

    def fetch_targets_from_firebase(url):
        targets = []
        try:
            # Correctly using keyword arguments
            targets_ref = db.collection("Cyber-Reports").where(field_path="url", op_string="==", value=url).stream()
            for target in targets_ref:
                target_data = target.to_dict()
                targets.append(target_data)
        except Exception as e:
            print(f"Error fetching targets: {e}")
        return targets

    def view_targets(e):
        url = target_input.value.strip()  # Get the URL from the input field
        if url:
            filtered_targets = fetch_targets_from_firebase(url)
            if filtered_targets:
                target_views.content = ft.Column(controls=[
                    ft.Text("Filtered Targets:", size=18, weight=ft.FontWeight.BOLD, color="white"),
                    *[
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.LINK, color="blue"),
                            title=ft.Text(target['name']),  # Adjust based on your data structure
                            subtitle=ft.Text(target['url']),
                        )
                        for target in filtered_targets
                    ]
                ])
            else:
                target_views.content = ft.Container(
                    padding=ft.padding.only(top=10, bottom=10),
                    content=(
                        ft.Card(
                            content=ft.Container(
                                padding=20,
                                width=300,
                                border_radius=10,
                                bgcolor="#17171d",
                                content=ft.Column(
                                    controls=[
                                        ft.Text("Targets Overview", size=18, weight=ft.FontWeight.BOLD, color="white"),
                                        ft.Text("Details about your targets will be displayed here.", color="white"),
                                        ft.Divider(height=5, color=ft.colors.TRANSPARENT),
                                        ft.Text("No targets found for the entered URL.", color="white")
                                    ]
                                )
                            )
                        )
                    )
                )
        else:
            target_views.content = ft.Container(
                padding=ft.padding.only(top=10, bottom=10),
                content=(
                    ft.Card(
                        content=ft.Container(
                            padding=20,
                            width=300,
                            border_radius=10,
                            bgcolor="#17171d",
                            content=ft.Column(
                                controls=[
                                    ft.Text("Targets Overview", size=18, weight=ft.FontWeight.BOLD, color="white"),
                                    ft.Text("Details about your targets will be displayed here.", color="white"),
                                    ft.Divider(height=5, color=ft.colors.TRANSPARENT),
                                    ft.Text("Please enter a URL to search.", color="white")
                                ]
                            )
                        )
                    )
                )
            )

        target_views.visible = True  # Show the target views
        page.update()  # Update the page to reflect changes

    target_views = ft.Container(
        padding=ft.padding.only(top=10, bottom=10),
        content=(
            ft.Card(
                content=ft.Container(
                    padding=20,
                    width=300,
                    border_radius=10,
                    bgcolor="#17171d",
                    content=ft.Column(
                        controls=[
                            ft.Text("Targets Overview", size=18, weight=ft.FontWeight.BOLD, color="white"),
                            ft.Text("Details about your targets will be displayed here.", color="white"),
                        ]
                    )
                )
            )
        )
    )
    target_views.visible = False  # Initially set to invisible

    def view_targets_page(e):
        target_views.visible = not target_views.visible  # Toggle visibility
        page.update()  # Update the page to reflect changes

    target_content = ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Workspaces and Targets", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(height=10),
                ft.Row(
                    controls=[
                        ft.Container(
                            width=200,
                            content=ft.Column(
                                controls=[
                                    ft.Text("Workspaces", size=18, weight=ft.FontWeight.BOLD),
                                    ft.ListTile(
                                        leading=ft.Icon(ft.icons.PERSON, color="blue"),
                                        title=ft.Text("Personal Space"),
                                    ),
                                    ft.TextField(hint_text="Search workspaces..."),

                                    ft.Divider(height=10),
                                    ft.Text("Recent", style="subtitle1"),
                                    ft.ListTile(
                                        leading=ft.Icon(ft.icons.API_SHARP, color="green"),
                                        title=ft.Text("API Tests"),
                                    ),
                                    ft.Text("Workspaces", style="subtitle1"),
                                    ft.ListTile(
                                        leading=ft.Icon(ft.icons.ALL_OUT, color=ft.colors.ON_SURFACE),
                                        title=ft.Text("All Workspaces"),
                                    ),
                                    ft.ListTile(
                                        leading=ft.Icon(ft.icons.BUSINESS, color=ft.colors.BLUE_ACCENT),
                                        title=ft.Text("Company Workspace"),
                                    ),
                                ],
                            ),
                        ),
                        ft.VerticalDivider(width=10),
                        ft.Container(
                            width=400,
                            content=ft.Column(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Text("Targets", size=18, weight=ft.FontWeight.BOLD),
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                    ),
                                    ft.Row(
                                        controls=[
                                            target_input := ft.TextField(hint_text="Search by url, target name...",
                                                                         width=300),
                                            ft.ElevatedButton(
                                                "Search",
                                                on_click=view_targets,
                                                style=ft.ButtonStyle(
                                                    shape={"": ft.RoundedRectangleBorder(radius=8)},
                                                    color={"": "black"},
                                                    bgcolor={"": "#7df6dd"},
                                                )
                                            )
                                        ]
                                    ),
                                    ft.Divider(height=10),
                                    ft.Text("Favorites", style="subtitle1"),
                                    ft.ListTile(
                                        leading=ft.Icon(ft.icons.APPS, color="teal"),
                                        title=ft.Text("Web Pentest"),
                                        subtitle=ft.Text("APIs - Delivery Completed", size=10),
                                    ),
                                    ft.Text("Pending Setup", style="subtitle1"),
                                    ft.ListTile(
                                        leading=ft.Icon(ft.icons.MOBILE_FRIENDLY, color=ft.colors.LIGHT_BLUE),
                                        title=ft.Text("Mobile"),
                                        subtitle=ft.Text("iOS App - Pending", size=10),
                                    ),
                                    ft.ListTile(
                                        leading=ft.Icon(ft.icons.CLOUD, color="grey"),
                                        title=ft.Text("Azure"),
                                        subtitle=ft.Text("Cloud Infra - Pending", size=10),
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ],
        ),
    )

    return ft.View(
        "/targets",
        controls=[
            ft.Row(
                controls=[
                    ft.Row(
                        controls=[
                            sidebar_content,
                            ft.VerticalDivider(width=1, color=ft.colors.TRANSPARENT),
                            target_content,
                            ft.VerticalDivider(width=1, color=ft.colors.TRANSPARENT),
                            target_views,
                            ft.Container(
                                content=dark_btn,
                                alignment=ft.alignment.top_right,
                                padding=ft.padding.only(left=0, top=20),
                            ),
                        ],
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
                expand=True
            )
        ]
    )
