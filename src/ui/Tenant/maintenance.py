import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime
from base_dashboard import ACCENT_BLUE, ACCENT_BLUE_LIGHT, CARD_BG, TEXT_DARK, TEXT_MUTED, BaseDashboard
from flet_charts import PieChart, PieChartSection
from db import get_db_connection

import flet as ft


def fetch_maintenance_requests():
    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT request_id, description, status, reported_at, resolved_at
            FROM maintenance_requests
            ORDER BY request_id DESC
        """)

        records = cursor.fetchall()
        formatted_records = []

        for row in records:
            formatted_records.append([
                row["request_id"],
                "General",
                row["description"],
                "Medium",
                row["status"],
                str(row["reported_at"]).split(" ")[0] if row["reported_at"] else "-",
                str(row["resolved_at"]).split(" ")[0] if row["resolved_at"] else "-"
            ])

        return formatted_records

    except Exception as e:
        print("Error fetching maintenance requests:", e)
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def show_maintenance(dash, *args):
    if not dash:
        return

    dash.content_column.controls.clear()

    if hasattr(dash, "backend"):
        maintenance_records = dash.backend.get_maintenance_requests()
    else:
        maintenance_records = fetch_maintenance_requests()

    maintenance_records = sorted(maintenance_records, key=lambda x: x.get("created_date") if isinstance(x, dict) else x[5], reverse=True)

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
    for m in maintenance_records:
        if isinstance(m, dict):
            m_id = m.get("id")
            category = m.get("category", "General")
            desc = m.get("description", "")
            priority = m.get("priority", "Medium")
            status = m.get("status", "Pending")
            reported = m.get("created_date", "-")
            completed = m.get("completed_date", "-") or "-"
        else:
            m_id, category, desc, priority, status, reported, completed = m

        p_color = ft.Colors.RED_700 if priority == "High" else ft.Colors.ORANGE_700 if priority == "Medium" else ft.Colors.BLUE_GREY_400
        s_color = ft.Colors.BLUE_700 if status == "In Progress" else ft.Colors.GREEN_700 if status == "Completed" else ft.Colors.GREY_600

        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(f"#{m_id}", weight="w500", color=TEXT_DARK)),
                    ft.DataCell(ft.Text(category, weight="w500", color=TEXT_DARK)),
                    ft.DataCell(ft.Container(content=ft.Text(desc, weight="w500", color=TEXT_DARK, overflow=ft.TextOverflow.ELLIPSIS), width=200)),
                    ft.DataCell(ft.Text(priority, color=p_color, weight="bold")),
                    ft.DataCell(ft.Container(content=ft.Text(status, color="white", size=10, weight="bold"), bgcolor=s_color, padding=ft.padding.symmetric(vertical=4, horizontal=10), border_radius=15)),
                    ft.DataCell(ft.Text(reported, weight="w500", color=TEXT_DARK)),
                    ft.DataCell(ft.Text(completed, weight="w500", color=TEXT_DARK)),
                ]
            )
        )

    table_container = ft.Container(
        bgcolor=CARD_BG, padding=20, border_radius=12, expand=True,
        content=ft.Column([
            ft.DataTable(
                expand=True,
                column_spacing=45,
                heading_row_color=ft.Colors.BLUE_GREY_50,
                columns=[
                    ft.DataColumn(ft.Text("ID", weight="bold", color=ft.Colors.BLUE_900)),
                    ft.DataColumn(ft.Text("Category", weight="bold", color=ft.Colors.BLUE_900)),
                    ft.DataColumn(ft.Text("Description", weight="bold", color=ft.Colors.BLUE_900)),
                    ft.DataColumn(ft.Text("Priority", weight="bold", color=ft.Colors.BLUE_900)),
                    ft.DataColumn(ft.Text("Status", weight="bold", color=ft.Colors.BLUE_900)),
                    ft.DataColumn(ft.Text("Reported", weight="bold", color=ft.Colors.BLUE_900)),
                    ft.DataColumn(ft.Text("Completed", weight="bold", color=ft.Colors.BLUE_900)),
                ],
                rows=rows,
            )
        ], scroll=ft.ScrollMode.AUTO)
    )

    pie_chart = PieChart(
        sections=[
            PieChartSection(30, title="30%", color=ft.Colors.BLUE_700, radius=40, title_style=ft.TextStyle(size=12, weight="bold", color="white")),
            PieChartSection(50, title="50%", color=ft.Colors.GREEN_700, radius=40, title_style=ft.TextStyle(size=12, weight="bold", color="white")),
            PieChartSection(20, title="20%", color=ft.Colors.GREY_600, radius=40, title_style=ft.TextStyle(size=12, weight="bold", color="white")),
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

    sent_card = ft.Container(
        bgcolor=CARD_BG, padding=20, border_radius=12, width=320,
        content=ft.Column([
            ft.Text("Recent History", size=18, weight="bold", color=TEXT_DARK),
            ft.Divider(),
            ft.ListView(
                spacing=10,
                height=300,
                controls=[
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.BUILD_CIRCLE_ROUNDED, color=ACCENT_BLUE),
                        title=ft.Text(f"Request #{m.get('id') if isinstance(m, dict) else m[0]}", weight="bold", color=TEXT_DARK),
                        subtitle=ft.Text(f"{m.get('category') if isinstance(m, dict) else m[1]} - {m.get('created_date') if isinstance(m, dict) else m[5]}"),
                    )
                    for m in maintenance_records[:5]
                ]
            )
        ])
    )

    dash.content_column.controls = [
        action_bar,
        ft.Row([table_container]),
        ft.Row([chart_card, sent_card], spacing=20, vertical_alignment="start")
    ]
    dash.page.update()


def open_maintenance_form(dash):
    current_date = datetime.now().strftime("%Y-%m-%d")

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

        try:
            if hasattr(dash, "backend"):
                success, msg = dash.backend.create_maintenance_request(ref_category.value, ref_desc.value, ref_priority.value)
                if not success:
                    raise Exception(msg)
            else:
                raise Exception("No backend available for creating maintenance request")

            dash.show_message("Success! Request submitted successfully!")
            dash.close_dialog()
            show_maintenance(dash)

        except Exception as ex:
            dash.show_message(f"Submit error: {str(ex)}")

    form_content = ft.Column([
        ft.Text("Please fill out the details below", color=TEXT_MUTED),
        ref_category,
        ref_priority,
        ref_desc,
        ft.Row([
            ft.Icon(ft.Icons.CALENDAR_MONTH, size=16, color=TEXT_MUTED),
            ft.Text(f"Reported Date: {current_date}", size=12, color=TEXT_MUTED, weight="bold"),
        ]),
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