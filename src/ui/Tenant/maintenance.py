import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Đoạn code trên đang thêm thư mục cha của file hiện tại vào sys.path để có thể import các module từ thư mục đó để chạy test. Điều này giúp tránh lỗi ImportError khi import các module khác trong dự án. Sau này sẽ sửa lại, dùng .. để import trực tiếp thay vì sửa sys.path như này.

from base_dashboard import ACCENT_BLUE, ACCENT_BLUE_LIGHT, CARD_BG, TEXT_DARK, TEXT_MUTED, BaseDashboard
from flet_charts import PieChart, PieChartSection
import flet as ft

def show_maintenance(dash, *args):
    if not dash: return
    dash.content_column.controls.clear()
    # 1. Mock Data
    maintenance_data = [
        (101, "Plumbing", "Kitchen sink leaking", "High", "In Progress", "2026-02-15", 45.0, 1.5),
        (102, "Electrical", "AC Filter Cleaning", "Low", "Completed", "2026-01-22", 20.0, 0.5),
        (103, "Furniture", "Broken door handle", "Medium", "Pending", "TBD", 0.0, 0.0),
    ]
    action_bar = ft.Container(
        padding=ft.padding.symmetric(vertical=10),
        content=ft.Row([
            ft.Text("Maintenance Records", size=18, weight="bold", color=TEXT_DARK),
            ft.Button(
                content=ft.Row([
                    ft.Icon(ft.Icons.ADD_ROUNDED, color="white", size=20),
                    ft.Text("NEW REQUEST", weight="bold", color="white"),
                ], tight=True),
                bgcolor=ACCENT_BLUE,
                on_click=lambda _: open_maintenance_form(dash)
            )
        ], alignment="spaceBetween")
    )
    rows = []
    for m in maintenance_data:
        p_color = ft.Colors.RED_700 if m[3] == "High" else ft.Colors.ORANGE_700 if m[3] == "Medium" else ft.Colors.BLUE_GREY_400
        s_color = ft.Colors.BLUE_700 if m[4] == "In Progress" else ft.Colors.GREEN_700 if m[4] == "Completed" else ft.Colors.GREY_600

        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(f"#{m[0]}",weight=ft.FontWeight.W_500, color=TEXT_DARK)),
                    ft.DataCell(ft.Text(m[1],weight=ft.FontWeight.W_500,color=TEXT_DARK)),
                    ft.DataCell(ft.Container(content=ft.Text(m[2],weight=ft.FontWeight.W_500,color=TEXT_DARK, overflow=ft.TextOverflow.ELLIPSIS), width=200)),
                    ft.DataCell(ft.Text(m[3], color=p_color, weight="Bold")),
                    ft.DataCell(ft.Container(content=ft.Text(m[4], color="white", size=10, weight="Bold"), bgcolor=s_color, padding=ft.padding.symmetric(vertical=4, horizontal=10), border_radius=15)),
                    ft.DataCell(ft.Text(m[5], weight=ft.FontWeight.W_500, color=TEXT_DARK)),
                    ft.DataCell(ft.Text(f"${m[6]:.2f}", weight=ft.FontWeight.W_500, color=TEXT_DARK)),
                    ft.DataCell(ft.Text(f"{m[7]}h", weight=ft.FontWeight.W_500, color=TEXT_DARK)),
                ]
            )
        )

    # 2. Records
    table_container = ft.Container(
        bgcolor=CARD_BG, padding=20, border_radius=12, expand=True,
        content=ft.Column([
            ft.DataTable(
                column_spacing=35,
                heading_row_color=ft.Colors.BLUE_GREY_50,
                columns=[
                    ft.DataColumn(ft.Text("ID", weight="bold", color=TEXT_DARK)),
                    ft.DataColumn(ft.Text("Category", weight="bold", color=TEXT_DARK)),
                    ft.DataColumn(ft.Text("Description", weight="bold", color=TEXT_DARK)),
                    ft.DataColumn(ft.Text("Priority", weight="bold", color=TEXT_DARK)),
                    ft.DataColumn(ft.Text("Status", weight="bold", color=TEXT_DARK)),
                    ft.DataColumn(ft.Text("Scheduled", weight="bold", color=TEXT_DARK)),
                    ft.DataColumn(ft.Text("Cost", weight="bold", color=TEXT_DARK)),
                    ft.DataColumn(ft.Text("Time", weight="bold", color=TEXT_DARK)),
                ],
                rows=rows,
            )
        ], scroll=ft.ScrollMode.ALWAYS)
    )
    
    # 3a. DTA CHART (Mock Data) - Replace with actual chart component later
    pie_chart = PieChart(
        sections=[
            PieChartSection(30, title="30%", color=ft.Colors.BLUE_700, radius=40,title_style=ft.TextStyle(size=12, weight="bold", color="white")),
            PieChartSection(50, title="50%", color=ft.Colors.GREEN_700, radius=40,title_style=ft.TextStyle(size=12, weight="bold", color="white")),
            PieChartSection(20, title="20%", color=ft.Colors.GREY_600, radius=40,title_style=ft.TextStyle(size=12, weight="bold", color="white")),
        ],
        sections_space=2,
        center_space_radius=40,
        expand=True,
    )

    chart_card = ft.Container(
        bgcolor=CARD_BG,
        padding=20,
        border_radius=12,
        expand=True,
        content=ft.Column([
            ft.Text("Status Overview", size=18, weight="bold", color=TEXT_DARK),
            ft.Container(content=pie_chart, height=200),
            ft.Column([
                ft.Row([ft.Container(width=12, height=12, bgcolor=ft.Colors.BLUE_700, border_radius=3), ft.Text("In Progress", weight="bold", size=12, color=ft.Colors.BLUE_700)]),
                ft.Row([ft.Container(width=12, height=12, bgcolor=ft.Colors.GREEN_700, border_radius=3), ft.Text("Completed", weight="bold", size=12, color=ft.Colors.GREEN_700)]),
                ft.Row([ft.Container(width=12, height=12, bgcolor=ft.Colors.GREY_600, border_radius=3), ft.Text("Pending", weight="bold", size=12, color=ft.Colors.GREY_600)]),
            ], spacing=10)
        ])
    )
    # 3b. Lists

    sent_card = ft.Container(
        bgcolor=CARD_BG, padding=20, border_radius=12, width=320,
        content=ft.Column([
            ft.Text("Recent History", size=18, weight="bold", color=TEXT_DARK),
            ft.Divider(),
            ft.ListView(
                spacing=10,
                controls=[
                    ft.ListTile(title=ft.Text(f"Request #{m[0]}", weight="bold", color=TEXT_DARK), subtitle=ft.Text(f"{m[1]} - {m[5]}"))
                    for m in maintenance_data
                ]
            )
        ])
    )

    # 4. MAIN LAYOUT
    dash.content_column.controls = [
        action_bar,
        ft.Row([table_container]),
        ft.Row([chart_card, sent_card], spacing=20)
    ]
    dash.page.update()
        
