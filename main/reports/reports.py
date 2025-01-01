import flet as ft
import firebase_admin
from firebase_admin import credentials, firestore
import threading
import concurrent.futures
import os
from dotenv import load_dotenv
load_dotenv()

database = os.getenv("database")

# Initialize Firebase Admin
if not firebase_admin._apps:
    cred = credentials.Certificate(fr"{database}")
    firebase_admin.initialize_app(cred)

db = firestore.client()


# Function to save a new folder to Firebase
def save_folder_to_firebase(folder_name):
    doc_ref = db.collection("Cyber-Folders").document()
    doc_ref.set({"name": folder_name})
    return doc_ref.id


# Function to load folders from Firebase
def load_folders():
    folders = []
    try:
        folders_ref = db.collection("Cyber-Folders").stream()
        for folder in folders_ref:
            folder_data = folder.to_dict()
            folder_data['id'] = folder.id
            folders.append(folder_data)
    except Exception as e:
        print(f"Error loading folders: {e}")
    return folders


# Function to load recent files from Firebase
def load_recent_files():
    recent_files = []
    try:
        files_ref = db.collection("Cyber-Files").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(5).stream()
        for file in files_ref:
            file_data = file.to_dict()
            recent_files.append(file_data)
    except Exception as e:
        print(f"Error loading recent files: {e}")
    return recent_files


def load_data(callback):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_folders = executor.submit(load_folders)
        future_recent_files = executor.submit(load_recent_files)

        folders_data = future_folders.result()
        recent_files_data = future_recent_files.result()
        callback(folders_data, recent_files_data)


