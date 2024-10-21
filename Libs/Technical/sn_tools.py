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

def sn_tools_page(page: ft.Page):
    configure_main_window(page)
    page.title = "Menu Windows"
    page.window.title_bar_hidden = True
    page.window.maximizable = False
    page.window.resizable = False
    page.theme_mode = 'Dark'

    drawer = create_drawer(page)
    drawer.selected_index = 4

    drag_area = create_drag_area(page, drawer)

    # Tamanhos padrão para ícones e texto
    icon_size = 80  # Tamanho do ícone
    text_size = 16  # Tamanho do texto
    spacing = 8     # Espaçamento entre ícone e texto

    icons_with_labels = [
        (ft.icons.DESCRIPTION, "Verificar APIs no servidor", lambda e: ver_api_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Conferir Versão FV", lambda e: ver_fv_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Conferir Versão B2B", lambda e: ver_b2b_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Conferir Versão Checkout", lambda e: ver_checkout_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Verificar comunicação Tomcat", lambda e: ver_tomcat_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Configurar Config", lambda e: config_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Configurar Config_compilado", lambda e: configcompilado_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Configurar Agendador", lambda e: agendador_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Abrir Tomcat e Unimake", lambda e: open_apps_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Abrir S7 pelo prompt", lambda e: open_s7_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Fechar Janelas S7", lambda e: close_s7_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Revogar 1 acesso", lambda e: kill_old_conf(page), '#CC8105'),
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

def ver_api_conf(page):
    print("Verificar APIs")

def ver_fv_conf(page):
    print("Verificar FV")

def ver_b2b_conf(page):
    print("Verificar B2B")

def ver_checkout_conf(page):
    print("Verficar Checkout")

def ver_tomcat_conf(page):
    print("Verificar Tomcat")

def config_conf(page):
    print("Configurar Config")

def configcompilado_conf(page):
    print("Configurar Compilado")

def agendador_conf(page):
    print("Configurar Agendador")

def open_apps_conf(page):
    print("Abrir Tomcat e Unimake")

def open_s7_conf(page):
    print("Abrir S7")

def close_s7_conf(page):
    print("Fechar S7")

def kill_old_conf(page):
    print("Kill em 1 usuário")

def go_to_technical_page(page):
    from Libs.Technical.technical import technical_page
    page.clean()
    technical_page(page)
    page.update()
