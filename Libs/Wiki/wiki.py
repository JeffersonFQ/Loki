import flet as ft
import webbrowser  # Para abrir URLs no navegador
from Libs.Public.ui import configure_main_window, go_to_login
from Libs.Public.utils import create_drag_area, create_drawer

def handle_change(e, page: ft.Page):
    from Libs.Public.menu import menu_page
    from Libs.Scripts.scripts import scripts_page
    from Libs.Dashboard.dashboard import dashboard_page
    from Libs.Technical.technical import technical_page
    from Libs.Movdesk.movdesk import movdesk_page
    from Config.settings import settings_page
    selected_index = e.control.selected_index

    page.clean()

    page_map = {
        0: menu_page,
        1: scripts_page,
        2: wiki_page,
        3: technical_page,
        4: dashboard_page,
        5: movdesk_page,
        6: settings_page
    }

    if selected_index in page_map:
        page_map[selected_index](page)
    elif selected_index == 7:
        go_to_login(page)

    page.close(e.control)

def abrir_webpage(url):
    webbrowser.open(url)

def wiki_page(page: ft.Page):
    configure_main_window(page)
    page.title = "Menu Wiki"
    page.window.title_bar_hidden = True
    page.window.maximizable = False
    page.window.resizable = False
    page.theme_mode = 'Dark'

    drawer = create_drawer(page)
    drawer.selected_index = 3

    drawer.on_change = lambda e: handle_change(e, page)

    drag_area = create_drag_area(page, drawer)

    # Adicionando os botões em duas linhas e duas colunas com tamanhos padronizados e ajuste no tamanho da letra
    botoes_container = ft.Column(
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.ElevatedButton("Tela Principal", 
                                      on_click=lambda _: abrir_webpage("https://google.com"),
                                      style=ft.ButtonStyle(
                                          bgcolor="#CC8105",
                                          color="#081c15",
                                          shape=ft.RoundedRectangleBorder(radius=8),
                                          padding=ft.padding.symmetric(horizontal=20, vertical=10),
                                          text_style=ft.TextStyle(size=40)  # Alterando o tamanho da letra
                                      ),
                                      width=500,
                                      height=300),
                    ft.ElevatedButton("Buscar Conteúdo", 
                                      on_click=lambda _: abrir_webpage("https://google.com"),
                                      style=ft.ButtonStyle(
                                          bgcolor="#CC8105",
                                          color="#081c15",
                                          shape=ft.RoundedRectangleBorder(radius=8),
                                          padding=ft.padding.symmetric(horizontal=20, vertical=10),
                                          text_style=ft.TextStyle(size=40)  # Alterando o tamanho da letra
                                      ),
                                      width=500,
                                      height=300)
                ]
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.ElevatedButton("Novo Conteúdo", 
                                      on_click=lambda _: abrir_webpage("https://google.com"),
                                      style=ft.ButtonStyle(
                                          bgcolor="#CC8105",
                                          color="#081c15",
                                          shape=ft.RoundedRectangleBorder(radius=8),
                                          padding=ft.padding.symmetric(horizontal=20, vertical=10),
                                          text_style=ft.TextStyle(size=40)  # Alterando o tamanho da letra
                                      ),
                                      width=500,
                                      height=300),
                    ft.ElevatedButton("Editar Conteúdo", 
                                      on_click=lambda _: abrir_webpage("https://google.com"),
                                      style=ft.ButtonStyle(
                                          bgcolor="#CC8105",
                                          color="#081c15",
                                          shape=ft.RoundedRectangleBorder(radius=8),
                                          padding=ft.padding.symmetric(horizontal=20, vertical=10),
                                          text_style=ft.TextStyle(size=40)  # Alterando o tamanho da letra
                                      ),
                                      width=500,
                                      height=300)
                ]
            )
        ]
    )

    main_container = ft.Container(
        content=ft.Column(
            controls=[drag_area, botoes_container],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=ft.padding.all(0),
        margin=ft.Margin(left=0, right=0, top=0, bottom=0),
    )

    page.add(main_container)
    page.update()
