import flet as ft
import subprocess, re, os, webbrowser
from Libs.Public.ui import configure_main_window
from Libs.Public.utils import create_drag_area, create_drawer, show_snackbar


def ferramentas_page(page: ft.Page):
    configure_main_window(page)
    page.title = "Menu Windows"
    page.window.title_bar_hidden = True
    page.window.maximizable = False
    page.window.resizable = False
    page.theme_mode = 'Dark'

    drawer = create_drawer(page)
    drawer.selected_index = 3

    drag_area = create_drag_area(page, drawer)

    icon_size = 80
    text_size = 16
    spacing = 8

    icons_with_labels = [
        (ft.icons.DESCRIPTION, "Resetar Anydesk", lambda e: anydesk_reroll(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Reiniciar SQL", lambda e: restart_sql(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Dispositivos na rede", lambda e: dispositivos_rede(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Abrir pasta S7", lambda e: open_s7(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Abrir pasta WebApps", lambda e: open_webapps(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Abrir Mega - Compilados", lambda e: open_mega_compilados(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Abrir Mega - Manuais", lambda e: open_mega_manuais(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Abrir Drive - Compilados", lambda e: open_drive(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Ativar o Windows", lambda e: windows_activate(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Reiniciar Maquina", lambda e: reload_win(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Reiniciar Agendado", lambda e: temp_reload_win(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Desligar agendado", lambda e: temp_off_win(page), '#CC8105'),
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

def anydesk_reroll(page):
    def on_confirm(e):
        try:
            fechar_comando = 'powershell -Command "Stop-Process -Name AnyDesk -Force"'
            subprocess.run(fechar_comando, shell=True)

            programdata_anydesk = os.path.join(os.environ['PROGRAMDATA'], 'AnyDesk')

            service_conf = os.path.join(programdata_anydesk, 'service.conf')
            system_conf = os.path.join(programdata_anydesk, 'system.conf')

            if os.path.exists(service_conf):
                os.remove(service_conf)

            if os.path.exists(system_conf):
                os.remove(system_conf)

            close_dialog(page, dialog)
            show_snackbar(page, "AnyDesk encerrado e arquivos apagados.", is_error=False)
        except Exception as ex:
            show_snackbar(page, f"Erro: {str(ex)}", is_error=True)

    dialog = ft.AlertDialog(
        title=ft.Text("Encerrar AnyDesk e Apagar Configurações"),
        content=ft.Text("Você tem certeza que deseja encerrar o AnyDesk e apagar os arquivos de configuração?"),
        actions=[
            ft.TextButton("Sim", on_click=on_confirm),
            ft.TextButton("Não", on_click=lambda e: close_dialog(page, dialog)),
        ]
    )

    page.overlay.append(dialog)
    dialog.open = True
    page.update()

def restart_sql(page):
    def on_reiniciar_sql(e):
        try:
            comando = 'powershell -Command "Restart-Service -Name MSSQLSERVER"'
            subprocess.run(comando, shell=True)
            close_dialog(page, dialog)
            show_snackbar(page, "SQL Server reiniciado com sucesso.", is_error=False)
        except Exception as e:
            show_snackbar(page, f"Erro ao reiniciar SQL Server: {str(e)}", is_error=True)

    dialog = ft.AlertDialog(
        title=ft.Text("Reiniciar SQL Server"),
        content=ft.Text("Você tem certeza que deseja reiniciar o banco de dados SQL Server?"),
        actions=[
            ft.TextButton("Sim", on_click=on_reiniciar_sql),
            ft.TextButton("Não", on_click=lambda e: close_dialog(page, dialog)),
        ]
    )

    page.overlay.append(dialog)
    dialog.open = True
    page.update()

def dispositivos_rede(page):
    try:
        result = subprocess.run(['arp', '-a'], capture_output=True, text=True)

        if result.returncode == 0:
            devices = []
            pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+)\s+([^\s]+)\s+([^\s]+)')

            for line in result.stdout.splitlines():
                match = pattern.search(line)
                if match:
                    ip = match.group(1)
                    mac = match.group(2)
                    devices.append(f"IP: {ip}, MAC: {mac}")

            if devices:
                device_list = "\n".join(devices)
                dialog_content = f"Dispositivos encontrados:\n{device_list}"
            else:
                dialog_content = "Nenhum dispositivo encontrado."
        else:
            dialog_content = f"Erro ao executar o comando arp:\n{result.stderr}"

    except Exception as e:
        dialog_content = f"Ocorreu um erro: {e}"

    dialog = ft.AlertDialog(
        title=ft.Text("Dispositivos na Rede"),
        content=ft.Text(dialog_content),
        actions=[ft.ElevatedButton("Fechar", on_click=lambda e: close_dialog(page, dialog))],
    )
    
    page.overlay.append(dialog)
    dialog.open = True
    page.update()

def open_s7(page):
    try:
        subprocess.Popen(f'explorer "C:\\S7"')
    except Exception as e:
        show_snackbar(page, f"Erro ao abrir a pasta", is_error=True)

def open_webapps(page):
    try:
        caminhos_possiveis = [
            r"C:\Program Files\Apache Software Foundation\Tomcat 8.0",
            r"C:\Program Files (x86)\Apache Software Foundation\Tomcat 8.0"
        ]
        
        for caminho in caminhos_possiveis:
            if os.path.exists(caminho):
                subprocess.Popen(f'explorer "{caminho}"')
                return

        show_snackbar(page, "Tomcat não encontrado em Program Files ou Program Files (x86)", is_error=True)
    
    except Exception as e:
        show_snackbar(page, f"Erro ao abrir a pasta: {str(e)}", is_error=True)

def open_mega_compilados(page):
    try:
        webbrowser.open("https://mega.nz/folder/CpU13a7R#hUoabwV39gkk5-rC2LsgFg/folder/Ll1RkJqC")
    except Exception as e:
        show_snackbar(page, f"Erro ao acessar o link", is_error=True)

def open_mega_manuais(page):
    try:
        webbrowser.open("https://mega.nz/folder/CpU13a7R#hUoabwV39gkk5-rC2LsgFg/folder/z98l2S6C")
    except Exception as e:
        show_snackbar(page, f"Erro ao acessar o link", is_error=True)

def open_drive(page):
    try:
        webbrowser.open("https://drive.google.com/drive/folders/1-1YC9b2JawuWnsKIXFzxgwILtFMgow2q?usp=drive_link")
    except Exception as e:
        show_snackbar(page, f"Erro ao acessar o link", is_error=True)

def windows_activate(page):
    try:
        comando_powershell = 'irm https://massgrave.dev/get | iex'

        comando = f'powershell -Command "Start-Process PowerShell -ArgumentList \'-NoProfile -ExecutionPolicy Bypass -Command {comando_powershell}\' -Verb RunAs"'

        subprocess.run(comando, shell=True)
    
    except Exception as e:
        show_snackbar(page, f"Erro ao executar o comando no PowerShell: {str(e)}", is_error=True)

def reload_win(page):
    def on_reiniciar(e):
        try:
            subprocess.run('shutdown -r -t 0', shell=True)
            close_dialog(page, dialog)
            show_snackbar(page, "Reiniciando o computador...", is_error=False)
        except Exception as e:
            show_snackbar(page, f"Erro ao reiniciar: {str(e)}", is_error=True)

    dialog = ft.AlertDialog(
        title=ft.Text("Você tem certeza que deseja reiniciar o computador?"),
        actions=[
            ft.TextButton("Sim", on_click=on_reiniciar),
            ft.TextButton("Não", on_click=lambda e: close_dialog(page, dialog)),
        ]
    )

    page.overlay.append(dialog)
    dialog.open = True
    page.update()

def temp_reload_win(page):
    def on_confirm(e):
        try:
            tempo = int(text_field.value)
            if tempo <= 0:
                page.add(ft.SnackBar(ft.Text("Por favor, insira um número positivo.", size="large"), is_error=True))
                return

            comando = f'shutdown -r -t {tempo * 60}'

            subprocess.run(f'powershell -Command "{comando}"', shell=True)

            close_dialog(page, dialog)
            show_snackbar(page, f"Reinício agendado em {tempo} minutos.", is_error=False)
        except ValueError:
            show_snackbar(page, "Por favor, insira um número válido.", is_error=True)

    text_field = ft.TextField(label="Minutos para reiniciar", keyboard_type="number")

    dialog = ft.AlertDialog(
        title=ft.Text("Agendar Reinício"),
        content=text_field,
        actions=[
            ft.TextButton("Confirmar", on_click=on_confirm),
            ft.TextButton("Cancelar", on_click=lambda e: close_dialog(page, dialog)),
        ]
    )

    page.overlay.append(dialog)
    dialog.open = True
    page.update()

def temp_off_win(page):
    def on_confirm(e):
        try:
            tempo = int(text_field.value)
            if tempo <= 0:
                page.add(ft.SnackBar(ft.Text("Por favor, insira um número positivo.", size="large"), is_error=True))
                return

            comando = f'shutdown -s -t {tempo * 60}'

            subprocess.run(f'powershell -Command "{comando}"', shell=True)

            close_dialog(page, dialog)
            show_snackbar(page, f"Desligamento agendado em {tempo} minutos.", is_error=False)
        except ValueError:
            show_snackbar(page, "Por favor, insira um número válido.", is_error=True)

    text_field = ft.TextField(label="Minutos para desligar", keyboard_type="number")

    dialog = ft.AlertDialog(
        title=ft.Text("Agendar Desligamento"),
        content=text_field,
        actions=[
            ft.TextButton("Confirmar", on_click=on_confirm),
            ft.TextButton("Cancelar", on_click=lambda e: close_dialog(page, dialog)),
        ]
    )

    page.overlay.append(dialog)
    dialog.open = True
    page.update()

def close_dialog(page, dialog):
    dialog.open = False
    page.update()

def go_to_technical_page(page):
    from Libs.Technical.technical import technical_page
    page.clean()
    technical_page(page)
    page.update()
