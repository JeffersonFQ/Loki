import flet as ft
from Libs.Data.firebase_config import db
from Libs.Public.ui import configure_main_window, go_to_login
from Libs.Public.utils import create_client_button, update_client_list, create_drag_area, create_drawer
import re

def handle_change(e, page: ft.Page):
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

def filter_clients(all_clients, search_text, field):
    return [client for client in all_clients if search_text.lower() in client[field].lower()]

def menu_page(page: ft.Page):
    configure_main_window(page)
    page.title = "Menu Principal"
    page.window.title_bar_hidden = True
    page.window.maximizable = False
    page.window.resizable = False
    page.theme_mode = 'Dark'

    drawer = create_drawer(page)
    drawer.selected_index = 0
    drawer.on_change = lambda e: handle_change(e, page)

    drag_area = create_drag_area(page, drawer)

    main_container = ft.Container(
        content=ft.Column(
            controls=[drag_area],
            expand=True,
        ),
        padding=ft.padding.all(0),
        margin=ft.Margin(left=0, right=0, top=0, bottom=0)
    )

    client_list_container = ft.Column(expand=True)

    search_field_nome = ft.TextField(
        hint_text="Buscar por Nome",
        on_change=lambda e: update_client_list(e.control.value, all_clients, client_list_container, page, 'NOME'),
        width=360,
        autofocus=True,
        border_color='White',
        bgcolor='Black'
    )
    search_field_fantasia = ft.TextField(
        hint_text="Buscar por Razão",
        on_change=lambda e: update_client_list(e.control.value, all_clients, client_list_container, page, 'RAZAO'),
        width=360,
        border_color='White',
        bgcolor='Black'
    )
    search_field_cnpj = ft.TextField(
        hint_text="Buscar CNPJ Matriz",
        on_change=lambda e: update_client_list(e.control.value, all_clients, client_list_container, page, 'CNPJ'),
        width=180,
        border_color='White',
        bgcolor='Black'
    )

    add_client_button = ft.ElevatedButton(
        text="Novo Cliente",
        icon=ft.icons.ADD,
        on_click=lambda e: open_add_client_page(page),
        bgcolor='#CC8105',
        color='White'
    )

    search_container = ft.Container(
        content=ft.Row(
            controls=[
                search_field_nome,
                search_field_fantasia,
                search_field_cnpj,
                add_client_button
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=ft.padding.all(20),
    )

    main_container.content.controls.append(search_container)

    all_clients = []
    clients_data = db.child("clientes").get()

    if clients_data.each():
        for client in clients_data.each():
            client_id = client.key()
            client_info = client.val()
            if client_info:
                client_name = client_info.get("NOME", "Cliente Desconhecido")
                client_cnpj = client_info.get("CNPJ", "")
                client_fantasia = client_info.get("FANTASIA", "")
                button = create_client_button(client_id, client_name, page)
                all_clients.append({
                    'id': client_id,
                    'NOME': client_name,
                    'CNPJ': client_cnpj,
                    'FANTASIA': client_fantasia,
                    'button': button
                })
                client_list_container.controls.append(ft.Container(button, margin=ft.Margin(left=20, right=0, top=15, bottom=15)))
            else:
                print(f"Informações do cliente com ID {client_id} não encontradas.")
    else:
        print("Nenhum cliente encontrado.")

    main_container.content.controls.append(client_list_container)

    page.add(main_container)
    page.update()

def open_add_client_page(page: ft.Page, client_data=None):
    nome_value = client_data["NOME"] if client_data else ""
    razao_value = client_data["RAZAO"] if client_data else ""
    cnpj_value = client_data["CNPJ"] if client_data else ""
    conexao_value = client_data["CONEXAO"] if client_data else ""
    senha_value = client_data["SENHA"] if client_data else ""
    ip_value = client_data["IP"] if client_data else ""
    porta_value = client_data["PORTA"] if client_data else ""

    add_client_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Novo Cliente", weight=ft.FontWeight.BOLD),
        content=ft.Column(
            controls=[
                ft.TextField(label="Nome", width=300, value=nome_value),
                ft.TextField(label="Razão", width=300, value=razao_value),
                ft.TextField(label="CNPJ", width=300, value=cnpj_value),
                ft.TextField(label="Conexão", width=300, value=conexao_value),
                ft.TextField(label="Senha", width=300, password=True, value=senha_value),
                ft.TextField(label="IP", width=300, value=ip_value),
                ft.TextField(label="Porta", width=300, value=porta_value),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=15
        ),
        actions=[
            ft.Row(
                controls=[
                    ft.ElevatedButton(
                        text="Salvar",
                        icon=ft.icons.SAVE,
                        on_click=lambda e: save_client(e, page, add_client_dialog),
                        width=150
                    ),
                    ft.TextButton(
                        text="Voltar",
                        on_click=lambda e: close_dialog(page, add_client_dialog),
                        width=150
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER
    )

    page.overlay.append(add_client_dialog)
    add_client_dialog.open = True
    page.update()

def validate_client_data(client_data, fields):
    errors = []
    color_map = {
        "NOME": None,
        "RAZAO": None,
        "CNPJ": None,
        "CONEXAO": None,
        "PORTA": None,
        "IP": None,
    }

    if not client_data["NOME"]:
        errors.append("O NOME não pode ser nulo.")
        color_map["NOME"] = ft.colors.RED

    if not client_data["RAZAO"]:
        errors.append("A RAZÃO não pode ser nula.")
        color_map["RAZAO"] = ft.colors.RED

    if not client_data["CNPJ"] or (len(client_data["CNPJ"]) != 11 and len(client_data["CNPJ"]) != 14):
        errors.append("O CNPJ deve conter 11 ou 14 números e não pode ser nulo.")
        color_map["CNPJ"] = ft.colors.RED

    if client_data["CONEXAO"] and not client_data["CONEXAO"].isdigit():
        errors.append("A CONEXÃO deve conter apenas números.")
        color_map["CONEXAO"] = ft.colors.RED

    if client_data["PORTA"]:
        if not (client_data["PORTA"].isdigit() and len(client_data["PORTA"]) == 4):
            errors.append("A PORTA deve conter exatamente 4 dígitos numéricos.")
            color_map["PORTA"] = ft.colors.RED

    ip_pattern = re.compile(r'^\d{1,3}(\.\d{1,3}){0,3}$')
    if client_data["IP"] and not ip_pattern.match(client_data["IP"]):
        errors.append("O IP deve conter apenas números e pontos.")
        color_map["IP"] = ft.colors.RED

    for field_id in fields:
        field_id.bgcolor = color_map.get(field_id.label, None)

    return errors

def save_client(event, page: ft.Page, dialog: ft.AlertDialog):
    fields = dialog.content.controls

    client_data = {
        "NOME": fields[0].value,
        "RAZAO": fields[1].value,
        "CNPJ": fields[2].value,
        "CONEXAO": fields[3].value,
        "SENHA": fields[4].value,
        "IP": fields[5].value,
        "PORTA": fields[6].value,
    }

    validation_errors = validate_client_data(client_data, fields)

    if validation_errors:
        error_message = "\n".join(validation_errors)
        error_dialog = ft.AlertDialog(
            title=ft.Text("Erro ao Salvar Cliente"),
            content=ft.Text(error_message),
            actions=[ft.TextButton("Fechar", on_click=lambda e: close_dialog(page, error_dialog))],
        )
        page.overlay.append(error_dialog)
        error_dialog.open = True
        page.update()
        return

    try:
        db.child("clientes").push(client_data)
        print("Cliente salvo com sucesso!")
    except Exception as e:
        error_dialog = ft.AlertDialog(
            title=ft.Text("Erro ao Salvar Cliente"),
            content=ft.Text(f"Erro: {str(e)}"),
            actions=[ft.TextButton("Fechar", on_click=lambda e: close_dialog(page, error_dialog))],
        )
        page.overlay.append(error_dialog)
        error_dialog.open = True
        page.update()
        return

    close_dialog(page, dialog)

def close_dialog(page: ft.Page, dialog: ft.AlertDialog):
    dialog.open = False
    page.update()
