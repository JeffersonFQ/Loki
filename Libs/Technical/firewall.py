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

def firewall_page(page: ft.Page):
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
        (ft.icons.DESCRIPTION, "Abrir porta SQL (1433)", lambda e: sql_port_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Abrir porta Tomcat (7071)", lambda e: tomcat_port_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Desativar compartilhameto por senha", lambda e: off_passw_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Tornar rede atual Privada", lambda e: rede_priv_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Ativar Firewall", lambda e: firewall_on_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Desativar Firewall", lambda e: firewall_off_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Alterar Hostname", lambda e: edit_host_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Verificar Hostname", lambda e: ver_host_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Verificar IP Externo", lambda e: ver_ipexterno_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Verificar IP Interno", lambda e: ver_ipinterno_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Compartilhar pastas SN", lambda e: comp_sn_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Verificar Pastas Compartilhadas", lambda e: ver_comp_sn_conf(page), '#CC8105'),
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

def sql_port_conf(page):
    print("Porta SQL")

def tomcat_port_conf(page):
    print("Porta Tomcat")

def off_passw_conf(page):
    print("Desativar compartilhamento por senha")

def rede_priv_conf(page):
    print("Tornar rede privada")

def firewall_on_conf(page):
    print("Firewall ativado")

def firewall_off_conf(page):
    print("Firewall desativado")

def edit_host_conf(page):
    print("Editar Hostname")

def ver_ipinterno_conf(page):
    print("Verificar IP Interno")

def ver_ipexterno_conf(page):
    print("Verificar IP Externo")

def comp_sn_conf(page):
    print("Compartilhar pastas SN")

def ver_comp_sn_conf(page):
    print("Verificar pastas compartilhadas")

def ver_host_conf(page):
    print("Verificar Hostname")

def go_to_technical_page(page):
    from Libs.Technical.technical import technical_page
    page.clean()
    technical_page(page)
    page.update()
