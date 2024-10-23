import flet as ft
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

def analytics_page(page: ft.Page):
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
        (ft.icons.DESCRIPTION, "Verificar Empresas da Base", lambda e: empresa_ver(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Verificar configurações completas", lambda e: all_config_ver(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Verificar Unimake", lambda e: unimake_ver(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Verificar porta do Tomcat", lambda e: tomcat_port_ver(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Verificar Consumo RAM", lambda e: ram_ver(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Verificar Consumo Processador", lambda e: processador_ver(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Verificar tabela Pessoa", lambda e: pessoa_ver(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Verificar tabela Produto", lambda e: produto_ver(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Verificar Status Sefaz", lambda e: sefaz_ver(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Verificar Odin", lambda e: odin_ver(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Verificar porta aberta", lambda e: port_open_ver(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Verificar Produtos B2B", lambda e: b2b_produto_ver(page), '#CC8105'),
    ]

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
                expand=True
            )
            columns.append(column)

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

def empresa_ver(page):
    print("Verificar Empresa")

def all_config_ver(page):
    print("Verificar tudo")

def unimake_ver(page):
    print("Verificar Unimake")

def tomcat_port_ver(page):
    print("Perificar Tomcat")

def ram_ver(page):
    print("Verificar Ram")

def processador_ver(page):
    print("Verificar Processador")

def pessoa_ver(page):
    print("Verificar Pessoa")

def produto_ver(page):
    print("Verificar Produto")

def sefaz_ver(page):
    print("Verificar Sefaz")

def odin_ver(page):
    print("Verificar Odin")

def port_open_ver(page):
    print("Verificar Portas abertas")

def b2b_produto_ver(page):
    print("Verificar produto B2B")

def go_to_technical_page(page):
    from Libs.Technical.technical import technical_page
    page.clean()
    technical_page(page)
    page.update()
