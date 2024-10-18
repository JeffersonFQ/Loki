import os, pyperclip
import flet as ft
from Libs.Public.ui import configure_main_window, go_to_login
from Libs.Public.utils import create_drag_area, create_drawer

pastas_historico = []

def handle_change(e, page: ft.Page):
    from Libs.Public.menu import menu_page
    from Libs.Scripts.scripts import scripts_page
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

def listar_pastas_e_arquivos(caminho, page, nivel=0, filtro=""):
    global pastas_historico
    try:
        folder_rows = []
        if nivel == 0:
            pastas_historico.clear()
            pastas_historico.append(caminho)
        else:
            pastas_historico.append(caminho)

        page.controls.clear()
        page.add(create_drag_area(page, create_drawer(page)))

        voltar_button = ft.IconButton(
            icon=ft.icons.ARROW_BACK,
            on_click=lambda e: voltar(page),
            tooltip="Voltar"
        )

        search_field = ft.TextField(
            hint_text="Pesquisar Pastas...",
            expand=True,
            bgcolor="#000000",
            color=ft.colors.WHITE,
            border_color=ft.colors.WHITE,
            text_size=20,
            autofocus=True,
            on_change=lambda e: listar_pastas_e_arquivos(caminho, page, nivel, e.control.value)
        )

        search_container = ft.Row(
            controls=[voltar_button, search_field],
            alignment=ft.MainAxisAlignment.START,
            spacing=10
        )

        page.add(search_container)

        # Lista de arquivos a serem ignorados
        arquivos_ignorados = ['desktop.ini','virada.py','__pycache__']

        for item in os.listdir(caminho):
            if filtro.lower() in item.lower() and item not in arquivos_ignorados:
                caminho_completo = os.path.join(caminho, item)
                item_tooltip = item

                if os.path.isdir(caminho_completo):
                    item_nome = item if len(item) <= 20 else item
                    folder_button = ft.Container(
                        content=ft.Column(
                            controls=[ft.Icon(ft.icons.FOLDER, size=100, color=ft.colors.YELLOW),
                                      ft.Text(item_nome, size=16, color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER, tooltip=item_tooltip)],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0
                        ),
                        on_click=lambda e, path=caminho_completo: listar_pastas_e_arquivos(path, page, nivel + 1, filtro),
                        padding=ft.padding.all(2),
                        bgcolor='#081c15',
                        border_radius=ft.border_radius.all(10),
                        width=150,
                        height=150
                    )
                    folder_rows.append(folder_button)
                elif item.endswith('.sql'):
                    item_nome = item if len(item) <= 20 else item
                    file_button = ft.Container(
                        content=ft.Column(
                            controls=[ft.Icon(ft.icons.DESCRIPTION, size=100, color=ft.colors.GREEN),
                                      ft.Text(item_nome, size=12, color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER, tooltip=item_tooltip)],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=5
                        ),
                        padding=ft.padding.all(10),
                        bgcolor='#081c15',
                        border_radius=ft.border_radius.all(10),
                        width=150,
                        height=150,
                        on_click=lambda e, path=caminho_completo: abrir_arquivo_sql(path, page)
                    )
                    folder_rows.append(file_button)
                else:
                    item_nome = item if len(item) <= 20 else item
                    file_button = ft.Container(
                        content=ft.Column(
                            controls=[ft.Icon(ft.icons.DESCRIPTION, size=100, color=ft.colors.GREEN),
                                      ft.Text(item_nome, size=12, color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER, tooltip=item_tooltip)],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0
                        ),
                        padding=ft.padding.all(2),
                        bgcolor='#081c15',
                        border_radius=ft.border_radius.all(10),
                        width=150,
                        height=150
                    )
                    folder_rows.append(file_button)

        if folder_rows:
            scroll_container = ft.Container(
                content=ft.Row(
                    controls=folder_rows,
                    alignment=ft.MainAxisAlignment.CENTER,
                    wrap=True,
                    scroll=ft.ScrollMode.HIDDEN
                ),
                height=530,
                bgcolor='Transparent'
            )
            page.add(scroll_container)

        page.update()
    except PermissionError:
        mostrar_erro(page, "Sem permissão para acessar esta pasta.")
    except FileNotFoundError:
        mostrar_erro(page, "Pasta não encontrada.")
    except Exception as e:
        mostrar_erro(page, f"Ocorreu um erro: {str(e)}")

def abrir_arquivo_sql(caminho, page: ft.Page):
    try:
        with open(caminho, 'r', encoding='utf-8') as file:
            conteudo = file.read()

        def copiar_conteudo(e):
            pyperclip.copy(conteudo)
            print("Conteúdo copiado para a área de transferência.")

        def executar_sql(e):
            print("Executando o SQL...")

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Conteúdo do arquivo .sql"),
            content=ft.Container(
                content=ft.Text(conteudo, selectable=True),
                height=300,
                width=500
            ),
            actions=[
                ft.TextButton("Copiar", on_click=copiar_conteudo),
                ft.TextButton("Executar", on_click=executar_sql),
                ft.TextButton("Fechar", on_click=lambda e: close_dialog(page, dlg_modal)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.overlay.append(dlg_modal)
        dlg_modal.open = True
        page.update()
    except Exception as e:
        print(f"Erro ao abrir o arquivo: {str(e)}")

def close_dialog(page: ft.Page, dialog: ft.AlertDialog):
    dialog.open = False
    page.update()

def mostrar_erro(page, mensagem):
    page.controls.clear()
    error_container = ft.Container(
        content=ft.Text(mensagem, color=ft.colors.RED),
        padding=ft.padding.all(10),
        alignment=ft.alignment.center
    )
    page.add(error_container)
    page.update()

def voltar(page: ft.Page):
    global pastas_historico
    if pastas_historico and pastas_historico[-1] == "./Libs/Scripts/Virada/":
        from Libs.Scripts.scripts import scripts_page
        page.clean()
        scripts_page(page)
    elif len(pastas_historico) > 1:
        pastas_historico.pop()
        caminho_anterior = pastas_historico[-1]
        listar_pastas_e_arquivos(caminho_anterior, page, nivel=len(pastas_historico) - 1)

def virada_page(page: ft.Page):
    configure_main_window(page)
    page.bgcolor = '#081c15'
    page.title = "Menu Scripts"
    page.window.title_bar_hidden = True
    page.window.maximizable = False
    page.window.resizable = False
    page.theme_mode = 'Dark'
    page.window.border_color = ft.colors.TRANSPARENT

    path_to_list = "./Libs/Scripts/Virada/"
    listar_pastas_e_arquivos(path_to_list, page)
