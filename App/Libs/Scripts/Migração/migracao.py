import os
import flet as ft
from Libs.Public.ui import configure_main_window, go_to_login
from Libs.Public.utils import create_drag_area, create_drawer

def handle_change(e, page: ft.Page):
    selected_index = e.control.selected_index
    page.clean()

    if selected_index == 7:
        go_to_login(page)

    page.update()

def redirect_to(page: ft.Page, target_page_function):
    page.clean()
    target_page_function(page)
    page.update()

def folder_redirect(page: ft.Page, target_page_function):
    redirect_to(page, target_page_function)

def migracao_page(page: ft.Page):
    configure_main_window(page)

    page.bgcolor = '#081c15'
    page.title = "Menu Scripts"
    page.window.title_bar_hidden = True
    page.theme_mode = 'Dark'

    drawer = create_drawer(page)
    drawer.on_change = lambda e: handle_change(e, page)
    drag_area = create_drag_area(page, drawer)

    folders = [
        ("Download", go_to_downmigracao),
        ("Upload", go_to_new_file)
    ]

    def update_folder_buttons(filtered_folders):
        folder_rows = []
        row = []
        for i, (folder_name, target_page_function) in enumerate(filtered_folders):
            folder_button = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.icons.FOLDER if folder_name == "Download" else ft.icons.UPLOAD_FILE, size=200, color=ft.colors.YELLOW),
                        ft.Text(folder_name, size=20, color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5
                ),
                on_click=lambda e, func=target_page_function: folder_redirect(page, func),
                padding=ft.padding.all(10),
                bgcolor='#081c15',
                border_radius=ft.border_radius.all(10),
                width=250,
                height=250
            )
            row.append(folder_button)

            if (i + 1) % 2 == 0 or i == len(filtered_folders) - 1:
                folder_rows.append(ft.Row(controls=row, alignment=ft.MainAxisAlignment.CENTER))
                row = []

        page.controls.clear()

        back_button = ft.ElevatedButton(
            text="Voltar",
            on_click=lambda e: go_to_script(page),
            bgcolor='#CC8105',
            color=ft.colors.WHITE,
            width=100
        )

        def go_to_script(page):
            from Libs.Scripts.scripts import scripts_page
            page.clean()
            scripts_page(page)
            page.update()
        
        page.add(drag_area)
        page.add(back_button)

        main_container = ft.Container(
            content=ft.Column(
                controls=folder_rows,
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            bgcolor=ft.colors.TRANSPARENT
        )
        page.add(main_container)
        page.update()

    page.add(drag_area)
    update_folder_buttons(folders)

def go_to_new_file(page: ft.Page):
    page.clean()
    page.add(ft.Text("Nova página de arquivo"))  # Exemplo simples
    page.update()

def go_to_downmigracao(page: ft.Page):
    page.clean()
    downmigracao_page(page)
    page.update()

def downmigracao_page(page: ft.Page):
    page.clean()
    
    # Pasta onde os arquivos .sql estão localizados
    sql_directory = "./Libs/Scripts/Migração"  # Certifique-se de que esse diretório contém arquivos .sql

    # Lista os arquivos .sql no diretório especificado
    def list_sql_files(directory):
        try:
            # Depuração: Exibir arquivos no diretório
            print(f"Listando arquivos no diretório: {directory}")
            files = os.listdir(directory)
            print(f"Arquivos encontrados: {files}")
            return [f for f in files if f.endswith('.sql')]
        except Exception as e:
            print(f"Erro ao listar arquivos: {e}")
            return []

    # Atualiza os botões na página com os arquivos .sql
    def update_folder_buttons(sql_files):
        folder_rows = []
        row = []
        for i, filename in enumerate(sql_files):
            folder_button = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.icons.DESCRIPTION, size=200, color=ft.colors.YELLOW),  # Usando ícone de arquivo
                        ft.Text(filename, size=20, color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5
                ),
                on_click=lambda e, file=filename: open_sql_file(page, file),
                padding=ft.padding.all(10),
                bgcolor='#081c15',
                border_radius=ft.border_radius.all(10),
                width=250,
                height=250
            )
            row.append(folder_button)

            if (i + 1) % 2 == 0 or i == len(sql_files) - 1:
                folder_rows.append(ft.Row(controls=row, alignment=ft.MainAxisAlignment.CENTER))
                row = []

        back_button = ft.ElevatedButton(
            text="Voltar",
            on_click=lambda e: migracao_page(page),
            bgcolor='#CC8105',
            color=ft.colors.WHITE,
            width=100
        )

        page.controls.clear()
        page.add(back_button)

        main_container = ft.Container(
            content=ft.Column(
                controls=folder_rows,
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            bgcolor=ft.colors.TRANSPARENT
        )
        page.add(main_container)
        page.update()

    # Cria botões para os arquivos .sql
    sql_files = list_sql_files(sql_directory)
    update_folder_buttons(sql_files)

def open_sql_file(page: ft.Page, filename: str):
    page.clean()
    page.add(ft.Text(f"Abrindo arquivo: {filename}"))  # Exemplo de ação ao abrir o arquivo
    page.update()
