import flet as ft
import elevate
from Libs.Data.firebase_config import initialize_firebase
from Libs.Public.ui import login_page, configure_main_window,video_inicial
from Libs.Public.update import iniciar_atualizacao

# flet pack .\main.py --icon .\assets\icon.ico --add-data "assets\SvgAnimation.mp4;assets" --add-data "Libs;Libs" --copyright "© 2024 J Queiroz. Todos os direitos reservados." --product-name "Loki" --product-version "1.0.0" --icon ./assets/icon.ico
# pyinstaller --onefile --noconsole --add-data "assets:assets" --icon="C:\Users\jeffe\Documents\Mega Pessoal\Loki\App\assets\icon.ico" main.py
# elevate.elevate(show_console=False)

initialize_firebase()

async def main(page: ft.Page):
    page.window.center()
    configure_main_window(page)
    page.window.width = 1145
    page.add(video_inicial())  # Adiciona o vídeo de forma simples
    
    # Verifica e lida com a atualização
    await iniciar_atualizacao(page)
    
    page.controls.clear()
    configure_main_window(page)
    login_page(page)
    page.update()

ft.app(target=main)
