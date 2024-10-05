import subprocess
import os
import flet as ft
from datetime import datetime
from Libs.Data.firebase_config import db

def show_snackbar(page, message, is_error=False, color='#008000'):
    bgcolor = '#7B0000' if is_error else color
    snackbar = ft.SnackBar(
        content=ft.Text(message, color=ft.colors.WHITE),
        bgcolor=bgcolor,
        action="OK!",
        action_color="White",
        behavior=ft.SnackBarBehavior.FLOATING,
        duration=3000,
        width=400,
    )
    page.overlay.append(snackbar)
    snackbar.open = True
    page.update()

def create_drag_area(page: ft.Page, drawer: ft.NavigationDrawer): 
    drag_area = ft.WindowDragArea(
        ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(ft.icons.MENU, on_click=lambda e: page.open(drawer), width=50, height=50, icon_color='White'),
                    ft.IconButton(ft.icons.CLOSE, on_click=lambda e: page.window.close(), width=50, height=50, icon_color='White')
                ],                
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                expand=True
            ),
            bgcolor=ft.colors.TRANSPARENT,
            padding=ft.padding.all(0),
            height=40,
            margin=ft.Margin(left=0, right=0, top=0, bottom=0)
        ),
        maximizable=False,
        expand=False
    )
    return drag_area

def handle_change(e, page: ft.Page):
    selected_index = e.control.selected_index
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    destinations = [
        "Clientes", "Scripts SQL", "Dashboard", 
        "WikiSN", "Menu Técnico", "API Movdesk", 
        "Configurações", "Sair"
    ]
    
    if selected_index < len(destinations):
        show_snackbar(page, f"Navegando para {destinations[selected_index]} - {current_time}")
    if selected_index == 7:  
        show_snackbar(page, f"Sair - {current_time}")
        page.window.close()

