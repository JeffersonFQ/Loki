import flet as ft
from Libs.Public.utils import create_drag_area

def configure_main_window(page: ft.Page):
    page.bgcolor='#081c15'
    page.title = "Aplicativo"
    page.window.max_height = 700
    page.window.max_width = 1150
    page.window.center()
    page.window.frameless = True
    page.window.title_bar_hidden = True
    page.window.width = 1150
    page.window.height = 700
    page.window.resizable = False
    page.theme_mode = 'Dark'

def login_page(page: ft.Page):
    from Libs.Data.auth import login, register
    page.title = "Tela de Login"
    page.window.padding = 0
    page.window.border = None
    page.window.margin = 0
    page.window.title_bar_hidden = True
    page.window.width = 1150
    page.window.height = 700
    page.window.resizable = False
    page.theme_mode = 'Dark'

    drag_area = create_drag_area(page, None)

    username_input = ft.TextField(label="E-mail", width=300, border_color=ft.colors.WHITE)
    password_input = ft.TextField(label="Senha", password=True, width=300, can_reveal_password=True, border_color=ft.colors.WHITE)
    
    login_button = ft.ElevatedButton("Fazer Login", on_click=lambda e: login(username_input.value, password_input.value, page), color="#CC8105")
    register_button = ft.ElevatedButton("Cadastrar", on_click=lambda e: register(username_input.value, password_input.value, page), color="#CC8105")

    logo = ft.Image(
        src="../Resources/logo2.svg",
        width=280,
        height=280,
        fit=ft.ImageFit.CONTAIN
    )    

    app_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(content=logo, alignment=ft.Alignment(0, 0)),
                ft.Container(content=username_input, alignment=ft.Alignment(0, 0)),
                ft.Container(content=password_input, alignment=ft.Alignment(0, 0)),
                ft.Container(content=login_button, alignment=ft.Alignment(0, 0)),
                ft.Container(content=register_button, alignment=ft.Alignment(0, 0))
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=30,
        ),
        width=1150,
        height=650,
    )

    page.add(drag_area)
    page.add(app_container)
    page.update()

def go_to_login(page: ft.Page):
    page.clean()
    login_page(page)
    page.update()