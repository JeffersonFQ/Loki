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

    # Tamanhos padrão para ícones e texto
    icon_size = 80  # Tamanho do ícone
    text_size = 16  # Tamanho do texto
    spacing = 8     # Espaçamento entre ícone e texto

    icons_with_labels = [
        (ft.icons.DESCRIPTION, "Complexidade de Senha", lambda e: secpol_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Gerenciamento do Computador", lambda e: compmgmt_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Contas de Usuário", lambda e: userpasswords_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Politica Grupo Local", lambda e: gpedit_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Inicializar", lambda e: startup_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Propriedades de Internet", lambda e: inetcpl_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Propriedades do Sistema", lambda e: sysdm_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Editor de Registro", lambda e: regedit_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Configuração do Sistema", lambda e: msconfig_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Visualizador de Eventos", lambda e: eventvwr_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Painel de Programas", lambda e: appwiz_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Windows Firewall", lambda e: firewall_conf(page), '#CC8105'),
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

def secpol_conf(page):
    try:
        os.system("secpol.msc")
    except Exception:
        show_snackbar(page, "Erro ao abrir Política de Segurança Local.", "#D9534F")

def compmgmt_conf(page):
    try:
        os.system("compmgmt.msc")
    except Exception:
        show_snackbar(page, "Erro ao abrir Gerenciamento do Computador.", "#D9534F")

def userpasswords_conf(page):
    try:
        os.system("control userpasswords2")
    except Exception:
        show_snackbar(page, "Erro ao abrir Contas de Usuário.", "#D9534F")

def gpedit_conf(page):
    try:
        os.system("gpedit.msc")
    except Exception:
        show_snackbar(page, "Erro ao abrir Política de Grupo Local.", "#D9534F")

def startup_conf(page):
    try:
        startup_path = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
        os.startfile(startup_path)
    except Exception:
        show_snackbar(page, "Erro ao abrir Inicializar.", "#D9534F")

def inetcpl_conf(page):
    try:
        os.system("inetcpl.cpl")
    except Exception:
        show_snackbar(page, "Erro ao abrir Propriedades de Internet.", "#D9534F")

def sysdm_conf(page):
    try:
        os.system("sysdm.cpl")
    except Exception:
        show_snackbar(page, "Erro ao abrir Propriedades do Sistema.", "#D9534F")

def regedit_conf(page):
    try:
        os.system("regedit")
    except Exception:
        show_snackbar(page, "Erro ao abrir Editor de Registro.", "#D9534F")

def msconfig_conf(page):
    try:
        os.system("msconfig")
    except Exception:
        show_snackbar(page, "Erro ao abrir Configuração do Sistema.", "#D9534F")

def eventvwr_conf(page):
    try:
        os.system("eventvwr")
    except Exception:
        show_snackbar(page, "Erro ao abrir Visualizador de Eventos.", "#D9534F")

def appwiz_conf(page):
    try:
        os.system("appwiz.cpl")
    except Exception:
        show_snackbar(page, "Erro ao abrir Painel de Programas.", "#D9534F")

def firewall_conf(page):
    try:
        os.system("firewall.cpl")
    except Exception:
        show_snackbar(page, "Erro ao abrir Windows Firewall.", "#D9534F")


def go_to_technical_page(page):
    from Libs.Technical.technical import technical_page
    page.clean()
    technical_page(page)
    page.update()
