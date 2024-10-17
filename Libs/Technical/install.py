import os
import subprocess
from time import sleep
import gdown
import flet as ft
from threading import Thread
from Libs.Public.ui import configure_main_window
from Libs.Public.utils import create_drag_area, create_drawer

def show_snackbar(page: ft.Page, message: str, color: str):
    snackbar = ft.SnackBar(
        content=ft.Text(message, color=ft.colors.WHITE),
        bgcolor=color,
        open=True
    )
    page.snack_bar = snackbar
    page.update()

def download_installer(page, file_url, output):
    try:
        show_snackbar(page, "Baixando instalador...", color=ft.colors.BLUE)
        gdown.download(file_url, output, quiet=False)
        return True
    except Exception as e:
        show_snackbar(page, f"Erro ao baixar o instalador: {str(e)}", color=ft.colors.RED)
        return False

def install_with_progress(page, install_function, *args):
    pb = ft.ProgressBar(width=400, color="amber", bgcolor="#eeeeee", value=0)
    dialog = ft.AlertDialog(
        title=ft.Text("Instalação em progresso..."),
        content=pb,
        bgcolor='#081c15',
        actions_alignment=ft.MainAxisAlignment.CENTER
    )

    page.overlay.append(dialog)
    dialog.open = True
    page.update()

    progress_running = True  # Variável de controle para o loop de progresso

    # Função que simula um loop contínuo de progresso
    def progress_loop():
        while progress_running:
            pb.value += 0.05
            if pb.value >= 1:
                pb.value = 0
            page.update()
            sleep(0.1)  # Aumente ou diminua para controlar a velocidade do loop

    # Executa a instalação em uma thread separada
    def run_installation():
        nonlocal progress_running  # Permite alterar a variável dentro da função
        try:
            progress_thread = Thread(target=progress_loop)
            progress_thread.start()  # Inicia o loop de progresso

            # Executa a função de instalação
            install_function(page, *args)

            # Finaliza o loop de progresso
            progress_running = False
            progress_thread.join()  # Aguarda o fim do loop de progresso
            show_snackbar(page, "Instalação concluída com sucesso!", color=ft.colors.GREEN)
        except Exception as e:
            progress_running = False  # Finaliza o loop de progresso em caso de erro
            show_snackbar(page, f"Erro na instalação: {str(e)}", color=ft.colors.RED)
        finally:
            dialog.open = False  # Fecha o diálogo
            page.update()

    Thread(target=run_installation).start()

