import flet as ft
import pygetwindow as gw

def configure_main_window(page: ft.Page):
    page.window.icon = "./icon.ico"
    page.bgcolor='#081c15'
    page.title = "Aplicativo"
    page.window.max_height = 700
    page.window.max_width = 1150
    page.window.frameless = True
    page.window.title_bar_hidden = True
    page.window.width = 1150
    page.window.height = 700
    page.window.resizable = False
    page.theme_mode = 'Dark'

def video_inicial():
    return ft.Video(
        expand=True,
        playlist=[ft.VideoMedia("./assets/SvgAnimation.mp4")],
        autoplay=True,
        filter_quality='HIGH',
        show_controls=False,
        aspect_ratio='16/9'
    )

def login_page(page: ft.Page):
    from Libs.Data.auth import login
    page.title = "Tela de Login"
    page.window.padding = 0
    page.window.border = None
    page.window.margin = 0
    page.window.title_bar_hidden = True
    page.window.width = 1150
    page.window.height = 700
    page.window.resizable = False
    page.theme_mode = 'Dark'

    def minimize_window(e):
        window = gw.getWindowsWithTitle(page.title)[0]
        window.minimize()

    drag_area = ft.WindowDragArea(
        ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.MINIMIZE,
                        on_click=minimize_window,
                        width=50,
                        height=50,
                        icon_color='White'
                    ),
                    ft.IconButton(
                        icon=ft.icons.CLOSE,
                        on_click=lambda e: page.window.close(),
                        width=50,
                        height=50,
                        icon_color='White'
                    )
                ],
                alignment=ft.MainAxisAlignment.END,
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

    username_input = ft.TextField(
        label="E-mail", 
        width=300, 
        border_color=ft.colors.WHITE,
        on_submit=lambda e: password_input.focus()
    )

    password_input = ft.TextField(
        label="Senha", 
        password=True, 
        width=300, 
        can_reveal_password=True, 
        border_color=ft.colors.WHITE,
        on_submit=lambda e: login(username_input.value, password_input.value, page)
    )
    
    login_button = ft.ElevatedButton(
        "Fazer Login", 
        on_click=lambda e: login(username_input.value, password_input.value, page),
        bgcolor="#CC8105",
        color="#081c15"
    )

    logo = ft.Image(
        src="./logo3.svg",
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