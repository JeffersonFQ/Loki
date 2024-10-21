import os
import re
import pyperclip
import pyodbc
import flet as ft
from pathlib import Path
from Libs.Data.sql_server_config import initialize_sql_server
from Libs.Public.ui import configure_main_window, go_to_login
from Libs.Public.utils import create_drag_area, create_drawer, show_snackbar

pastas_historico = []

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

        # Manter a drag bar ao atualizar a página
        if len(page.controls) == 0:
            drawer = create_drawer(page)
            drawer.selected_index = 1
            drawer.on_change = lambda e: handle_change(e, page)
            drag_area = create_drag_area(page, drawer)
            page.add(drag_area)

        voltar_button = ft.IconButton(
            icon=ft.icons.ARROW_BACK,
            on_click=lambda e: voltar(page),
            tooltip="Voltar",
            disabled=(nivel == 0)  # Desativa o botão se estiver no nível inicial
        )

        # Adiciona um botão para ir à pasta raiz
        raiz_button = ft.IconButton(
            icon=ft.icons.HOME,
            on_click=lambda e: listar_pastas_e_arquivos("./Libs/Scripts", page, 0, filtro),
            tooltip="Ir para a Raiz",
            disabled=(nivel == 0)  # Desativa o botão se já estiver na raiz
        )

        search_field = ft.TextField(
            hint_text="Pesquisar Pastas e Arquivos...",
            expand=True,
            bgcolor="#000000",
            color=ft.colors.WHITE,
            border_color=ft.colors.WHITE,
            text_size=20,
            autofocus=True,
            value=filtro,  # Preenche o valor atual da pesquisa
            on_change=lambda e: listar_pastas_e_arquivos(caminho, page, nivel, e.control.value)
        )

        search_container = ft.Row(
            controls=[voltar_button, raiz_button, search_field],
            alignment=ft.MainAxisAlignment.START,
            spacing=10
        )

        page.add(search_container)

        arquivos_ignorados = ['desktop.ini', '__pycache__']

        # Função para buscar no nível atual ou recursivamente se houver um filtro
        def buscar_arquivos_e_pastas(pasta, filtro, recursivo=False):
            resultados = []
            with os.scandir(pasta) as it:
                for entry in it:
                    if filtro.lower() in entry.name.lower() and entry.name not in arquivos_ignorados:
                        if entry.is_dir():
                            resultados.append((entry.path, 'pasta'))
                        elif entry.is_file() and entry.name.endswith('.sql'):
                            resultados.append((entry.path, 'arquivo'))

                    # Se o filtro estiver ativo, buscar recursivamente
                    if recursivo and entry.is_dir():
                        resultados.extend(buscar_arquivos_e_pastas(entry.path, filtro, recursivo=True))
            return resultados

        # Se houver filtro, buscar recursivamente, senão, buscar apenas no nível atual
        recursivo = bool(filtro)  # Buscar recursivamente apenas se houver filtro
        resultados = buscar_arquivos_e_pastas(caminho, filtro, recursivo)

        # Exibir os resultados encontrados
        for caminho_completo, tipo in resultados:
            item = os.path.basename(caminho_completo)
            item_tooltip = item

            if tipo == 'pasta':
                folder_button = ft.Container(
                    content=ft.Column(
                        controls=[ft.Icon(ft.icons.FOLDER, size=100, color=ft.colors.YELLOW),
                                  ft.Text(item, size=16, color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER, tooltip=item_tooltip)],
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
            elif tipo == 'arquivo':
                file_button = ft.Container(
                    content=ft.Column(
                        controls=[ft.Icon(ft.icons.DESCRIPTION, size=100, color=ft.colors.GREEN),
                                  ft.Text(item, size=12, color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER, tooltip=item_tooltip)],
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
        else:
            page.add(ft.Text("Nenhuma pasta ou arquivo encontrado.", color=ft.colors.RED))

        page.update()
    except PermissionError:
        show_snackbar(page, f"Sem permissão para acessar esta pasta.", is_error=True)
    except FileNotFoundError:
        show_snackbar(page, f"Pasta não encontrada.", is_error=True)
    except Exception as e:
        show_snackbar(page, f"Ocorreu um erro: {str(e)}", is_error=True)

def voltar(page: ft.Page):
    global pastas_historico
    if len(pastas_historico) > 1:
        pastas_historico.pop()  # Remove a pasta atual do histórico
        caminho_anterior = pastas_historico[-1]  # Obtém a pasta anterior
        listar_pastas_e_arquivos(caminho_anterior, page, len(pastas_historico) - 1)  # Retorna ao nível anterior

def scripts_page(page: ft.Page):
    configure_main_window(page)
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

    # Adiciona a lista de pastas para navegação
    page.add(drag_area)
    listar_pastas_e_arquivos("./Libs/Scripts", page)

def abrir_arquivo_sql(caminho, page: ft.Page):
    try:
        # Abre o arquivo .sql e lê seu conteúdo
        with open(caminho, 'r', encoding='utf-8') as file:
            conteudo = file.read()

        # Função para copiar o conteúdo para a área de transferência
        def copiar_conteudo(e):
            pyperclip.copy(conteudo)
            show_snackbar(page, f"Conteúdo copiado para a área de transferência.", is_error=False)

        # Função para solicitar os valores para placeholders
        def solicitar_valores_para_placeholders(script):
            placeholder_pattern = r"\{(\w+)\}"
            matches = re.findall(placeholder_pattern, script)

            # Criar um dicionário para armazenar os campos de texto
            fields = []
            for var in matches:
                text_field = ft.TextField(label=f"Valor para {{{var}}}", width=300)
                fields.append((var, text_field))

            return fields

        # Criar os campos de texto para cada placeholder encontrado no script SQL
        placeholder_fields = solicitar_valores_para_placeholders(conteudo)

        # Função para executar o comando SQL no servidor SQL
        def executar_sql(e):
            try:
                # Coletar os valores dos campos de texto
                valores = {var: field.value for var, field in placeholder_fields}

                # Conectar ao SQL Server
                conn = initialize_sql_server()
                cursor = conn.cursor()

                # Substituir os placeholders no script
                script_completo = conteudo.format(**valores)

                # Executar o comando SQL
                cursor.execute(script_completo)
                conn.commit()

                show_snackbar(page, f"Comando SQL executado com sucesso.", is_error=False)
            except Exception as ex:
                show_snackbar(page, f"Erro ao executar o comando: {str(ex)}", is_error=True)
            finally:
                cursor.close()
                conn.close()

        # Exibir um diálogo com o conteúdo do arquivo SQL e opções para copiar e executar
        page.dialog = ft.AlertDialog(
            title="Conteúdo do Arquivo SQL",
            content=ft.Column(controls=[
                ft.TextArea(value=conteudo, height=300, width=400),
                *[field for var, field in placeholder_fields]
            ]),
            actions=[
                ft.TextButton("Copiar", on_click=copiar_conteudo),
                ft.TextButton("Executar", on_click=executar_sql),
                ft.TextButton("Fechar", on_click=lambda e: page.dialog.close())
            ]
        )
        page.dialog.open = True
        page.update()

    except Exception as e:
        show_snackbar(page, f"Ocorreu um erro ao abrir o arquivo: {str(e)}", is_error=True)