def create_drawer(page: ft.Page):
    drawer = ft.NavigationDrawer(
        on_change=lambda e: handle_change(e, page),
        indicator_color="#CC8105",
        bgcolor='#081c15',
        shadow_color='#081c15',
        controls=[
            ft.Column(
                [
                    ft.Container(height=30),
                    ft.Container(
                        content=ft.Image(
                            src="../Resources/logo3.svg",
                            width=150,
                            height=150,
                            fit=ft.ImageFit.CONTAIN
                        ),
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(height=30),
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.NavigationDrawerDestination(label="Clientes", icon=ft.icons.PEOPLE_ALT),
            ft.NavigationDrawerDestination(label="Scripts SQL", icon=ft.icons.ALL_INBOX),
            ft.NavigationDrawerDestination(label="Dashboard", icon=ft.icons.TRENDING_UP),
            ft.NavigationDrawerDestination(label="WikiSN", icon=ft.icons.BOOK_SHARP),
            ft.NavigationDrawerDestination(label="Menu Técnico", icon=ft.icons.BUILD),
            ft.NavigationDrawerDestination(label="API Movdesk", icon=ft.icons.SWAP_VERT_CIRCLE_ROUNDED),
            ft.NavigationDrawerDestination(label="Configurações", icon=ft.icons.SETTINGS_OUTLINED),
            ft.NavigationDrawerDestination(label="Sair", icon=ft.icons.EXIT_TO_APP_OUTLINED),
        ],
    )
    return drawer

def create_client_button(client_id, client_name, page):
    return ft.Container(
        content=ft.Row(
            [
                ft.Text(client_name, color="#081c15", weight="bold", size=16),
                ft.IconButton(
                    icon=ft.icons.MORE_VERT,
                    icon_color="#081c15",
                    on_click=lambda e: on_settings_click(e, client_id, page),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
        ),
        width=240,
        height=60,
        border_radius=15,
        padding=10,
        bgcolor="#CC8105",  # Use "bgcolor" para definir a cor de fundo
        border=ft.Border(
            left=ft.BorderSide(2, "black"),
            top=ft.BorderSide(2, "black"),
            right=ft.BorderSide(2, "black"),
            bottom=ft.BorderSide(2, "black"),
        ),
        on_click=lambda e: on_folder_button_click(client_id, page),
    )

def on_folder_button_click(client_id, page):
    try:
        client_data = db.child("clientes").child(client_id).get()

        if client_data.each():
            client_info = client_data.val()
            anydesk_id = client_info.get("CONEXAO")
            password = client_info.get("SENHA")

            if anydesk_id and password:
                command = f'echo {password} | "C:\\Program Files (x86)\\AnyDesk\\AnyDesk.exe" {anydesk_id} --with-password'
                subprocess.run(command, shell=True)
                print(f"Conectando ao AnyDesk com ID: {anydesk_id} e senha: {password}")
            else:
                print("ID do AnyDesk ou senha não encontrados.")
                show_snackbar(page, "ID do AnyDesk ou senha não encontrados.", is_error=True)
        else:
            print("Cliente não encontrado.")
            show_snackbar(page, "Cliente não encontrado.", is_error=True)

    except Exception as e:
        print(f"Erro ao acessar o cliente: {e}")
        show_snackbar(page, "Erro ao acessar o cliente.", is_error=True)

def filter_clients(all_clients, search_text, field):
    return [
        client for client in all_clients
        if search_text.lower() in str(client[field]).lower()
    ]

def update_client_list(search_text, all_clients, client_list_container, page, field):
    client_list_container.controls = []
    filtered_clients = filter_clients(all_clients, search_text, field)

    for client in filtered_clients:
        client_list_container.controls.append(
            ft.Container(client['button'], margin=ft.margin.symmetric(vertical=10))
        )

    page.update()

def on_settings_click(e, client_id, page):
    try:
        client_data = db.child("clientes").child(client_id).get()
        if client_data.each():
            client_info = client_data.val()
            
            cnpj_input = ft.TextField(label="CNPJ", value=client_info.get("CNPJ", ""), width=400)
            nome_input = ft.TextField(label="Nome", value=client_info.get("NOME", ""), width=400)
            fantasia_input = ft.TextField(label="Razão", value=client_info.get("RAZAO", ""), width=400)
            ip_input = ft.TextField(label="IP", value=client_info.get("IP", ""), width=400)
            porta_input = ft.TextField(label="Porta", value=client_info.get("PORTA", ""), width=400)
            conexao_input = ft.TextField(label="Conexão", value=client_info.get("CONEXAO", ""), width=400)
            senha_input = ft.TextField(label="Senha", value=client_info.get("SENHA", ""), width=400)

            def save_changes(e):
                updated_data = {
                    "CNPJ": cnpj_input.value,
                    "NOME": nome_input.value,
                    "FANTASIA": fantasia_input.value,
                    "IP": ip_input.value,
                    "PORTA": porta_input.value,
                    "CONEXAO": conexao_input.value,
                    "SENHA": senha_input.value
                }
                
                db.child("clientes").child(client_id).update(updated_data)
                show_snackbar(page, "Informações atualizadas com sucesso!", color='green')
                
                modal.open = False
                page.update()

            modal = ft.AlertDialog(
                title=ft.Text("Editar Cliente"),
                content=ft.Column(
                    controls=[cnpj_input, nome_input, fantasia_input, ip_input, porta_input, conexao_input, senha_input]
                ),
                actions=[
                    ft.TextButton("Salvar", on_click=save_changes),
                    ft.TextButton("Cancelar", on_click=lambda e: close_modal(modal, page))
                ]
            )
            page.add(modal)
            modal.open = True
            page.update()

    except Exception as e:
        print(f"Erro ao carregar informações do cliente: {e}")
        show_snackbar(page, "Erro ao carregar informações do cliente.", is_error=True)

def close_modal(modal, page):
    modal.open = False
    page.update()

def log_action(action: str):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{current_time} - {action}")
