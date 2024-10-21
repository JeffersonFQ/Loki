import flet as ft
import os
from Libs.Public.ui import configure_main_window
from Libs.Public.utils import create_drag_area, create_drawer

def show_snackbar(page: ft.Page, message: str, color: str):
    snackbar = ft.SnackBar(
        content=ft.Text(message, color=ft.colors.WHITE),
        bgcolor=color,
        open=True
    )
    page.snack_bar = snackbar
    page.update()

def ferramentas_page(page: ft.Page):
    configure_main_window(page)
    page.title = "Menu Windows"
    page.window.title_bar_hidden = True
    page.window.maximizable = False
    page.window.resizable = False
    page.theme_mode = 'Dark'

    drawer = create_drawer(page)
    drawer.selected_index = 4

    drag_area = create_drag_area(page, drawer)

    icon_size = 80
    text_size = 16
    spacing = 8

    icons_with_labels = [
        (ft.icons.DESCRIPTION, "Gerar Backup troca Servidor", lambda e: gerar_backup(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Abrir SSMS", lambda e: open_ssms(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Dispositivos na rede", lambda e: dispositivos_rede(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Abrir pasta S7", lambda e: open_s7(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Abrir pasta WebApps", lambda e: open_webapps(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Abrir Mega - Compilados", lambda e: open_mega_compilados(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Abrir Mega - Manuais", lambda e: open_mega_manuais(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Abrir Drive - Compilados", lambda e: open_drive(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Ativar o Windows", lambda e: windows_activate(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Reiniciar Maquina", lambda e: reload_win(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Reiniciar Agendado", lambda e: temp_reload_win(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Desligar agendado", lambda e: temp_off_win(page), '#CC8105'),
    ]

    # Definir número de colunas
    num_columns = 3
    rows = []
    for i in range(0, len(icons_with_labels), num_columns):
        columns = []
        for icon, label, on_click, color in icons_with_labels[i:i + num_columns]:
            column = ft.Column(
                controls=[
                    ft.IconButton(
                        icon,
                        tooltip=label,
                        on_click=on_click,
                        icon_size=icon_size,
                        style=ft.ButtonStyle(
                            icon_color=color
                        )
                    ),
                    ft.Text(label, text_align=ft.TextAlign.CENTER, size=text_size)
                ],
                spacing=spacing,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True  # Permite que a coluna expanda para preencher o espaço
            )
            columns.append(column)

        # Alinha as colunas na mesma linha
        row = ft.Row(
            spacing=20,
            controls=columns,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        rows.append(row)

    icons_container = ft.Column(
        controls=rows,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    back_button = ft.TextButton(
        text="Voltar",
        on_click=lambda e: go_to_technical_page(page),
        style=ft.ButtonStyle(
            bgcolor="#7B0000",
            color=ft.colors.WHITE,
            padding=ft.padding.symmetric(horizontal=20, vertical=12)
        ),
    )

    main_container = ft.Container(
        content=ft.Column(
            controls=[
                drag_area,
                ft.Row(
                    controls=[back_button],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(content=icons_container, margin=ft.Margin(left=60, top=18, right=60, bottom=0))
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=ft.padding.all(0),
        margin=ft.Margin(left=0, right=0, top=0, bottom=0),
    )

    page.add(main_container)
    page.update()

def gerar_backup(page):
    print("Gerar o Backup da base")

def open_ssms(page):
    print("Abrir o SSMS")

def dispositivos_rede(page):
    print("Visualizar Dispositivos na Rede")

def open_s7(page):
    print("Abrir S7")

def open_webapps(page):
    print("Abrir WebApps")

def open_mega_compilados(page):
    print("Abrir Mega - Compilados")

def open_mega_manuais(page):
    print("Abrir Mega - Manuais")

def open_drive(page):
    print("Abrir Google Drive")

def windows_activate(page):
    print("Ativar Windos")

def reload_win(page):
    print("Reinicir maquina")

def temp_reload_win(page):
    print("Temporizador reiniciar")

def temp_off_win(page):
    print("Temporizador desligar")

def go_to_technical_page(page):
    from Libs.Technical.technical import technical_page
    page.clean()
    technical_page(page)
    page.update()
