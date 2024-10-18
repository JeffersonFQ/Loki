import os
import pyperclip, pyodbc
import flet as ft
from pathlib import Path
from Libs.Data.sql_server_config import initialize_sql_server
from Libs.Public.ui import configure_main_window, go_to_login
from Libs.Public.utils import create_drag_area, create_drawer

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
            controls=[voltar_button, search_field],
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
        mostrar_erro(page, "Sem permissão para acessar esta pasta.")
    except FileNotFoundError:
        mostrar_erro(page, "Pasta não encontrada.")
    except Exception as e:
        mostrar_erro(page, f"Ocorreu um erro: {str(e)}")


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
            print("Conteúdo copiado para a área de transferência.")

        # Função para solicitar o valor de uma variável DECLARE
        def solicitar_valor_variavel(variavel):
            # Aqui você pode adicionar uma interface para o usuário inserir o valor
            # Por enquanto, usaremos uma entrada padrão para simplificar
            valor = input(f"Insira o valor para a variável {variavel}: ")
            return valor

        # Função para substituir o valor da variável DECLARE
        def substituir_valor_declare(conteudo):
            linhas = conteudo.splitlines()
            novo_conteudo = []
            for linha in linhas:
                if linha.strip().upper().startswith("DECLARE"):
                    # Extrai o nome da variável e substitui pelo valor fornecido pelo usuário
                    partes = linha.split()
                    if len(partes) > 1:
                        variavel = partes[1]
                        valor = solicitar_valor_variavel(variavel)
                        linha = f"DECLARE {variavel} = {valor};"
                novo_conteudo.append(linha)
            return "\n".join(novo_conteudo)

        # Função para executar o comando SQL no servidor SQL
        def executar_sql(e):
            try:
                # Substitui o valor da variável DECLARE, se necessário
                conteudo_modificado = substituir_valor_declare(conteudo)

                # Inicializa a conexão com o SQL Server
                conn = initialize_sql_server()
                if conn is not None:
                    cursor = conn.cursor()

                    # Executa o script SQL
                    print("Executando SQL...")
                    cursor.execute(conteudo_modificado)
                    conn.commit()

                    # Fecha o cursor e a conexão
                    cursor.close()
                    conn.close()
                    print("Script SQL executado com sucesso.")
                else:
                    print("Erro ao estabelecer a conexão com o banco de dados.")
            except pyodbc.Error as db_err:
                print(f"Erro no banco de dados: {str(db_err)}")
            except Exception as ex:
                print(f"Erro ao executar o SQL: {str(ex)}")

        # Exibir o conteúdo do arquivo e botões de ação no diálogo modal
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
        
        # Adiciona o diálogo modal à página
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
