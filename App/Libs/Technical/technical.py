import flet as ft
from Libs.Public.ui import configure_main_window, go_to_login
from Libs.Public.utils import create_drag_area, create_drawer

def handle_change(e, page: ft.Page):
    from Libs.Public.menu import menu_page
    from Libs.Scripts.scripts import scripts_page
    from Libs.Dashboard.dashboard import dashboard_page
    from Libs.Wiki.wiki import wiki_page
    from Libs.Movdesk.movdesk import movdesk_page
    from Config.settings import settings_page
    selected_index = e.control.selected_index

    page.clean()

    page_map = {
        0: menu_page,
        1: scripts_page,
        2: dashboard_page,
        3: wiki_page,
        4: technical_page,
        5: movdesk_page,
        6: settings_page
    }

    if selected_index in page_map:
        page_map[selected_index](page)
    elif selected_index == 7:
        go_to_login(page)

    page.close(e.control)

def technical_page(page: ft.Page):
    configure_main_window(page)
    page.title = "Menu Técnico"
    page.window.title_bar_hidden = True
    page.window.maximizable = False
    page.window.resizable = False
    page.theme_mode = 'Dark'

    drawer = create_drawer(page)
    drawer.selected_index = 4

    drawer.on_change = lambda e: handle_change(e, page)

    drag_area = create_drag_area(page, drawer)

    development_message = ft.Text(
        "Em Desenvolvimento", 
        size=30,  # Tamanho da fonte
        weight=ft.FontWeight.BOLD,  # Texto em negrito
        color=ft.colors.WHITE,  # Cor branca
        text_align=ft.TextAlign.CENTER,  # Alinhamento central
    )

    main_container = ft.Container(
        content=ft.Column(
            controls=[drag_area,
            development_message],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=ft.padding.all(0),
        margin=ft.Margin(left=0, right=0, top=0, bottom=0),
        
    )

    page.add(main_container)
    page.update()