def install_java(page, version):
    if version == "32":
        file_url = "https://drive.google.com/uc?id=1d0oJ5JCtwT9aqJQGdK13QdQpFMP-wCyn"
        install_command = "Java_32_bits_installer.exe"
    else:
        file_url = "https://drive.google.com/uc?id=1EMAUXtuMXrBkfoYBo4KxydZPMVej59MX"
        install_command = "Java_64_bits_installer.exe"

    if download_installer(page, file_url, install_command):
        try:
            subprocess.run([install_command, '/s'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            show_snackbar(page, f"Java {version} bits foi instalado com sucesso!", color=ft.colors.GREEN)
        except subprocess.CalledProcessError as e:
            show_snackbar(page, f"Erro na instalação do Java {version} bits: {e.stderr.decode()}", color=ft.colors.RED)
        finally:
            if os.path.exists(install_command):
                os.remove(install_command)

def install_sql_server(page, version):
    if version == "2017":
        file_url = "https://drive.google.com/uc?id=1t9d8bOe9-n2XsC8MnnhswBG633K7-bp0"
        install_command = "SQL_Server_2017_installer.exe"
    else:
        file_url = "https://drive.google.com/uc?id=1tJMvqSvrI64pB3b4fYexfKzeAktEbYQ4"
        install_command = "SQL_Server_2019_installer.exe"

    if download_installer(page, file_url, install_command):
        try:
            subprocess.run([install_command], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            show_snackbar(page, f"SQL Server {version} foi instalado com sucesso!", color=ft.colors.GREEN)
        except subprocess.CalledProcessError as e:
            show_snackbar(page, f"Erro na instalação do SQL Server {version}: {e.stderr.decode()}", color=ft.colors.RED)
        finally:
            if os.path.exists(install_command):
                os.remove(install_command)

def install_ssms(page):
    file_url = "https://drive.google.com/uc?id=1dB0plPWXRDO-xM6jZxx7tiFjrXQrxL7-"
    install_command = "SSMS_installer.exe"

    if download_installer(page, file_url, install_command):
        try:
            subprocess.run([install_command, '/install', '/quiet', '/norestart'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            show_snackbar(page, "SQL Server Management Studio foi instalado com sucesso!", color=ft.colors.GREEN)
        except subprocess.CalledProcessError as e:
            show_snackbar(page, f"Erro na instalação do SSMS: {e.stderr.decode()}", color=ft.colors.RED)
        finally:
            if os.path.exists(install_command):
                os.remove(install_command)

def install_unimake(page):
    file_url = "https://drive.google.com/uc?id=1dQwNxSOQXi7BUZVb0LsmyfX1IGZYCSmP"
    install_command = "Unimake_installer.exe"

    if download_installer(page, file_url, install_command):
        try:
            subprocess.run([install_command, '/VERYSILENT'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            show_snackbar(page, "Unimake foi instalado com sucesso!", color=ft.colors.GREEN)
        except subprocess.CalledProcessError as e:
            show_snackbar(page, f"Erro na instalação do Unimake: {e.stderr.decode()}", color=ft.colors.RED)
        finally:
            if os.path.exists(install_command):
                os.remove(install_command)

def install_tomcat(page):
    file_url = "https://drive.google.com/uc?id=1cJ8W3Dv5vAkpPfZVoG02ekhxl9-pQqRd"
    install_command = "Tomcat_installer.exe"

    if download_installer(page, file_url, install_command):
        try:
            subprocess.run([install_command, '/S'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            show_snackbar(page, "Tomcat foi instalado com sucesso!", color=ft.colors.GREEN)
        except subprocess.CalledProcessError as e:
            show_snackbar(page, f"Erro na instalação do Tomcat: {e.stderr.decode()}", color=ft.colors.RED)
        finally:
            if os.path.exists(install_command):
                os.remove(install_command)

def configure_tomcat(page):
    server_file_path = "C:\\Program Files\\Apache Software Foundation\\Tomcat 8.0\\conf\\server.xml"
    show_snackbar(page, "Configurando o Tomcat...", color=ft.colors.BLUE)

    try:
        with open(server_file_path, 'r') as file:
            config = file.readlines()

        for i, line in enumerate(config):
            if '<Connector port="8080"' in line:
                config[i] = line.replace('8080', '7071')
                break

        for i, line in enumerate(config):
            if 'user=' in line:
                config[i] = f'    <User name="admin" password="admin"/>\n'
                break

        with open(server_file_path, 'w') as file:
            file.writelines(config)

        show_snackbar(page, "Configuração do Tomcat concluída com sucesso!", color=ft.colors.GREEN)

    except Exception as e:
        show_snackbar(page, f"Erro ao configurar o Tomcat: {str(e)}", color=ft.colors.RED)

def choose_java_version(page):
    def on_version_selected(version):
        install_with_progress(page, install_java, version)
        dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        title=ft.Text("Qual versão do java deseja instala ?"),
        actions=[
            ft.TextButton("32 Bits", on_click=lambda e: on_version_selected("32"), style=ft.ButtonStyle(bgcolor="#CC8105")),
            ft.TextButton("64 Bits", on_click=lambda e: on_version_selected("64"), style=ft.ButtonStyle(bgcolor="#CC8105")),
            ft.TextButton("Fechar", on_click=lambda e: close_dialog(page, dialog), style=ft.ButtonStyle(bgcolor="#7B0000")),
        ],
        bgcolor='#081c15',
        actions_alignment=ft.MainAxisAlignment.CENTER
    )

    page.overlay.append(dialog)
    dialog.open = True
    page.update()

def choose_sql_version(page):
    def on_version_selected(version):
        install_with_progress(page, install_sql_server, version)
        dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        title=ft.Text("Qual versão do SQL Server deseja instala?"),
        actions=[
            ft.TextButton("SQL 2017", on_click=lambda e: on_version_selected("2017"), style=ft.ButtonStyle(bgcolor="#CC8105")),
            ft.TextButton("SQL 2019", on_click=lambda e: on_version_selected("2019"), style=ft.ButtonStyle(bgcolor="#CC8105")),
            ft.TextButton("Fechar", on_click=lambda e: close_dialog(page, dialog), style=ft.ButtonStyle(bgcolor="#7B0000")),
        ],
        bgcolor='#081c15',
        actions_alignment=ft.MainAxisAlignment.CENTER
    )

    page.overlay.append(dialog)
    dialog.open = True
    page.update()

def close_dialog(page, dialog):
    dialog.open = False
    page.update()

def install_page(page: ft.Page):
    configure_main_window(page)
    page.title = "Menu Instalação"
    page.window.title_bar_hidden = True
    page.window.maximizable = False
    page.window.resizable = False
    page.theme_mode = 'Dark'

    drawer = create_drawer(page)
    drawer.selected_index = 4

    drag_area = create_drag_area(page, drawer)

    icon_size = 200
    icons_with_labels = [
        (ft.icons.COFFEE, "Instalar Java", lambda e: choose_java_version(page), ft.colors.RED),
        (ft.icons.ALL_INBOX, "Instalar SQL Server", lambda e: choose_sql_version(page), ft.colors.BLUE),
        (ft.icons.MANAGE_SEARCH_OUTLINED, "Instalar SSMS", lambda e: install_ssms(page), ft.colors.PURPLE),
        (ft.icons.ARTICLE, "Instalar Unimake", lambda e: install_unimake(page), ft.colors.YELLOW),
        (ft.icons.BROADCAST_ON_HOME, "Instalar Tomcat", lambda e: install_tomcat(page), ft.colors.BROWN),
        (ft.icons.BROADCAST_ON_HOME, "Configurar Tomcat", lambda e: configure_tomcat(page), ft.colors.CYAN),
    ]

    rows = []
    for i in range(0, len(icons_with_labels), 3):
        columns = []
        for icon, label, on_click, color in icons_with_labels[i:i + 3]:
            column = ft.Column(
                controls=[
                    ft.IconButton(
                        icon,
                        tooltip=label,
                        on_click=on_click,
                        icon_size=icon_size,
                        style=ft.ButtonStyle(
                            icon_color='#CC8105'
                        )
                    ),
                    ft.Text(label, text_align=ft.TextAlign.CENTER, size=18)
                ],
                spacing=0,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
            columns.append(column)

        row = ft.Row(
            spacing=20,
            controls=columns,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
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

def go_to_technical_page(page):
    from Libs.Technical.technical import technical_page
    page.clean()
    technical_page(page)
    page.update()