import flet as ft
import elevate
from Libs.Data.firebase_config import initialize_firebase
from Libs.Public.ui import login_page, configure_main_window


# Inicializa o Firebase
initialize_firebase()

# Eleva permissões (descomente se necessário)
# elevate.elevate(show_console=False)

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = "TheEthicalVideo"
    page.window.always_on_top = True
    page.spacing = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Adiciona o player de vídeo
    video = ft.Video(
        expand=True,
        playlist=[
            ft.VideoMedia("./Resources/SvgAnimation.mp4")
        ],
        autoplay=True,
    )

    page.add(video)
    page.add(ft.Column())  # Pode adicionar um espaço vazio para manter o layout
    page.update()  # Atualiza a página para mostrar o vídeo

    # Configura a página de login
    login_page(page)

# Executa a aplicação
ft.app(target=main)
