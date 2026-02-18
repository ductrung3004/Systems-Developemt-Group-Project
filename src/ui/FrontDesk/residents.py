import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Đoạn code trên đang thêm thư mục cha của file hiện tại vào sys.path để có thể import các module từ thư mục đó để chạy test. Điều này giúp tránh lỗi ImportError khi import các module khác trong dự án. Sau này sẽ sửa lại, dùng .. để import trực tiếp thay vì sửa sys.path như này.

import flet as ft
from base_dashboard import *

# Mock Database for Residents
test_residents_data = [
    ["A-101", "Nguyen Van A", "Owner", "0901234567"],
    ["B-302", "Johnathan Doe", "Tenant", "0987654321"],
    ["A-505", "Tran Thi B", "Owner", "0911223344"],
    ["C-204", "Le Van C", "Tenant", "0922334455"],
]

def show_residents(dash, *args):
    if not dash: return
    dash.content_column.controls.clear()

    # --- 1. HEADER SECTION ---
    header = ft.Container(
        padding=ft.padding.symmetric(vertical=10),
        content=ft.Row([
            ft.Row([
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.APARTMENT_ROUNDED, size=18, color=ACCENT_BLUE),
                        ft.Text("Quick Stats", weight="bold", size=13,color=TEXT_DARK),], tight=True),
                    bgcolor=ft.Colors.with_opacity(0.1, ACCENT_BLUE),
                    padding=ft.padding.symmetric(horizontal=12, vertical=8),
                    border_radius=20,
                ),
                ft.Row([
                    ft.Text("Occupied:", size=13, weight="w500", color=TEXT_MUTED),
                    ft.Text("185", size=13, weight="bold", color=ACCENT_BLUE),
                    ft.VerticalDivider(width=10, color="transparent"),
                    ft.Text("Vacant:", size=13, weight="w500", color=TEXT_MUTED),
                    ft.Text("15", size=13, weight="bold", color=ft.Colors.ORANGE_700),
                ], spacing=5)
            ], spacing=15),

            ft.Button(
                content=ft.Row([
                    ft.Icon(ft.Icons.PERSON_ADD_ROUNDED, color="white", size=20),
                    ft.Text("Add New Resident", weight="bold", color="white"),
                ], tight=True),
                bgcolor=ACCENT_BLUE,
                on_click=lambda _: draw_resident_registration(dash)
            )
        ], alignment="spaceBetween")
    )

    # --- 2. SEARCH & FILTER SECTION ---
    search_box = ft.TextField(
        label="Search by Room, Name or Phone...",
        prefix_icon=ft.Icons.SEARCH,
        expand=True,
        border_radius=10,
        bgcolor="white",
        on_submit=lambda e: dash.show_message(f"Searching for: {e.control.value}")
    )

    filter_row = ft.Row([
        search_box,
        ft.Dropdown(
            width=200,
            label="Block",
            options=[ft.dropdown.Option("All Blocks"), ft.dropdown.Option("Block A"), ft.dropdown.Option("Block B")],
            border_radius=10,
        ),
    ])

    # --- 3. RESIDENT TABLE ---
    rows = []
    for room, name, res_type, contact in test_residents_data:
        rows.append(_create_resident_row(dash, room, name, res_type, contact))
        
    resident_list_container = ft.Container(
        bgcolor=CARD_BG,
        padding=20,
        border_radius=12,
        expand=True,
        content=ft.Column([
            ft.DataTable(
                expand=True,
                columns=[
                    ft.DataColumn(ft.Text("Room", weight="bold", color=TEXT_DARK)),
                    ft.DataColumn(ft.Text("Full Name", weight="bold", color=TEXT_DARK)),
                    ft.DataColumn(ft.Text("Type", weight="bold", color=TEXT_DARK)),
                    ft.DataColumn(ft.Text("Contact", weight="bold", color=TEXT_DARK)),
                    ft.DataColumn(ft.Text("Actions", weight="bold", color=TEXT_DARK)),
                ],
                rows=rows,
            )
        ], scroll=ft.ScrollMode.AUTO)
    )
    dash.content_column.controls.extend([header, filter_row, resident_list_container])
    dash.page.update()

