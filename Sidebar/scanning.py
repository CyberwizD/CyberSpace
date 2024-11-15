import flet as ft
from datetime import date
import time

def main(page: ft.Page):
    page.title = "Scanning"

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

    def start_scan(e):
        e.page.go("/scanning")

    def create_pie_chart():
        normal_radius = 50
        hover_radius = 60
        normal_title_style = ft.TextStyle(
            size=16, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD
        )
        hover_title_style = ft.TextStyle(
            size=22,
            color=ft.colors.WHITE,
            weight=ft.FontWeight.BOLD,
            shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.BLACK54),
        )

        def on_chart_event(e: ft.PieChartEvent):
            for idx, section in enumerate(chart.sections):
                if idx == e.section_index:
                    section.radius = hover_radius
                    section.title_style = hover_title_style
                else:
                    section.radius = normal_radius
                    section.title_style = normal_title_style
            chart.update()

        chart = ft.PieChart(
            sections=[
                ft.PieChartSection(
                    40,
                    title="40%",
                    title_style=normal_title_style,
                    color=ft.colors.BLUE,
                    radius=normal_radius,
                ),
                ft.PieChartSection(
                    30,
                    title="30%",
                    title_style=normal_title_style,
                    color=ft.colors.YELLOW,
                    radius=normal_radius,
                ),
                ft.PieChartSection(
                    15,
                    title="15%",
                    title_style=normal_title_style,
                    color=ft.colors.PURPLE,
                    radius=normal_radius,
                ),
                ft.PieChartSection(
                    15,
                    title="15%",
                    title_style=normal_title_style,
                    color=ft.colors.GREEN,
                    radius=normal_radius,
                ),
            ],
            sections_space=0,
            center_space_radius=40,
            on_chart_event=on_chart_event,
            expand=True,
        )
        return chart

    page.add(create_pie_chart())

    page.snack_bar = ft.SnackBar(
        ft.Column([
            ft.Row([
                ft.Text("Scanning... Please wait!", size=30, color="black"),
                ft.ProgressRing(color="black")

            ], alignment="center")
        ], alignment="center"),
        bgcolor="#7df6dd"
    )
    page.snack_bar.open = True

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
            ],
        ),
    )

    scans_content = ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Automated App Scan (Full)", size=24, weight="bold"),
                ft.Divider(height=10),
                ft.Row(
                    controls=[
                        ft.Text("In Progress -", size=16),
                        ft.ElevatedButton(f"Date: {date.today().strftime('%b-%d-%Y')}", color="White"),
                        ft.ElevatedButton(f"Time: {time.strftime("%H:%M %p", time.localtime())}", color="white")
                    ]
                ),
                # ft.Divider(height=0),
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text("Vulnerabilities", size=18, weight="bold"),
                                ft.Text(value="Some description goes here", height=200),
                            ]
                        ),
                        ft.VerticalDivider(width=500, color="transparent"),
                        ft.Column(
                            controls=[
                                ft.Text("Scan Details", size=18, weight="bold"),
                                ft.Column(
                                    controls=[
                                        ft.Text("Policy:  Web Application Tests"),
                                        ft.Text("Status:  Completed"),
                                        ft.Text("Security Base:  CVSS v3.0"),
                                        ft.Text("Scanner:  Local Scanner"),
                                        ft.Text(f"Start:  {date.today().strftime('%b-%d')} at {time.strftime("%H:%M %p", time.localtime())}"),
                                        ft.Text(f"End:  {date.today().strftime('%b-%d')} at {time.sleep(5)}"),
                                        ft.Text("Elasped:  2 hours"),
                                        ft.Divider(height=20),
                                        # create_pie_chart()
                                    ]
                                ),
                            ]
                        )
                    ]
                )
            ],
        ),
    )

    return ft.View(
        "/scans",
        controls=[
            ft.Row(
                controls=[
                    # page.snack_bar,
                    sidebar_content,
                    ft.VerticalDivider(width=1, color=ft.colors.TRANSPARENT),
                    scans_content,
                    page.snack_bar,

                ],
                alignment=ft.MainAxisAlignment.START,
                expand=True
            )
        ]
    )
