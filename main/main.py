import flet as ft
from cover import cover
from signup import signup
from login import login
from dashboard import dashboard
from targets import targets
from scans import scans
from integration import integration
from reports import reports


def main(page: ft.Page):
    # Store the current route in the page session
    page.title = "CyberSpace"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    # page.window.title_bar_hidden = True
    # page.window.title_bar_buttons_hidden = True

    # Define a function to handle routing
    def route_change(route):
        page.views.clear()
        print(f"Navigating to: {route}")  # Debugging line to show current route

        if page.route == "/":
            # Show Cover page
            cover_page = cover.main(page)
            page.views.append(cover_page)
        elif page.route == "/signup":
            # Show Signup page
            signup_page = signup.main(page)
            page.views.append(signup_page)
        elif page.route == "/login":
            # Show Login page
            login_page = login.main(page)
            page.views.append(login_page)
        elif page.route == "/dashboard":
            # Show Dashboard page
            dashboard_page = dashboard.main(page)
            page.views.append(dashboard_page)
        elif page.route == "/scans":
            # Show Scans page
            scans_page = scans.main(page)
            page.views.append(scans_page)
        elif page.route == "/targets":
            # Show Targets page
            targets_page = targets.main(page)
            page.views.append(targets_page)
        elif page.route == "/integration":
            # Show Integration page
            integration_page = integration.main(page)
            page.views.append(integration_page)
        elif page.route == "/reports":
            # Show Reports page
            reports_page = reports.main(page)
            page.views.append(reports_page)

        page.update()

    # Listen to route changes
    page.on_route_change = route_change

    # Navigate to the initial route
    page.go("/")


# Run the app
if __name__ == "__main__":
    ft.app(target=main)
