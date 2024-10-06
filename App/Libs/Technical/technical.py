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

    # Funções para os ícones
    def on_add_clicked(e):
        print("Adicionar clicado!")

    def on_remove_clicked(e):
        print("Remover clicado!")

    def on_edit_clicked(e):
        print("Editar clicado!")

    def on_settings_clicked(e):
        print("Configurações clicadas!")

    def on_list_clicked(e):
        print("Lista clicada!")

    def on_info_clicked(e):
        print("Informação clicada!")

    # Lista de ícones e rótulos com cores
    icon_size = 200  # Tamanho do ícone
    icons_with_labels = [
        (ft.icons.WINDOW, "Windows Tools", on_add_clicked, ft.colors.RED),
        (ft.icons.BUILD_CIRCLE_OUTLINED, "Ferramentas", on_remove_clicked, ft.colors.GREEN),
        (ft.icons.WALLET_TRAVEL_ROUNDED, "SN Tools", on_edit_clicked, ft.colors.BLUE),
        (ft.icons.WIFI, "Rede e Firewall", on_settings_clicked, ft.colors.ORANGE),
        (ft.icons.ANALYTICS_OUTLINED, "Verificações", on_list_clicked, ft.colors.PURPLE),
        (ft.icons.INSTALL_DESKTOP, "Instalações", on_info_clicked, ft.colors.YELLOW),
    ]

    # Criar linhas de ícones com textos
    rows = []
    for i in range(0, len(icons_with_labels), 3):
        columns = []
        for icon, label, on_click, color in icons_with_labels[i:i+3]:
            column = ft.Column(
                controls=[
                    ft.IconButton(
                        icon, 
                        tooltip=label, 
                        on_click=on_click, 
                        icon_size=icon_size,
                        style=ft.ButtonStyle(
                            icon_color='#CC8105'
                        )
                    ),
                    ft.Text(label, text_align=ft.TextAlign.CENTER, size=18)
                ],
                spacing=0,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
            columns.append(column)

        row = ft.Row(
            spacing=40,
            controls=columns,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        rows.append(row)

    # Container para os ícones
    icons_container = ft.Column(
        spacing=80,
        controls=rows,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    main_container = ft.Container(
        content=ft.Column(
            controls=[
                drag_area, 
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
