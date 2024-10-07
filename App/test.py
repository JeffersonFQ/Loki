import os
import subprocess
import gdown
import flet as ft

def create_drag_area(page: ft.Page, close_app, go_back):
    return ft.WindowDragArea(
        ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(ft.icons.ARROW_BACK, on_click=go_back, icon_color=ft.colors.WHITE),
                    ft.IconButton(ft.icons.CLOSE, on_click=close_app, icon_color=ft.colors.WHITE)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                expand=True
            ),
            bgcolor=ft.colors.TRANSPARENT,
            height=40
        ),
        expand=False
    )

def show_snackbar(page: ft.Page, message: str, color: str):
    snackbar = ft.SnackBar(
        content=ft.Text(message, color=ft.colors.WHITE),
        bgcolor=color,
        open=True
    )
    page.snack_bar = snackbar
    page.update()

def close_dialog(page: ft.Page, dialog: ft.AlertDialog):
    dialog.open = False
    page.update()

def download_installer(page, file_url, output):
    try:
        show_snackbar(page, "Baixando instalador...", color=ft.colors.BLUE)
        gdown.download(file_url, output, quiet=False)
        return True
    except Exception as e:
        show_snackbar(page, f"Erro ao baixar o instalador: {str(e)}", color=ft.colors.RED)
        return False

def install_java(page, version):
    close_dialog()
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
    close_dialog()
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
    file_url = "https://drive.google.com/uc?id=1tB0plPWXRDO-xM6jZxx7tiFjrXQrxL7-"
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

def install_page(page: ft.Page):
    page.clean()

    def close_app(e):
        page.window.close()

    def go_back(e):
        from Libs import technical_page
        page.clean()
        page.update()
        technical_page(page)

    button_width, button_height = 200, 60

    def choose_java(e):
        dialog = ft.AlertDialog(
            title=ft.Text("Escolha a versão do Java"),
            content=ft.Column([
                ft.ElevatedButton("Java 32 bits", on_click=lambda e: install_java(page, "32")),
                ft.ElevatedButton("Java 64 bits", on_click=lambda e: install_java(page, "64")),
            ]),
            actions=[ft.TextButton("Fechar", on_click=lambda e: close_dialog(page, dialog))],
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def choose_sql(e):
        dialog = ft.AlertDialog(
            title=ft.Text("Escolha a versão do SQL Server"),
            content=ft.Column([
                ft.ElevatedButton("SQL Server 2017", on_click=lambda e: install_sql_server(page, "2017")),
                ft.ElevatedButton("SQL Server 2019", on_click=lambda e: install_sql_server(page, "2019")),
            ]),
            actions=[ft.TextButton("Fechar", on_click=lambda e: close_dialog(page, dialog))],
            modal=False
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    buttons = [
        ft.Container(ft.ElevatedButton("Escolher Java", on_click=choose_java), width=button_width, height=button_height),
        ft.Container(ft.ElevatedButton("Escolher SQL Server", on_click=choose_sql), width=button_width, height=button_height),
        ft.Container(ft.ElevatedButton("Instalar SSMS", on_click=install_ssms), width=button_width, height=button_height),
        ft.Container(ft.ElevatedButton("Instalar Unimake", on_click=install_unimake), width=button_width, height=button_height),
        ft.Container(ft.ElevatedButton("Instalar Tomcat", on_click=install_tomcat), width=button_width, height=button_height),
        ft.Container(ft.ElevatedButton("Configurar Tomcat", on_click=lambda e: configure_tomcat(page)), width=button_width, height=button_height)
    ]

    button_rows = [
        ft.Row(controls=buttons[:2], alignment=ft.MainAxisAlignment.CENTER, spacing  = 80),
        ft.Row(controls=buttons[2:4], alignment=ft.MainAxisAlignment.CENTER, spacing  = 80),
        ft.Row(controls=[buttons[4], buttons[5]], alignment=ft.MainAxisAlignment.CENTER, spacing  = 80)
    ]

    button_container = ft.Container(
        content=ft.Column(
            controls=button_rows,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=60,
        ),
        width=860,
        height=350,
        bgcolor=ft.colors.TRANSPARENT,
        margin=ft.padding.only(top=10, bottom=200)
    )

    drag_area = create_drag_area(page, close_app, go_back)

    main_container = ft.Container(
        content=ft.Column(
            controls=[drag_area, button_container],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        ),
        padding=0,
        margin=0
    )

    page.add(main_container)
    page.update()

def main(page: ft.Page):
    page.window.width = 400
    page.window.height = 600
    page.window.resizable = False
    page.bgcolor = ft.colors.BLACK
    page.update()
    install_page(page)

if __name__ == "__main__":
    ft.app(target=main)
