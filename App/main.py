import flet as ft
import elevate
from Libs.Data.firebase_config import initialize_firebase
from Libs.Public.ui import login_page, configure_main_window

initialize_firebase()

# elevate.elevate(show_console=False)

def main(page: ft.Page):
    configure_main_window(page)
    login_page(page)


ft.app(target=main)