def open_maintenance_form(dash):
    """Popup form for adding new request"""
    ref_category = ft.Dropdown(
        label="Category", value="Plumbing",
        options=[ft.dropdown.Option(x) for x in ["Plumbing", "Electrical", "Furniture", "Others"]],
        border_color=ACCENT_BLUE
    )

    ref_priority = ft.Dropdown(
        label="Priority Level", value="Medium",
        options=[ft.dropdown.Option(x) for x in ["Low", "Medium", "High"]],
        border_color=ACCENT_BLUE
    )
    ref_desc = ft.TextField(
        label="Issue Description", hint_text="Tell us what needs fixing...", multiline=True, min_lines=3, border_color=ACCENT_BLUE
    )

    def handle_submit(e):
        if not ref_desc.value:
            dash.show_message("Please provide a description of the issue!")
            return

        # Thực hiện lưu vào database
        try:
            # db.save_maintenance(ref_category.value, ref_priority.value, ref_desc.value)
            print(f"Submitting: {ref_category.value} | Priority: {ref_priority.value}")
            
            dash.show_message("Success! Request submitted successfully!")
            
            if hasattr(dash, "active_dialog"):
                dash.active_dialog.open = False
            elif dash.page.dialog:
                dash.page.dialog.open = False

            show_maintenance(dash)
            dash.page.update()
            
        except Exception as ex:
            dash.show_message(f"Submit error: {str(ex)}")

    form_content = ft.Column([
        ft.Divider(height=10, color="transparent"),
        ref_category,
        ref_priority,
        ref_desc,
        ft.Text("* Costs and dates will be updated by Admin.", size=14, color=TEXT_MUTED, italic=True),
        ft.Text(f"Reported Date: 2026-02-18", size=12, color=TEXT_MUTED),
    ], spacing=20, width=450)
    
    actions = [
        ft.Button(
            ft.TextButton("Cancel", on_click=dash.close_dialog),
        ),
        ft.Button(
            content=ft.Text("SUBMIT REQUEST", color="white", weight="bold"),
            bgcolor=ACCENT_BLUE,
            on_click=handle_submit
        ),
    ]
    dash.show_custom_modal("New Maintenance Request", form_content, actions)