def draw_resident_registration(dash, *args):
    dash.content_column.controls.clear()

    ref_block = ft.TextField(label="Block", expand=True, border_radius=8, color=TEXT_DARK, hint_text="e.g. A")
    ref_room = ft.TextField(label="Room Number", expand=True, border_radius=8, color=TEXT_DARK)
    ref_name = ft.TextField(label="Full Name", expand=True, border_radius=8, color=TEXT_DARK)
    ref_email = ft.TextField(label="Email Address", expand=True, border_radius=8, color=TEXT_DARK)
    ref_phone = ft.TextField(label="Phone Number", expand=True, border_radius=8, color=TEXT_DARK)
    ref_dob = ft.TextField(label="Date of Birth", expand=True, border_radius=8, hint_text="DD/MM/YYYY", color=TEXT_DARK)
    ref_id = ft.TextField(label="ID / Passport Number", expand=True, border_radius=8)
    ref_type = ft.Dropdown(
        label="Resident Type",
        expand=True,
        border_radius=8,
        options=[
            ft.dropdown.Option("Owner"),
            ft.dropdown.Option("Tenant"),
            ft.dropdown.Option("Family Member"),
        ]
    )
    
    back_btn = ft.Button(
        content=ft.Row([
            ft.Icon(ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED, color=NAVY_SECOND, size=16),
            ft.Text("Back to Directory", color=NAVY_SECOND, weight="bold"),
        ], tight=True),
        bgcolor="transparent",
        on_click=lambda _: show_residents(dash)
    )

    registration_card = ft.Container(
        bgcolor=CARD_BG,
        padding=30,
        border_radius=12,
        content=ft.Column([
            ft.Text("Register New Resident", size=20, weight="bold", color=TEXT_DARK),
            ft.Divider(height=20),
            
            # Apartment Info
            ft.Row([ref_block, ref_room], spacing=20),

            # Personal Info
            ft.Row([ref_name, ref_email], spacing=20),
            ft.Row([ref_phone, ref_dob], spacing=20),
            ft.Row([ref_type, ref_id], spacing=20),
            ft.Divider(height=20),
            
            # Action Buttons
            ft.Row([
                ft.Button(
                    content=ft.Text("Confirm Registration", color="white", weight="bold"),
                    bgcolor=ACCENT_BLUE,
                    width=200,
                    on_click=lambda _: handle_save_resident(
                        dash,
                        ref_block.value,
                        ref_room.value,
                        ref_name.value,
                        ref_phone.value,
                        ref_type.value
                    )
                ),
            ], alignment="end")
        ], spacing=15)
    )

    dash.content_column.controls.extend([back_btn, registration_card])
    dash.page.update()

def handle_save_resident(dash, block, room, name, phone, res_type):
    if not room or not name or not phone:
        dash.show_message("Error: Room, Name and Phone are required!")
        return

    try:
        global test_residents_data
        full_room = f"{block}-{room}" if block else room

        test_residents_data.insert(0, [full_room, name, res_type, phone])

        dash.show_message(f"Resident {name} registered successfully!")
        show_residents(dash)
        
    except Exception as e:
        dash.show_message(f"Registration failed: {str(e)}")

def _create_resident_row(dash, room, name, res_type, contact):
    type_color = ACCENT_BLUE if res_type == "Owner" else ft.Colors.ORANGE_700
    return ft.DataRow(
        cells=[
            ft.DataCell(ft.Text(room, color=TEXT_DARK, weight="w500")),
            ft.DataCell(ft.Text(name, color=TEXT_DARK, weight="w500")),
            ft.DataCell(
                ft.Container(
                    content=ft.Text(res_type, size=11, weight="bold", color="white"),
                    bgcolor=type_color,
                    padding=ft.padding.symmetric(horizontal=10, vertical=2),
                    border_radius=5
                )
            ),
            ft.DataCell(ft.Text(contact, color=TEXT_DARK)),
            ft.DataCell(
                ft.Row([
                    ft.IconButton(ft.Icons.EDIT_OUTLINED, icon_color=ACCENT_BLUE, icon_size=18, tooltip="Edit"),
                    ft.IconButton(ft.Icons.CONTACT_PHONE_OUTLINED, icon_color=TEXT_MUTED, icon_size=18, tooltip="Contact"),
                ], spacing=0)
            ),
        ]
    )