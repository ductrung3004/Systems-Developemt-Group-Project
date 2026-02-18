import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from base_dashboard import *
import flet as ft

def show_payments(dash, *args):
    if not dash: return
    dash.content_column.controls.clear()
    
    # 1. Balance Overview (Cards)
    balance_cards = ft.Row(
        spacing=20,
        controls=[
            dash.create_stat_card("Total Outstanding", "$1,250.00", ft.Icons.MONEY_OFF_ROUNDED, highlight=True),
            dash.create_stat_card("Last Paid", "$1,200.00 (Sep 05)", ft.Icons.CHECK_CIRCLE_ROUNDED),
            dash.create_stat_card("Next Paid", "$1,200.00 (Oct 05)", ft.Icons.CHECK_CIRCLE_ROUNDED),
        ]
    )
    
    # 2. Transaction History
    transactions = [
        ("2025-10-01", "Monthly Rent - October", "$1,200.00", "Pending"),
        ("2025-09-05", "Monthly Rent - September", "$1,200.00", "Paid"),
        ("2025-08-28", "Water Bill - August", "$50.00", "Paid"),
    ]
    rows = []
    for date, desc, amt, status in transactions:
        status_color = ft.Colors.ORANGE_700 if status == "Pending" else ft.Colors.GREEN_700
        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(date, color=TEXT_DARK, weight=ft.FontWeight.W_500)),
                    ft.DataCell(ft.Text(desc, color=TEXT_DARK, weight=ft.FontWeight.W_500)),
                    ft.DataCell(ft.Text(amt, weight=ft.FontWeight.BOLD, color=TEXT_DARK)),
                    ft.DataCell(
                    ft.Text(status, color=status_color, weight=ft.FontWeight.BOLD)
                    ),
                ]
            )
        )
    
    history_table = ft.Container(
        bgcolor=CARD_BG,
        padding=25,
        border_radius=12,
        expand=True,
        content=ft.Column([
            ft.Text("Transaction History", size=18, weight="bold", color=TEXT_DARK),
            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Date", weight="bold", color=TEXT_DARK)),
                    ft.DataColumn(ft.Text("Description", weight="bold", color=TEXT_DARK)),
                    ft.DataColumn(ft.Text("Amount", weight="bold", color=TEXT_DARK)),
                    ft.DataColumn(ft.Text("Status", weight="bold", color=TEXT_DARK)),
                ],
                rows=rows,
            )
        ], scroll=ft.ScrollMode.AUTO)
    )

    # 3. Pay Action
    action_card = ft.Container(
        bgcolor=CARD_BG,
        padding=20,
        border_radius=12,
        width=300,
        content=ft.Column([
            ft.Text("Current Invoice", size=16, weight="bold",color=TEXT_DARK),
            ft.Text("$1,250.00", size=28, weight="bold", color=TEXT_DARK),
            ft.Divider(),
            ft.Button(
                "Make a Payment",
                icon=ft.Icons.PAYMENT_ROUNDED,
                bgcolor=ACCENT_BLUE,
                color="white",
                height=50,
                on_click=lambda _: open_payment_modal(dash)
            ),
            ft.Text("* Secured by Paragon Pay", size=10, color=TEXT_MUTED, italic=True)
        ], horizontal_alignment="center")
    )
    
    main_content = ft.Row(
        [history_table, action_card],
        alignment="start",
        vertical_alignment="start",
        spacing=20
    )
    dash.content_column.controls = [balance_cards,main_content]

def open_payment_modal(dash):
    ref_amount = ft.TextField(
        label="Enter Amount",
        prefix=ft.Text("$ "),
        value="",
        keyboard_type=ft.KeyboardType.NUMBER,
        border_color=ACCENT_BLUE,
        label_style=ft.TextStyle(weight="bold")
    )
    
    ref_method = ft.Dropdown(
        label="Select Payment Method",
        value="Visa / Mastercard",
        options=[
            ft.dropdown.Option("Visa / Mastercard"),
            ft.dropdown.Option("PayPal"),
            ft.dropdown.Option("Google Pay"),
            ft.dropdown.Option("Apple Pay"),
        ],
        border_color=ACCENT_BLUE,
        label_style=ft.TextStyle(weight="bold")
    )
    def handle_confirm_payment(e):
        if not ref_amount.value or float(ref_amount.value) <= 0:
            dash.show_message("Please enter a valid amount!")
            return
        print(f"DB Action: Processing {ref_amount.value} via {ref_method.value}")
        
        dash.show_message(f"Success! Paid ${ref_amount.value} via {ref_method.value}")
        dash.close_dialog()
        show_payments(dash)

    payment_content = ft.Column([
        ft.Text("Verify payment details before confirming.", size=12, color=TEXT_MUTED),
        ref_amount,
        ref_method,
    ], spacing=15, tight=True, width=400)

    actions = [
        ft.TextButton("Cancel", on_click=dash.close_dialog),
        ft.Button(
            content=ft.Text("CONFIRM PAYMENT", color="white", weight="bold"),
            bgcolor=ACCENT_BLUE,
            on_click=handle_confirm_payment
        ),
    ]

    dash.show_custom_modal("Secure Payment", payment_content, actions)
