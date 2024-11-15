import flet as ft
# AND INSTALL SCAPY WITH PIP INSTALL SCAPY
from scapy.all import ARP, Ether, srp
import socket


def main(page: ft.Page):
    # INSERT IP ADDRESS FOR SCAN
    iptxt = ft.TextField(label="insert ip ")

    # CREATE TABLE FOR SEE RESULT OF YOUR SCANNING
    dt = ft.DataTable(
        columns=[
            ft.DataColumn(ft.ElevatedButton("Ip Address")),
            ft.DataColumn(ft.ElevatedButton("MAC Address")),
            ft.DataColumn(ft.ElevatedButton("Device name")),
        ],
        rows=[]

    )

    def scannow(e):
        # CLEAR ROWS FOR SEE RESULT AGAIN
        dt.rows.clear()

        # SHOW SNACK BAR
        page.snack_bar = ft.SnackBar(
            ft.Column([
                ft.Row([
                    ft.Text("scanning device.....", size=30, color="black"),
                    ft.ProgressRing(color="black")

                ], alignment="center")
            ], alignment="center"),
            bgcolor="#7df6dd"

        )
        page.snack_bar.open = True
        page.update()

        target_ip = iptxt.value
        arp = ARP(pdst=target_ip)
        # YOU FORMAT MAC ADDRESS
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp
        result = srp(packet, timeout=3, verbose=0)[0]

        clients = []
        # AND LOOP RESULT
        for sent, received in result:
            client = {"ip": received.psrc, "mac": received.hwsrc}

            # GET HOSTNAME DEVICE
            try:
                host_name = socket.gethostbyaddr(received.psrc)[0]
                client['device_name'] = host_name

            except:
                # IF DEVICE NAME NOT FOUND BRAND
                client['device_name'] = "N/A"
                clients.append(client)
        # SHOW DEVICE FOUND IN TERMINAL PRINT
        print("available device found ")
        print("IP" + " " * 15 + "MAC" + " " * 18 + "Device name")

        # AND PRINT RESULT IN FOR LOOP
        # AND PUSH RESULT TO DATATABLE
        for client in clients:
            print("{:16} 	{:17}  	{} ".format(client["ip"], client['mac'], client['device_name']))

            # PUSH TO DATATABLE
            dt.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(client['ip'])),
                        ft.DataCell(ft.Text(client['mac'])),
                        ft.DataCell(ft.Text(client['device_name'])),

                    ]

                )

            )
        page.update()

    page.add(
        ft.Column([
            ft.Text("Scan device in your network", size=30, weight="bold"),
            iptxt,

            ft.ElevatedButton("Show device",
                           bgcolor="red", color="white",
                           on_click=scannow
                           ),
            dt

        ])
    )


ft.app(target=main)