def main(page: ft.Page):
    page.title = "Reports"

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
            dark_btn.icon = ft.icons.LIGHT_MODE
        else:
            page.theme_mode = ft.ThemeMode.DARK
            dark_btn.icon = ft.icons.DARK_MODE
        page.update()

    dark_btn = ft.IconButton(
        icon=ft.icons.DARK_MODE,
        icon_size=20,
        on_click=dark_mode,
    )

    # Load initial data
    folders_data = []
    recent_files_data = []

    # Function to update UI after loading data
    def update_ui(folders, recent_files):
        nonlocal folders_data, recent_files_data
        folders_data = folders
        recent_files_data = recent_files
        update_folders()

    threading.Thread(target=load_data, args=(update_ui,), daemon=True).start()

    def create_folder_dialog(e):
        folder_name_input = ft.TextField(label="Folder Name")
        dialog = ft.AlertDialog(
            title=ft.Text("Create New Folder"),
            content=folder_name_input,
            actions=[
                ft.ElevatedButton("Create", on_click=lambda e: on_create_click(folder_name_input, dialog)),
                ft.ElevatedButton("Cancel", on_click=lambda e: close_dialog(dialog)),
            ]
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def close_dialog(dialog):
        dialog.open = False
        page.update()

    def on_create_click(folder_name_input, dialog):
        folder_name = folder_name_input.value.strip()
        if folder_name:
            save_folder_to_firebase(folder_name)
            folders_data.append({"name": folder_name})
            close_dialog(dialog)
            update_folders()
        else:
            error_dialog = ft.AlertDialog(
                title=ft.Text("Folder name cannot be empty.", size=16),
                actions=[ft.ElevatedButton("OK", on_click=lambda e: close_dialog(error_dialog))]
            )
            page.dialog = error_dialog
            error_dialog.open = True
            page.update()

    def display_folder_content(folder_id):
        folder_details = db.collection("Cyber-Folders").document(folder_id).get().to_dict()
        if folder_details:
            dialog = ft.AlertDialog(
                title=ft.Text(folder_details.get('name', None)),
                content=ft.Text("Folder content goes here."),
                actions=[ft.ElevatedButton("Close", on_click=lambda e: close_dialog(dialog))]
            )
            dialog.open = True
            page.dialog = dialog
            page.update()
        else:
            error_dialog = ft.AlertDialog(
                title=ft.Text("Folder not found.", size=16),
                actions=[ft.ElevatedButton("OK", on_click=lambda e: close_dialog(error_dialog))]
            )
            page.dialog = error_dialog
            error_dialog.open = True
            page.update()

    def update_folders():
        folder_controls = []
        for folder in folders_data:
            folder_controls.append(
                ft.Card(
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Column(
                                        controls=[
                                            ft.Text(folder.get('name', None), size=16, weight=ft.FontWeight.BOLD, bgcolor="#17171d", color="white"),
                                            ft.Text("Details: Click to View.", bgcolor="#17171d", color="white")
                                        ]
                                    ),
                                    ft.ElevatedButton(
                                        "Open",
                                        on_click=lambda e, f=folder: display_folder_content(f.get('id', None)),
                                        style=ft.ButtonStyle(
                                            shape={"": ft.RoundedRectangleBorder(radius=8)},
                                            color={"": "black"},
                                            bgcolor={"": "#7df6dd"},
                                        )
                                    )
                                ],
                            )
                        ],
                        alignment=ft.alignment.center,
                        horizontal_alignment=ft.alignment.center,
                    ),
                    color="#17171d",
                    elevation=2,
                    margin=ft.margin.all(10),
                )
            )
        folders_content.controls = folder_controls
        page.update()

    folders_content = ft.Column()
    update_folders()

    sidebar_content = ft.Container(
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

    report_views = ft.Container(
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
                            ft.Text("Recent Files", size=18, weight=ft.FontWeight.BOLD, color="white"),
                            ft.Text("Folders", style="subtitle1", weight=ft.FontWeight.BOLD, color="white"),
                            ft.Divider(height=5, color=ft.colors.TRANSPARENT),
                            folders_content,  # This will hold the folder controls
                        ]
                    )
                )
            )
        )
    )
    report_views.visible = False  # Initially set to invisible
    dark_btn.visible = False

    def toggle_report_views(e):
        if e.control.value == "Recent":
            report_views.visible = True  # Show report_views if "Recent" is selected
            dark_btn.visible = True
        else:
            report_views.visible = False
            dark_btn.visible = False
        page.update()  # Update the page to reflect changes

    def folder1_view(e):
        dialog = ft.AlertDialog(
            title=ft.Text("Result"),
            content=ft.Column(
                controls=[
                    ft.Text("Folder content goes here."),
                ]
            ),
            actions=[
                ft.ElevatedButton("Close", on_click=lambda e: close_dialog(dialog))
            ],
        )
        # Open the new dialog
        dialog.open = True
        page.dialog = dialog  # Assign the dialog to page.dialog
        page.update()

    def folder2_view(e):
        dialog = ft.AlertDialog(
            title=ft.Text("Result"),
            content=ft.Column(
                controls=[
                    ft.Text("Folder content goes here."),
                ]
            ),
            actions=[
                ft.ElevatedButton("Close", on_click=lambda e: close_dialog(dialog))
            ],
        )
        # Open the new dialog
        dialog.open = True
        page.dialog = dialog  # Assign the dialog to page.dialog
        page.update()

    def folder3_view(e):
        dialog = ft.AlertDialog(
            title=ft.Text("Result"),
            content=ft.Column(
                controls=[
                    ft.Text("Folder content goes here."),
                ]
            ),
            actions=[
                ft.ElevatedButton("Close", on_click=lambda e: close_dialog(dialog))
            ],
        )
        # Open the new dialog
        dialog.open = True
        page.dialog = dialog  # Assign the dialog to page.dialog
        page.update()

    reports_content = ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Documents", size=24, weight=ft.FontWeight.BOLD),
                    ]
                ),
                ft.Divider(height=10),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            "New Folder",
                            on_click=create_folder_dialog,
                            style=ft.ButtonStyle(
                                shape={"": ft.RoundedRectangleBorder(radius=8)},
                                color={"": "black"},
                                bgcolor={"": "#7df6dd"},
                            )
                        ),
                        ft.ElevatedButton(
                            "Targets",
                            on_click=on_manage_targets_click,
                            style=ft.ButtonStyle(
                                shape={"": ft.RoundedRectangleBorder(radius=8)},
                                color={"": "black"},
                                bgcolor={"": "#7df6dd"},
                            )
                        ),
                        ft.Dropdown(
                            hint_text="Sort By: Folders",
                            width=160,
                            height=43,
                            border_radius=10,
                            options=[
                                ft.dropdown.Option("Recent"),
                                ft.dropdown.Option("Folders"),
                            ],
                            on_change=lambda e: toggle_report_views(e)  # Refresh folders on change
                        )
                    ],
                ),
                ft.Divider(height=20),
                ft.Text("Folders", style="subtitle1"),
                ft.Row(
                    controls=[
                        ft.Card(
                            content=ft.Container(
                                width=150,
                                height=100,
                                alignment=ft.alignment.center,
                                on_click=folder1_view,
                                content=ft.Text("Results 2024\n23 Files", size=16),
                            )
                        ),
                        ft.Card(
                            content=ft.Container(
                                width=150,
                                height=100,
                                alignment=ft.alignment.center,
                                on_click=folder2_view,
                                content=ft.Text("Market Analysis\n8 Files", size=16),
                            )
                        ),
                        ft.Card(
                            content=ft.Container(
                                width=150,
                                height=100,
                                alignment=ft.alignment.center,
                                on_click=folder3_view,
                                content=ft.Text("All Contracts\n37 Files", size=16),
                            )
                        ),
                    ],
                ),
                ft.Divider(height=20),
                ft.Text("Recent", style="subtitle1"),
                ft.ListTile(
                    width=200,
                    leading=ft.Icon(ft.icons.INSERT_DRIVE_FILE, color=ft.colors.BLUE_500),
                    title=ft.Text("Analysis Data"),
                    subtitle=ft.Text("Dec 15, 2024 - 1.8 MB", size=10),
                ),
                ft.ListTile(
                    width=200,
                    leading=ft.Icon(ft.icons.INSERT_DRIVE_FILE, color=ft.colors.BLUE_500),
                    title=ft.Text("Scan Results"),
                    subtitle=ft.Text("Nov 30, 2024 - 2.5 MB", size=10),
                ),
            ],
        ),
    )

    return ft.View(
        "/reports",
        controls=[
            ft.Row(
                controls=[
                    sidebar_content,
                    ft.VerticalDivider(width=1, color=ft.colors.TRANSPARENT),
                    reports_content,
                    ft.VerticalDivider(width=150, color=ft.colors.TRANSPARENT),
                    report_views,
                    ft.Container(
                        content=dark_btn,
                        alignment=ft.alignment.top_right,
                        padding=ft.padding.only(left=0, top=20),
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                expand=True
            )
        ]
    )
