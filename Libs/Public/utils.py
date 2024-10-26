import subprocess
import flet as ft
from Libs.Data.firebase_config import db
import pygetwindow as gw

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

def minimize_window(page: ft.Page):
    window = gw.getWindowsWithTitle(page.title)[0]
    window.minimize()

def create_drag_area(page: ft.Page, drawer: ft.NavigationDrawer): 
    drag_area = ft.WindowDragArea(
        ft.Container(
            content=ft.Row(
                controls=[
                    ft.Row(
                        controls=[
                            ft.IconButton(
                                ft.icons.MENU, 
                                on_click=lambda e: page.open(drawer), 
                                width=50, 
                                height=50, 
                                icon_color='White'
                            )
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ft.Row(
                        controls=[
                            ft.IconButton(
                                ft.icons.REMOVE, 
                                on_click=lambda e: minimize_window(page),
                                width=50, 
                                height=50, 
                                icon_color='White'
                            ),
                            ft.IconButton(
                                ft.icons.CLOSE, 
                                on_click=lambda e: page.window.close(), 
                                width=50, 
                                height=50, 
                                icon_color='White'
                            )
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        spacing=5
                    )
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
    from Libs.Public.menu import menu_page
    from Libs.Scripts.scripts import scripts_page
    from Libs.Migracao.migracao import migracao_page
    from Libs.Wiki.wiki import wiki_page
    from Libs.Technical.technical import technical_page
    from Libs.Movdesk.movdesk import movdesk_page
    from Config.settings import settings_page

    selected_index = e.control.selected_index

    destinations = [
        menu_page,
        scripts_page,
        wiki_page,
        technical_page,
        migracao_page,
        movdesk_page,
        settings_page
    ]

    if selected_index < len(destinations):
        page.clean()
        destinations[selected_index](page)
        show_snackbar(page, f"Navegando para {destinations[selected_index].__name__}")
    elif selected_index == 7:
        show_snackbar(page, "Saindo...")
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
                            src="./logo3.svg",
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
            ft.NavigationDrawerDestination(label="WikiSN", icon=ft.icons.PSYCHOLOGY_ALT),
            ft.NavigationDrawerDestination(label="Menu Técnico", icon=ft.icons.HANDYMAN),
            ft.NavigationDrawerDestination(label="Migração", icon=ft.icons.SYSTEM_UPDATE_ALT),
            ft.NavigationDrawerDestination(label="API Movdesk", icon=ft.icons.PUBLISHED_WITH_CHANGES),
            ft.NavigationDrawerDestination(label="Configurações", icon=ft.icons.SETTINGS_OUTLINED),
            ft.NavigationDrawerDestination(label="Sair", icon=ft.icons.LOGOUT),
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
        bgcolor="#CC8105",
        border=ft.Border(
            left=ft.BorderSide(2, "black"),
            top=ft.BorderSide(2, "black"),
            right=ft.BorderSide(2, "black"),
            bottom=ft.BorderSide(2, "black"),
        ),
        on_click=lambda e: on_folder_button_click(client_id, page),
    )

def connect_rdp_directly(rdp_ip, rdp_user, rdp_pass):
    try:
        cmdkey_command = f'cmdkey /generic:{rdp_ip} /user:{rdp_user} /pass:{rdp_pass}'
        subprocess.run(cmdkey_command, shell=True)
        
        mstsc_command = f'mstsc /v:{rdp_ip}'
        subprocess.run(mstsc_command, shell=True)

        remove_cmdkey_command = f'cmdkey /delete:{rdp_ip}'
        subprocess.run(remove_cmdkey_command, shell=True)

    except Exception as e:
        print(f"Erro ao conectar via RDP: {e}")
        return False
    
    return True

def on_folder_button_click(client_id, page):
    try:
        client_data = db.child("clientes").child(client_id).get()

        if client_data.each():
            client_info = client_data.val()
            anydesk_id = client_info.get("CONEXAO")
            password = client_info.get("SENHA")
            rdp_ip = client_info.get("RDP_IP")
            rdp_user = client_info.get("RDP_USER")
            rdp_pass = client_info.get("RDP_PASS")

            if rdp_ip and rdp_user and rdp_pass:
                if connect_rdp_directly(rdp_ip, rdp_user, rdp_pass):
                    print(f"Conectando via RDP ao IP: {rdp_ip} com o usuário: {rdp_user}")
                    return
                else:
                    show_snackbar(page, "Erro ao conectar via RDP, tentando AnyDesk...", is_error=True)

            if anydesk_id and password:
                command_anydesk = f'echo {password} | "C:\\Program Files (x86)\\AnyDesk\\AnyDesk.exe" {anydesk_id} --with-password'
                subprocess.run(command_anydesk, shell=True)
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

            cnpj_input = ft.TextField(label="CNPJ", value=client_info.get("CNPJ", ""), width=400, fill_color= '#06140f')
            nome_input = ft.TextField(label="Nome", value=client_info.get("NOME", ""), width=400, fill_color= '#06140f')
            razao_input = ft.TextField(label="Razão", value=client_info.get("RAZAO", ""), width=400, fill_color= '#06140f')
            ip_input = ft.TextField(label="IP", value=client_info.get("IP", ""), width=400, fill_color= '#06140f')
            porta_input = ft.TextField(label="Porta", value=client_info.get("PORTA", ""), width=400, fill_color= '#06140f')
            conexao_input = ft.TextField(label="Conexão", value=client_info.get("CONEXAO", ""), width=400, fill_color= '#06140f')
            senha_input = ft.TextField(label="Senha", value=client_info.get("SENHA", ""), width=400, fill_color= '#06140f')
            rdp_ip_input = ft.TextField(label="RDP IP", value=client_info.get("RDP_IP", ""), width=400, fill_color= '#06140f')
            rdp_user_input = ft.TextField(label="RDP Usuário", value=client_info.get("RDP_USER", ""), width=400, fill_color= '#06140f')
            rdp_pass_input = ft.TextField(label="RDP Senha", value=client_info.get("RDP_PASS", ""), width=400, fill_color= '#06140f')

            def save_changes(e):
                updated_data = {
                    "CNPJ": cnpj_input.value,
                    "NOME": nome_input.value,
                    "RAZAO": razao_input.value,
                    "IP": ip_input.value,
                    "PORTA": porta_input.value,
                    "CONEXAO": conexao_input.value,
                    "SENHA": senha_input.value,
                    "RDP_IP": rdp_ip_input.value,
                    "RDP_USER": rdp_user_input.value,
                    "RDP_PASS": rdp_pass_input.value
                }

                db.child("clientes").child(client_id).update(updated_data)
                show_snackbar(page, "Informações atualizadas com sucesso!", color='green')

                modal.open = False
                page.update()

            modal = ft.AlertDialog(
                content=ft.Column(
                    controls=[
                        cnpj_input, nome_input, razao_input, ip_input, porta_input,
                        conexao_input, senha_input,
                        rdp_ip_input, rdp_user_input, rdp_pass_input
                    ],
                    spacing=8
                ),
                bgcolor='#081c15',
                actions_alignment=ft.MainAxisAlignment.CENTER,
                actions=[
                    ft.TextButton("Salvar", on_click=save_changes,style=ft.ButtonStyle(bgcolor="#CC8105")),
                    ft.TextButton("Cancelar", on_click=lambda e: close_modal(modal, page),style=ft.ButtonStyle(bgcolor="#7B0000"))
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
    print(f"{action}")
