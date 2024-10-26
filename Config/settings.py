import flet as ft
import json
import subprocess
from pathlib import Path
from Libs.Public.ui import configure_main_window, go_to_login
from Libs.Public.utils import create_drag_area, create_drawer

CONFIG_FILE = Path("config.json")
LOG_FILE = Path("monitor_log.txt")

def load_config():
    if CONFIG_FILE.is_file():
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    else:
        return {
            "monitor_folder": "Caminho/para/a/pasta",
            "permitted_files": ["ServicoS7.war"],
            "software_closed_count": 0,
            "files_deleted_count": 0
        }

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def log_event(event_message):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{event_message}\n")

def start_monitor():
    subprocess.Popen(["python", "monitor_secundario.py"])

def handle_change(e, page: ft.Page):
    from Libs.Public.menu import menu_page
    from Libs.Scripts.scripts import scripts_page
    from Libs.Migracao.migracao import migracao_page
    from Libs.Wiki.wiki import wiki_page
    from Libs.Technical.technical import technical_page
    from Libs.Movdesk.movdesk import movdesk_page
    selected_index = e.control.selected_index

    page.clean()

    page_map = {
        0: menu_page,
        1: scripts_page,
        2: wiki_page,
        3: technical_page,
        4: migracao_page,
        5: movdesk_page,
        6: settings_page
    }

    if selected_index in page_map:
        page_map[selected_index](page)
    elif selected_index == 7:
        go_to_login(page)

    page.close(e.control)

def settings_page(page: ft.Page):
    configure_main_window(page)
    page.title = "Configurações"
    page.window.title_bar_hidden = True
    page.window.maximizable = False
    page.window.resizable = False
    page.theme_mode = 'Dark'

    drawer = create_drawer(page)
    drawer.selected_index = 6
    drawer.on_change = lambda e: handle_change(e, page)

    drag_area = create_drag_area(page, drawer)

    config = load_config()

    monitor_folder = ft.TextField(label="Pasta a Monitorar", value=config["monitor_folder"], width=300)
    permitted_files = ft.TextField(label="Arquivos Permitidos", value=", ".join(config["permitted_files"]), width=300)

    software_closed_count = ft.Text(f"Software fechado: {config['software_closed_count']}")
    files_deleted_count = ft.Text(f"Arquivos deletados: {config['files_deleted_count']}")

    def save_settings(e):
        config["monitor_folder"] = monitor_folder.value
        config["permitted_files"] = [f.strip() for f in permitted_files.value.split(",")]
        save_config(config)
        page.snack_bar = ft.SnackBar(ft.Text("Configurações salvas!"), open=True)
        page.update()

    def start_monitoring(e):
        start_monitor()
        page.snack_bar = ft.SnackBar(ft.Text("Monitoramento iniciado!"), open=True)
        page.update()

    main_container = ft.Container(
        content=ft.Column(
            controls=[
                drag_area,
                ft.Text("Configurações do Monitor", style="headlineMedium"),
                monitor_folder,
                permitted_files,
                software_closed_count,
                files_deleted_count,
                ft.Row([
                    ft.ElevatedButton("Salvar Configurações", on_click=save_settings),
                    ft.ElevatedButton("Iniciar Monitoramento", on_click=start_monitoring)
                ]),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=ft.padding.all(20),
    )

    page.add(main_container)
    page.update()
