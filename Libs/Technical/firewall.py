import flet as ft
import os, requests, subprocess, locale, socket, pyperclip
from Libs.Public.ui import configure_main_window
from Libs.Public.utils import create_drag_area, create_drawer, show_snackbar

def firewall_page(page: ft.Page):
    configure_main_window(page)
    page.title = "Menu Windows"
    page.window.title_bar_hidden = True
    page.window.maximizable = False
    page.window.resizable = False
    page.theme_mode = 'Dark'

    drawer = create_drawer(page)
    drawer.selected_index = 4

    drag_area = create_drag_area(page, drawer)

    icon_size = 80
    text_size = 16
    spacing = 8

    icons_with_labels = [
        (ft.icons.DESCRIPTION, "Abrir porta SQL (1433)", lambda e: sql_port_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Abrir porta Tomcat (7071)", lambda e: tomcat_port_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Tornar rede atual Privada", lambda e: rede_priv_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Ativar Firewall", lambda e: firewall_on_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Desativar Firewall", lambda e: firewall_off_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Alterar Hostname", lambda e: edit_host_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Verificar IP Externo", lambda e: ver_ipexterno_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Verificar IP Interno", lambda e: ver_ipinterno_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Verificar Hostname", lambda e: ver_host_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Remover pastas compartilhadas", lambda e: del_comp_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Compartilhar pastas SN", lambda e: comp_sn_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Verificar Pastas Compartilhadas", lambda e: ver_comp_sn_conf(page), '#CC8105'),
    ]

    num_columns = 3
    rows = []
    for i in range(0, len(icons_with_labels), num_columns):
        columns = []
        for icon, label, on_click, color in icons_with_labels[i:i + num_columns]:
            column = ft.Column(
                controls=[
                    ft.IconButton(
                        icon,
                        tooltip=label,
                        on_click=on_click,
                        icon_size=icon_size,
                        style=ft.ButtonStyle(
                            icon_color=color
                        )
                    ),
                    ft.Text(label, text_align=ft.TextAlign.CENTER, size=text_size)
                ],
                spacing=spacing,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            )
            columns.append(column)

        row = ft.Row(
            spacing=20,
            controls=columns,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        rows.append(row)

    icons_container = ft.Column(
        controls=rows,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    back_button = ft.TextButton(
        text="Voltar",
        on_click=lambda e: go_to_technical_page(page),
        style=ft.ButtonStyle(
            bgcolor="#7B0000",
            color=ft.colors.WHITE,
            padding=ft.padding.symmetric(horizontal=20, vertical=12)
        ),
    )

    main_container = ft.Container(
        content=ft.Column(
            controls=[
                drag_area,
                ft.Row(
                    controls=[back_button],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
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

def sql_port_conf(page):
    command_in = 'netsh advfirewall firewall add rule name="SQL Server IN" protocol=TCP dir=in localport=1433 action=allow'
    result_in = os.system(command_in)

    command_out = 'netsh advfirewall firewall add rule name="SQL Server OUT" protocol=TCP dir=out localport=1433 action=allow'
    result_out = os.system(command_out)

    if result_in == 0 and result_out == 0:
        show_snackbar(page, "Portas SQL (1433) de entrada e saída abertas com sucesso!", is_error=False)
    else:
        show_snackbar(page, "Erro ao abrir as portas SQL.", is_error=True)

def tomcat_port_conf(page):
    command_in = 'netsh advfirewall firewall add rule name="Tomcat IN" protocol=TCP dir=in localport=7071 action=allow'
    result_in = os.system(command_in)

    command_out = 'netsh advfirewall firewall add rule name="Tomcat OUT" protocol=TCP dir=out localport=7071 action=allow'
    result_out = os.system(command_out)

    if result_in == 0 and result_out == 0:
        show_snackbar(page, "Portas Tomcat (7071) de entrada e saída abertas com sucesso!", is_error=False)
    else:
        show_snackbar(page, "Erro ao abrir as portas Tomcat.", is_error=True)

def del_comp_conf(page):
    shared_folders = [
        "Compilados","Imagens","Integracao","Interface","Nfe","S7","Unimake","Users"
    ]

    for folder in shared_folders:
        try:
            command = f"Remove-SmbShare -Name \"{folder}\" -Force"
            subprocess.run(["powershell", "-Command", command], check=True)
            show_snackbar(page, f"Compartilhamento da pasta '{folder}' removido com sucesso.", is_error=False)
        except subprocess.CalledProcessError as e:
            show_snackbar(page, f"Erro ao remover o compartilhamento da pasta '{folder}': {e}", is_error=True)

def rede_priv_conf(page):
    command = 'powershell -Command "Set-NetConnectionProfile -NetworkCategory Private"'
    result = os.system(command)
    if result == 0:
        show_snackbar(page, "Rede configurada como privada.", is_error=False)
    else:
        show_snackbar(page, "Erro ao configurar a rede.", is_error=True)

def firewall_on_conf(page):
    command = 'netsh advfirewall set allprofiles state on'
    result = os.system(command)
    if result == 0:
        show_snackbar(page, "Firewall ativado com sucesso.", is_error=False)
    else:
        show_snackbar(page, "Erro ao ativar o firewall.", is_error=True)

def firewall_off_conf(page):
    command = 'netsh advfirewall set allprofiles state off'
    result = os.system(command)
    if result == 0:
        show_snackbar(page, "Firewall desativado com sucesso.", is_error=False)
    else:
        show_snackbar(page, "Erro ao desativar o firewall.", is_error=True)

def edit_host_conf(page):
    def confirm_new_name(e):
        new_name = host_input.value
        if new_name:
            try:
                subprocess.run(f'wmic computersystem where name="%computername%" rename "{new_name}"', shell=True)
                show_snackbar(page, "Nome do host alterado com sucesso!", is_error=False)
                page.dialog.close()
            except Exception as e:
                show_snackbar(page, f"Erro ao alterar o nome do host: {str(e)}", is_error=True)
        else:
            show_snackbar(page, "Nome inválido!", is_error=True)

    host_input = ft.TextField(label="Novo nome do Host")
    dialog = ft.AlertDialog(
        title=ft.Text("Alterar Hostname"),
        content=host_input,
        actions=[
            ft.TextButton("Confirmar", on_click=confirm_new_name),
            ft.TextButton("Cancelar", on_click=lambda e: close_dialog(page, dialog))
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.overlay.append(dialog)
    dialog.open = True
    page.update()

def open_ip_dialog(page, ip_address, title):
    """Abre um diálogo mostrando o IP e permitindo copiar."""
    def copiar_conteudo(e):
        pyperclip.copy(ip_address)
        show_snackbar(page, "Conteúdo copiado para a área de transferência.", is_error=False)

    dialog = ft.AlertDialog(
        title=ft.Text(title),
        content=ft.Text(f"IP: {ip_address}"),
        actions=[
            ft.TextButton("Copiar IP", on_click=copiar_conteudo),
            ft.TextButton("Fechar", on_click=lambda e: close_dialog(page, dialog))
        ]
    )
    
    page.overlay.append(dialog)
    dialog.open = True
    page.update()

def close_dialog(page, dialog):
    """Fecha o diálogo."""
    dialog.open = False
    page.update()

def ver_ipinterno_conf(page):
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

        if ip_address.startswith("127."):
            show_snackbar(page, "Erro: IP interno não encontrado.", is_error=True)
            return

        result = subprocess.run(['ping', '-n', '1', ip_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            open_ip_dialog(page, ip_address, "IP Interno")
        else:
            show_snackbar(page, "Erro: IP interno não encontrado.", is_error=True)

    except Exception as e:
        show_snackbar(page, f"Erro ao verificar o IP interno: {str(e)}", is_error=True)

def ver_ipexterno_conf(page):
    try:
        response = requests.get('https://ipinfo.io/json')
        response.raise_for_status()
        ip_externo = response.json()["ip"]

        if ':' not in ip_externo:
            open_ip_dialog(page, ip_externo, "IP Externo")
        else:
            show_snackbar(page, "Erro: IP externo não é do tipo IPv4.", is_error=True)

    except Exception as e:
        show_snackbar(page, "Erro ao obter o IP externo.", is_error=True)

def comp_sn_conf(page):
    try:
        current_language = locale.getdefaultlocale()[0]
        if current_language.startswith("pt"):
            access_group = "Todos"
        else:
            access_group = "Everyone"

        os.system(f'net share S7="C:\\S7" /grant:{access_group},FULL')
        os.system(f'net share Compilados="C:\\S7\\Compilados" /grant:{access_group},FULL')
        os.system(f'net share Imagens="C:\\S7\\Imagens" /grant:{access_group},FULL')
        os.system(f'net share Interface="C:\\S7\\Interface" /grant:{access_group},FULL')
        os.system(f'net share Nfe="C:\\S7\\Nfe" /grant:{access_group},FULL')
        os.system(f'net share Unimake="C:\\Unimake" /grant:{access_group},FULL')

        show_snackbar(page, "Pastas compartilhadas com sucesso!", is_error=False)
    except Exception as e:
        show_snackbar(page, f"Erro ao compartilhar pastas: {str(e)}", is_error=True)

def ver_comp_sn_conf(page):
    shared_folders = os.popen('net share').readlines()

    filtered_folders = []
    for line in shared_folders:
        if not any(shared_name in line for shared_name in ["ADMIN$", "C$", "J$", "IPC$", "Comando concluído com êxito.", "Nome", "----"]):
            filtered_folders.append(line.strip())

    content_text = "\n".join(filtered_folders) if filtered_folders else "Nenhuma pasta compartilhada encontrada."

    dialog = ft.AlertDialog(
        title=ft.Text("Pastas Compartilhadas"),
        content=ft.Text(content_text),
        actions=[
            ft.TextButton("Fechar", on_click=lambda e: close_dialog(page, dialog))
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.overlay.append(dialog)
    dialog.open = True
    page.update()

def ver_host_conf(page):
    try:
        hostname = os.popen('hostname').read().strip()
        show_snackbar(page, f"Hostname atual: {hostname}", is_error=False)
    except Exception as e:
        show_snackbar(page, "Erro ao verificar o Hostname.", is_error=True)

def close_dialog(page, dialog):
    dialog.open = False
    page.update()

def go_to_technical_page(page):
    from Libs.Technical.technical import technical_page
    page.clean()
    technical_page(page)
    page.update()
