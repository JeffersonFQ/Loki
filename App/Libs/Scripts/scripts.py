import flet as ft
from pathlib import Path
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

def redirect_to(page: ft.Page, target_page_function):
    page.clean()
    target_page_function(page)
    page.update()

def folder_redirect(page: ft.Page, target_page_function):
    redirect_to(page, target_page_function)

def scripts_page(page: ft.Page):
    configure_main_window(page)

    # Configurações da página
    page.bgcolor = '#081c15'
    page.title = "Menu Scripts"
    page.window.title_bar_hidden = True
    page.window.maximizable = False
    page.window.resizable = False
    page.theme_mode = 'Dark'
    page.window.border_color = ft.colors.TRANSPARENT

    # Criação do drawer e área de drag
    drawer = create_drawer(page)
    drawer.selected_index = 1
    drawer.on_change = lambda e: handle_change(e, page)
    drag_area = create_drag_area(page, drawer)

    # Lista de pastas com funções de redirecionamento
    folders = [
        ("Tabelas", go_to_folder1),
        ("Notas", go_to_folder2),
        ("Virada", go_to_folder3),
        ("Migração", go_to_folder4),
        ("Ferramentas", go_to_folder5),
        ("Outros", go_to_folder6)
    ]

    # Função de busca de arquivos SQL
    def search_sql_files(search_text):
        caminho_pasta = Path("C:/Users/jeffe/Documents/Mega Pessoal/SCRIPT")
        return [str(file) for file in caminho_pasta.rglob('*.sql') if search_text in file.name.lower()]

    # Atualiza os botões de arquivos SQL e pastas encontrados
    def update_results(search_text):
        sql_files = search_sql_files(search_text) if search_text else []  # Atualiza a busca de arquivos SQL
        filtered_folders = [folder for folder in folders if search_text in folder[0].lower()]

        folder_rows = []
        sql_file_rows = []
        
        # Organiza pastas em linhas
        for folder_name, target_page_function in filtered_folders:
            folder_button = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.icons.FOLDER, size=100, color=ft.colors.YELLOW),
                        ft.Text(folder_name, size=16, color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5
                ),
                on_click=lambda e, func=target_page_function: folder_redirect(page, func),
                padding=ft.padding.all(10),
                bgcolor='#081c15',
                border_radius=ft.border_radius.all(10),
                width=150,
                height=150
            )
            folder_rows.append(folder_button)

        # Organiza arquivos SQL em linhas
        for file_path in sql_files:
            sql_file_button = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.icons.DOCUMENT_SCANNER, size=100, color=ft.colors.GREEN),
                        ft.Text(Path(file_path).name, size=16, color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5
                ),
                padding=ft.padding.all(10),
                bgcolor='#081c15',
                border_radius=ft.border_radius.all(10),
                width=150,
                height=200
            )
            sql_file_rows.append(sql_file_button)

        # Limpa e atualiza a página com os novos botões
        page.controls.clear()
        page.add(drag_area)
        page.add(search_container)

        # Adiciona pastas em uma grade
        if folder_rows:
            page.add(ft.Row(controls=folder_rows, alignment=ft.MainAxisAlignment.CENTER, wrap=True))

        # Adiciona arquivos SQL em uma grade
        if sql_file_rows:
            page.add(ft.Row(controls=sql_file_rows, alignment=ft.MainAxisAlignment.CENTER, wrap=True))

        page.update()  # Atualiza a página, mas mantém o foco

    # Campo de busca
    def search_changed(e):
        search_text = e.control.value.lower()
        update_results(search_text)

    search_container = ft.Container(
        content=ft.TextField(
            hint_text="Pesquisar Pastas e Arquivos SQL...",
            on_change=search_changed,
            expand=True,
            bgcolor="#000000",  # Fundo preto
            color=ft.colors.WHITE,  # Texto branco
            border_color=ft.colors.WHITE,  # Bordas brancas
            text_size=20,  # Aumenta o tamanho do texto
            autofocus=True  # Mantém o foco no campo de busca
        ),
        padding=ft.padding.all(10),
    )

    # Inicializa a página com os controles
    page.add(drag_area)
    page.add(search_container)
    update_results('')  # Atualiza inicialmente para mostrar somente pastas

# Placeholder para as funções de redirecionamento
def go_to_folder1(page: ft.Page):
    from Libs.Scripts.Tabelas.tabelas import tabelas_page
    page.clean()
    tabelas_page(page)
    page.update()

def go_to_folder2(page: ft.Page):
    from Libs.Scripts.Notas.notas import notas_page
    page.clean()
    notas_page(page)
    page.update()

def go_to_folder3(page: ft.Page):
    from Libs.Scripts.Virada.virada import virada_page
    page.clean()
    virada_page(page)
    page.update()

def go_to_folder4(page: ft.Page):
    from Libs.Scripts.Migração.migracao import migracao_page
    page.clean()
    migracao_page(page)
    page.update()

def go_to_folder5(page: ft.Page):
    from Libs.Scripts.Ferramentas.ferramentas import ferramentas_page
    page.clean()
    ferramentas_page(page)
    page.update()

def go_to_folder6(page: ft.Page):
    from Libs.Scripts.Outros.outros import outros_page
    page.clean()
    outros_page(page)
    page.update()
