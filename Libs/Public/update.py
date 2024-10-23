import asyncio
import requests
import subprocess
import sys
import flet as ft
from packaging import version

def verificar_nova_versao(usuario, repositorio, versao_atual, token_github):
    url = f"https://api.github.com/repos/{usuario}/{repositorio}/releases/latest"
    headers = {"Authorization": f"token {token_github}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        ultima_versao = response.json()["tag_name"]
        if version.parse(ultima_versao) > version.parse(versao_atual):
            return response.json()["zipball_url"], ultima_versao
    return None, versao_atual

def perguntar_se_atualizar(page: ft.Page, url_atualizacao, nova_versao):
    def confirmar_atualizacao(e):
        subprocess.Popen([sys.executable, "atualizador.py", url_atualizacao])
        page.window_close()

    def cancelar_atualizacao(e):
        dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(f"Nova versão {nova_versao} disponível!"),
        content=ft.Text("Deseja atualizar agora?"),
        actions=[
            ft.TextButton("Atualizar", on_click=confirmar_atualizacao),
            ft.TextButton("Cancelar", on_click=cancelar_atualizacao),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    page.overlay.append(dialog)
    dialog.open = True
    page.update()

async def iniciar_atualizacao(page: ft.Page):
    versao_atual = "v1.0.0"
    usuario_github = "JeffersonFQ"
    repositorio_github = "Loki"
    token_github = "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"

    url_atualizacao, nova_versao = verificar_nova_versao(usuario_github, repositorio_github, versao_atual, token_github)
    
    if url_atualizacao:
        perguntar_se_atualizar(page, url_atualizacao, nova_versao)
    
    await asyncio.sleep(6)

