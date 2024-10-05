import flet as ft
from Libs.Public.ui import configure_main_window, go_to_login
from Libs.Public.utils import create_drag_area, create_drawer

def handle_change(e, page: ft.Page):
    from Libs.Public.menu import menu_page
    from Libs.Dashboard.dashboard import dashboard_page
    from Libs.Wiki.wiki import wiki_page
    from Libs.Technical.technical import technical_page
    from Libs.Movdesk.movdesk import movdesk_page
    from Config.settings import settings_page
    selected_index = e.control.selected_index

    page.clean()

    page_map = {
        0: menu_page,
        1: '',
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

def redirect_to(page: ft.Page, target_page_function):
    page.clean()
    target_page_function(page)
    page.update()

def folder_redirect(page: ft.Page, target_page_function):
    redirect_to(page, target_page_function)

def tabelas_page(page: ft.Page):
    configure_main_window(page)
    
    # Definir o tema escuro para a página
    page.bgcolor = '#081c15'
    page.title = "Menu Scripts"
    page.window.title_bar_hidden = True
    page.window.maximizable = False
    page.window.resizable = False
    page.theme_mode = 'Dark'
    
    # Remover contorno da janela
    page.window.border_color = ft.colors.TRANSPARENT

    # Criação do drawer e área de drag
    drawer = create_drawer(page)
    drawer.selected_index = 1
    drawer.on_change = lambda e: handle_change(e, page)
    drag_area = create_drag_area(page, drawer)

    # Lista de pastas com funções de redirecionamento
    folders = [
        ("Tabelas", go_to_folder1),  # Função correspondente
        ("Notas", go_to_folder2),
        ("Virada", go_to_folder3),
        ("Migração", go_to_folder4),
        ("Ferramentas", go_to_folder5),
        ("Outros", go_to_folder6),
    ]

    # Função de filtragem
    def filter_folders(e):
        search_text = e.control.value.lower()
        filtered_folders = [folder for folder in folders if search_text in folder[0].lower()]
        update_folder_buttons(filtered_folders)

    # Função para atualizar os botões com base nas pastas filtradas
    def update_folder_buttons(filtered_folders):
        folder_rows = []
        row = []
        for i, (folder_name, target_page_function) in enumerate(filtered_folders):
            folder_button = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.icons.FOLDER, size=200, color=ft.colors.YELLOW),  # Ícone da pasta
                        ft.Text(folder_name, size=20, color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5
                ),
                on_click=lambda e, func=target_page_function: folder_redirect(page, func),  # Função de redirecionamento
                padding=ft.padding.all(10),
                bgcolor='#081c15',
                border_radius=ft.border_radius.all(10),  # Bordas arredondadas para os ícones
                width=250,
                height=250
            )
            row.append(folder_button)

            # Agrupar 3 botões por linha
            if (i + 1) % 3 == 0 or i == len(filtered_folders) - 1:
                folder_rows.append(ft.Row(controls=row, alignment=ft.MainAxisAlignment.CENTER))
                row = []

        # Atualizar o conteúdo da página
        page.controls.clear()
        search_container = ft.Container(
            content=ft.TextField(
                hint_text="Search folders...",
                on_change=filter_folders,
                expand=True,
            ),
            padding=ft.padding.all(10),
        )
        page.add(drag_area)  # Adicionando a área de drag acima da barra de pesquisa
        page.add(search_container)
        main_container = ft.Container(
            content=ft.Column(
                controls=folder_rows,  # Adicionar rows de botões
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=ft.padding.all(0),
            margin=ft.Margin(left=0, right=0, top=0, bottom=0),
            bgcolor=ft.colors.TRANSPARENT  # Fundo transparente para o container principal
        )
        page.add(main_container)
        page.update()

    # Adicionar barra de pesquisa e inicializar os botões de pastas
    page.add(drag_area)  # Adicionando a área de drag no topo
    search_container = ft.Container(
        content=ft.TextField(
            hint_text="Pesquisar Scripts...",
            on_change=filter_folders,
            expand=True,
        ),
        padding=ft.padding.all(10),
    )
    page.add(search_container)
    update_folder_buttons(folders)

# Placeholder para as funções de redirecionamento
def go_to_folder1(page: ft.Page):
    from Libs.Scripts.Tabelas import tabelas_page
    page.clean()
    tabelas_page(page)
    page.update()
def go_to_folder2(page: ft.Page):
    from Libs.Scripts.Notas import notas_page
    page.clean()
    notas_page(page)
    page.update()
def go_to_folder3(page: ft.Page):
    from Libs.Scripts.Virada import virada_page
    page.clean()
    virada_page(page)
    page.update()
def go_to_folder4(page: ft.Page):
    from Libs.Scripts.Migração import migracao_page
    page.clean()
    migracao_page(page)
    page.update()
def go_to_folder5(page: ft.Page):
    from Libs.Scripts.Ferramentas import ferramentas_page
    page.clean()
    ferramentas_page(page)
    page.update()
def go_to_folder6(page: ft.Page):
    from Libs.Scripts.Outros import outros_page
    page.clean()
    outros_page(page)
    page.update()
