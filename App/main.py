import flet as ft
import asyncio
import elevate
from Libs.Data.firebase_config import initialize_firebase
from Libs.Public.ui import login_page, configure_main_window

initialize_firebase()

# elevate.elevate(show_console=False)
video_duration = 5

video = ft.Video(
    expand=True,
    playlist=[
        ft.VideoMedia("./Resources/SvgAnimation.mp4")
    ],
    autoplay=True,
    filter_quality='HIGH',
    show_controls=False,
    aspect_ratio='16/9'
)

async def main(page: ft.Page):
    page.window.center()
    configure_main_window(page)
    page.window.width = 1145
    page.add(video)
   
    await asyncio.sleep(6)

    page.controls.clear()
    configure_main_window(page)
    login_page(page)
    page.update()

ft.app(target=main)
