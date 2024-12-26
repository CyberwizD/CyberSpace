import firebase_admin
from firebase_admin import credentials, firestore
import subprocess
import flet as ft
import pandas as pd
import json
import time
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

WP_API_TOKEN = os.getenv("WP_API_TOKEN")
OWASP_ZAP_API_KEY = os.getenv("OWASP_ZAP_API_KEY")
database = os.getenv("database")

# Initialize Firebase Admin
if not firebase_admin._apps:
    cred = credentials.Certificate(fr"{database}")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# url = https://wpscan.com/api/v3/wordpresses/494
# url = http://hackthissite.com

# Function to save data to Firebase
def save_to_firebase(data):
    doc_ref = db.collection("Cyber-Reports").document()
    doc_ref.set(data)
    return doc_ref.id

def main(page: ft.Page):
    page.title = "Integrations"

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

    # ListView to display scan results
    scan_output_view = ft.ListView(
        height=400,
        padding=10,
        expand=True,
        auto_scroll=True,
        controls=[
            # ft.Text(value="Scan results will be displayed here...", size=14, selectable=True),
            ft.Text("Connected Integrations", style="subtitle1"),
            ft.ListTile(
                leading=ft.Icon(ft.icons.API, color="blue"),
                title=ft.Text("Nessus"),
                subtitle=ft.Text("Active", size=10),
                trailing=ft.TextButton("Configure"),
            ),
            ft.ListTile(
                leading=ft.Icon(ft.icons.THUNDERSTORM, color="blue"),
                title=ft.Text("OWASP ZAP"),
                subtitle=ft.Text("Active", size=10),
                trailing=ft.TextButton("Configure"),
            ),
            ft.ListTile(
                leading=ft.Icon(ft.icons.APPS, color="blue"),
                title=ft.Text("WPScan"),
                subtitle=ft.Text("Inactive", size=10),
                trailing=ft.TextButton("Configure"),
            ),
            ft.Divider(height=10, color=ft.colors.TRANSPARENT),
            ft.Text("CLI Integrations", style="subtitle1"),
            ft.ListTile(
                leading=ft.Icon(ft.icons.SCANNER, color="#7df6dd"),
                title=ft.Text("Nmap"),
                trailing=ft.TextButton("Connect"),
            ),
            ft.ListTile(
                leading=ft.Icon(ft.icons.WEB, color="#7df6dd"),
                title=ft.Text("Wapiti"),
                trailing=ft.TextButton("Connect"),
            ),
            ft.ListTile(
                leading=ft.Icon(ft.icons.WEBHOOK, color="#7df6dd"),
                title=ft.Text("Nikto"),
                trailing=ft.TextButton("Connect"),
            ),
            ft.ListTile(
                leading=ft.Icon(ft.icons.CALENDAR_TODAY, color="#7df6dd"),
                title=ft.Text("SqlMap"),
                trailing=ft.TextButton("Connect"),
            ),
            ft.Divider(height=5, color=ft.colors.TRANSPARENT)
        ]
    )

    # Function to handle WPScan input and run the WPScan command
    def run_wpscan_scan(input_url):
        command = f'curl --ssl-no-revoke -H "Authorization: Token token={WP_API_TOKEN}" {input_url}'

        # Run the scan using subprocess
        wpscan_output = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Parse the JSON output
        try:
            json_data = json.loads(wpscan_output.stdout)  # Convert output to json
            document_id = save_to_firebase({"Scan Result": json_data})  # Save to Firebase

            # Convert the JSON to a Pandas DataFrame
            df = pd.json_normalize(json_data, record_path=['4.9.4', 'vulnerabilities'], meta=[
                ['4.9.4', 'release_date'],
                ['4.9.4', 'changelog_url'],
                ['4.9.4', 'status']
            ])

            # Clear previous results and update the scan_output_view with the table
            scan_output_view.controls.clear()

            # Create a DataTable to display scan results
            table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Vulnerability ID")),
                    ft.DataColumn(ft.Text("Title")),
                    # ft.DataColumn(ft.Text("CVE")),
                    ft.DataColumn(ft.Text("Created At")),
                    ft.DataColumn(ft.Text("Vulnerability Type")),
                    # ft.DataColumn(ft.Text("Published Date"))
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(row['id']))),
                            ft.DataCell(ft.Text(str(row['title']))),
                            # ft.DataCell(ft.Text(", ".join(row.get('cve', [])))),
                            ft.DataCell(ft.Text(str(row['created_at']))),
                            ft.DataCell(ft.Text(str(row['vuln_type']))),
                            # ft.DataCell(ft.Text(str(row['published_date'])))
                        ]
                    ) for index, row in df.iterrows()
                ]
            )

            # Add the table to the ListView
            scan_output_view.controls.append(table)
            page.update()

            page.dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Scan Complete"),
                content=ft.Text(f"Scan saved with ID: {document_id}"),
                actions=[
                    ft.TextButton(
                        "OK",
                        # style=ft.ButtonStyle(color=ft.colors.WHITE),
                        on_click=close_dialog  # Close dialog on "OK"
                    )
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            page.dialog.open = True
            page.update()

        except json.JSONDecodeError as e:
            # Handle JSON parsing errors
            #scan_output_view.controls.clear()
            scan_output_view.visible = False
            scan_output_view.controls.append(
                ft.Text(f"WPScan Error: {e}", size=14, selectable=True, weight="bold")
            )
            page.update()

            scan_output_view.visible = True
            page.update()

    async def display_alert_summary(target_url):
        zap_alert_summary = f"http://localhost:8080/JSON/alert/view/alertsSummary/?apikey={OWASP_ZAP_API_KEY}&baseurl={target_url}"

        # Clear previous results and add a loading indicator
        #scan_output_view.controls.clear()
        loading_text = ft.Text("Fetching alert summary...", size=16, weight="bold")
        scan_output_view.controls.append(loading_text)

        # Center the loading indicator in a Snackbar
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
        page.update()

        try:
            # Fetch the alert summary asynchronously
            result = await asyncio.to_thread(subprocess.run, ['curl', zap_alert_summary], shell=True,
                                             capture_output=True, text=True)
            zap_output = result.stdout

            # Remove loading indicator after fetching data
            scan_output_view.controls.remove(loading_text)
            page.snack_bar.open = False
            page.update()

            # Parse the JSON response
            json_data = json.loads(zap_output)

            # Prepare the rows for the DataFrame
            rows = []
            for severity, alerts in json_data.items():
                if isinstance(alerts, list):
                    for alert in alerts:
                        rows.append({
                            "Risk": severity,
                            "Name": alert.get("name", "N/A"),
                            "Confidence": alert.get("confidence", "N/A"),
                            "URL": alert.get("url", "N/A"),
                        })

            if rows:
                df = pd.DataFrame(rows)

                # Create a DataTable for the alert summary with styling
                table = ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Risk")),
                        ft.DataColumn(ft.Text("Name")),
                        ft.DataColumn(ft.Text("Confidence")),
                        ft.DataColumn(ft.Text("URL")),
                    ],
                    rows=[
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(row["Risk"],
                                                    color="red" if row["Risk"] == "High" else "orange" if row[
                                                                                                              "Risk"] == "Medium" else "green")),
                                ft.DataCell(ft.Text(row["Name"], color="blue")),
                                ft.DataCell(ft.Text(row["Confidence"], color="black")),
                                ft.DataCell(ft.Text(row["URL"], color="black")),
                            ]
                        ) for _, row in df.iterrows()
                    ],
                    style={"border": "1px solid #ccc", "border-radius": "5px", "padding": "10px"}
                )

                # Add the table to the ListView
                scan_output_view.controls.append(ft.Text("Alert Summary", size=20, weight="bold", color="black"))
                scan_output_view.controls.append(table)

                # Add animation effect for a smooth display
                for i in range(3):
                    await asyncio.sleep(0.5)  # Simulate delay
                    scan_output_view.controls[-1].opacity = i / 3
                    page.update()

                scan_output_view.controls[-1].opacity = 1  # Ensure fully visible
                page.update()

            else:
                # If no alerts are found, create and show an alert dialog
                alert = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("No alerts found in the summary."),
                    content=ft.Text("Re-Scan to check for alerts."),
                )
                page.dialog = alert
                page.dialog.open = True
                page.update()

                # Close the dialog after 3 seconds
                await asyncio.sleep(3)
                page.dialog.open = False
                page.update()

        except Exception as e:
            # Handle errors (e.g., JSON parsing errors or API call failures)
            scan_output_view.controls.append(
                ft.Text(f"Error fetching or processing alert summary: {e}", size=14, selectable=True)
            )
            page.update()

    def run_owasp_zap_scan(target_url):
        zap_start_ajax_spider = f"http://localhost:8080/JSON/spider/action/scan/?apikey={OWASP_ZAP_API_KEY}&url={target_url}&maxChildren=&recurse=true&contextName=&subtreeOnly="
        zap_api_url = f"http://localhost:8080/JSON/ascan/action/scan/?apikey={OWASP_ZAP_API_KEY}&url={target_url}&recurse=true&inScopeOnly=&scanPolicyName=&method=&postData=&contextId="
        zap_alert_json_report = f"http://localhost:8080/JSON/alert/view/alertsByRisk/?apikey={OWASP_ZAP_API_KEY}&url={target_url}&recurse=True"
        zap_alert_summary = f"http://localhost:8080/JSON/alert/view/alertsSummary/?apikey={OWASP_ZAP_API_KEY}&baseurl={target_url}"

        # Step 1: Run the AJAX spider
        try:
            result = subprocess.run(['curl', zap_start_ajax_spider], shell=True, capture_output=True, text=True)
            zap_output = result.stdout

            # Display the dialog that the spidering is done
            page.dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Spider Crawling Completed"),
                content=ft.Text(f"Spider has finished crawling '{target_url}'."),
            )
            page.dialog.open = True
            page.update()

            # Wait for 5 seconds before closing the dialog
            time.sleep(3)
            page.dialog.open = False
            page.update()

        except json.JSONDecodeError as e:
            scan_output_view.controls.clear()
            scan_output_view.controls.append(
                ft.Text(f"Error running Spider: {e}", size=14, selectable=True)
            )
            page.update()
            return

        # Step 2: Start the active scan using zap_api_url
        try:
            result = subprocess.run(['curl', zap_api_url], shell=True, capture_output=True, text=True)
            zap_output = result.stdout

            # Parse the JSON to get the scan ID
            json_data = json.loads(zap_output)
            scan_id = json_data.get('scan')

            # Update the scan output view to show the progress of the scan
            alert = ft.AlertDialog(
                modal=True,
                title=ft.Text(f"Scanning {target_url}"),
                content=ft.Text(f"Scan in progress... Scan ID: {233})", size=14),
                actions=[
                    ft.TextButton("OK", on_click=lambda e: close_dialog(e))
                ]
            )
            page.dialog = alert
            page.dialog.open = True
            page.update()

            time.sleep(3)
            page.dialog.open = False
            page.update()

            #scan_output_view.controls.clear()
            scan_output_view.controls.append(
                ft.Text(f"Active Scan in progress... (Scan ID: {scan_id})", size=14, weight="bold")
            )
            # scan_output_view.visible = False       ##########  Working on this  #########
            page.update()

            # Poll the ZAP API to check scan progress (this will simulate real-time progress updates)
            scan_complete = False
            while not scan_complete:
                progress_url = f"http://localhost:8080/JSON/ascan/view/status/?apikey={OWASP_ZAP_API_KEY}&scanId={scan_id}"
                progress_result = subprocess.run(['curl', progress_url], shell=True, capture_output=True, text=True)
                progress_data = json.loads(progress_result.stdout)

                progress = progress_data.get('status', 0)
                scan_output_view.controls[-1].value = f"Active Scan progress: {progress}%"
                page.update()

                if progress == '100':  # When scan is complete
                    scan_complete = True
                time.sleep(2)  # Poll every 2 seconds for updates

        except json.JSONDecodeError as e:
            scan_output_view.controls.clear()
            scan_output_view.controls.append(
                ft.Text(f"Error running active scan: {e}", size=14, selectable=True)
            )
            page.update()
            return

        # Step 3: Fetch the alert report using zap_alert_json_report and save it to Firebase
        try:
            result = subprocess.run(['curl', zap_alert_json_report], shell=True, capture_output=True, text=True)
            zap_output = result.stdout

            # Parse the final alert report
            json_data = json.loads(zap_output)
            document_id = save_to_firebase({"Scan Result": json_data})

            # Display the final results on the GUI
            #scan_output_view.controls.clear()
            scan_output_view.controls.append(
                ft.Text(f"Final Scan Report Saved (Document ID: {document_id})", size=14, weight="bold")
            )

            # Call the function to display the alert summary
            asyncio.run(display_alert_summary(target_url))

            # Example of displaying some scan data
            for alert in json_data.get('alerts', []):
                scan_output_view.controls.append(
                    ft.Text(f"Alert: {alert['name']} - Risk: {alert['risk']}", size=12)
                )

            page.update()

            # Display a success dialog
            page.dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("OWASP ZAP Scan Completed"),
                content=ft.Text(f"Scan saved with ID: {document_id}"),
            )
            page.dialog.open = True
            page.update()

            # Close the dialog after 5 seconds
            time.sleep(3)
            page.dialog.open = False
            page.update()

            scan_output_view.visible = True
            page.update()

        except json.JSONDecodeError as e:
            scan_output_view.controls.clear()
            scan_output_view.controls.append(
                ft.Text(f"Error fetching ZAP report: {e}", size=14, selectable=True)
            )
            page.update()

    # Function to close the dialog
    def close_dialog(e=None):
        page.dialog.open = False  # Close the dialog
        page.update()  # Update the page to reflect the changes

    def request_click(e):
        # Create an alert dialog for integrations
        url_input = ft.TextField(
            hint_text="Enter a web URL to scan",
        )

        def submit_input_wp_scan(e):
            # Run the WPScan and display results
            run_wpscan_scan(url_input.value)
            close_dialog()  # Close dialog after submission

        def submit_input_owasp_zap(e):
            # Run the OWASP ZAP scan and display results
            run_owasp_zap_scan(url_input.value)
            close_dialog()  # Close dialog after submission

        page.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Select Software Integration"),
            content=url_input,  # Use the TextField for input
            actions=[
                ft.TextButton(
                    "WPScan",
                    #style=ft.ButtonStyle(color=ft.colors.WHITE),
                    on_click=submit_input_wp_scan  # Trigger WPScan on button click
                ),
                ft.TextButton(
                    "OWASP ZAP",
                    #style=ft.ButtonStyle(color=ft.colors.WHITE),
                    on_click=submit_input_owasp_zap  # Trigger OWASP ZAP on button click
                ),
                ft.TextButton(
                    "Back",
                    #style=ft.ButtonStyle(color=ft.colors.WHITE),
                    on_click=close_dialog  # Close the dialog on "Back"
                )
            ],
            actions_alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        )
        page.dialog.open = True  # Open the dialog
        page.update()  # Update the page

    content_container = ft.Container(
        expand=True,
        content=ft.Column(
            controls=[
                ft.Container(
                    padding=20,
                    content=ft.Column(
                        controls=[
                            ft.Text("Integrations", size=24, weight="bold"),
                            ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                            ft.Text("Unlock the full power of CyberSpace with additional apps.", size=16),
                            ft.Divider(height=5, color=ft.colors.TRANSPARENT),
                            ft.Row(
                                controls=[
                                    ft.ElevatedButton(
                                        "Request Integration",
                                        on_click=request_click,
                                        style=ft.ButtonStyle(
                                            shape={"": ft.RoundedRectangleBorder(radius=8)},
                                            color={"": "black"},
                                            bgcolor={"": "#7df6dd"},
                                        )
                                    ),
                                    ft.VerticalDivider(width=2, color=ft.colors.TRANSPARENT),
                                    ft.ElevatedButton(
                                        "API Keys",
                                        style=ft.ButtonStyle(
                                            shape={"": ft.RoundedRectangleBorder(radius=8)},
                                            color={"": "black"},
                                            bgcolor={"": "#7df6dd"},
                                        )
                                    ),
                                ],
                            ),
                            #ft.Divider(height=5),
                        ],
                    ),
                ),
                scan_output_view,  # Display scan results here
            ]
        ),
    )

    return ft.View(
        "/integration",
        controls=[
            ft.Row(
                controls=[
                    sidebar_content,
                    content_container,
                    ft.Container(
                        content=dark_btn,
                        alignment=ft.alignment.top_right,
                        padding=ft.padding.only(left=0, top=20),
                    ),
                ],
                expand=True
            )
        ]
    )
