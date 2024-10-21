import requests, elevate, zipfile, shutil, subprocess, sys, io, os
import flet as ft

elevate.elevate(show_console=False)

usuario_github = "JeffersonFQ"
repositorio_github = "Loki"
seu_token_github = "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"

# Função para buscar a última versão da release no GitHub
def obter_url_ultima_release(usuario, repositorio, token_github):
    url_api = f"https://api.github.com/repos/{usuario}/{repositorio}/releases/latest"
    headers = {"Authorization": f"token {token_github}"}

    response = requests.get(url_api, headers=headers)
    
    if response.status_code == 200:
        dados_release = response.json()
        url_zip = dados_release["zipball_url"]
        versao = dados_release["tag_name"]
        return url_zip, versao
    else:
        raise Exception(f"Erro ao buscar a última release: {response.status_code}")

# Função para baixar e extrair a atualização
def baixar_atualizacao(url_zip, pasta_destino, page, progress_bar, texto_status, nome_executavel="main.exe"):
    try:
        headers = {"Authorization": f"token {seu_token_github}"}
        response = requests.get(url_zip, headers=headers, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0

        if response.status_code == 200:
            # Abre um arquivo em memória
            zip_file_data = io.BytesIO()

            # Download com atualização da barra de progresso
            for data in response.iter_content(chunk_size=1024):
                zip_file_data.write(data)
                downloaded_size += len(data)

                # Atualiza o progresso
                progress_percentage = downloaded_size / total_size if total_size > 0 else 0
                progress_bar.value = progress_percentage
                texto_status.value = f"Baixando atualização... {int(progress_percentage * 100)}%"
                page.update()  # Atualiza a interface

            # Extrai os arquivos do ZIP
            with zipfile.ZipFile(zip_file_data) as zip_file:
                arquivos_extraidos = zip_file.namelist()
                total_arquivos = len(arquivos_extraidos)

                for i, arquivo in enumerate(arquivos_extraidos, 1):
                    # Verifica se o arquivo atual não é o `atualizador.py`
                    if "atualizador.py" not in arquivo:
                        zip_file.extract(arquivo, pasta_destino)

                    # Atualiza o progresso para a extração
                    progress_bar.value = (i / total_arquivos)
                    texto_status.value = f"Extraindo arquivos... {int((i / total_arquivos) * 100)}%"
                    page.update()  # Atualiza a interface

                # Procura o executável na pasta extraída (incluindo subpastas)
                for arquivo in arquivos_extraidos:
                    if arquivo.endswith(nome_executavel):
                        novo_executavel_path = os.path.join(pasta_destino, arquivo)
                        texto_status.value = f"Atualização concluída."
                        page.update()  # Atualiza a interface
                        return novo_executavel_path

            texto_status.value = f"Erro: O executável {nome_executavel} não foi encontrado após a extração."
            page.update()
            return None
        else:
            texto_status.value = f"Erro ao baixar a atualização. Código de status: {response.status_code}"
            page.update()
            return None
    except Exception as e:
        texto_status.value = f"Ocorreu um erro: {str(e)}"
        page.update()
        return None

# Função para substituir os arquivos antigos pelos novos, exceto o `atualizador.py`
def substituir_arquivos(pasta_destino):
    try:
        # Caminho do diretório atual da aplicação
        caminho_atual = os.getcwd()

        # Copia todos os arquivos da pasta_destino para o diretório da aplicação, exceto o `atualizador.py`
        for raiz, dirs, arquivos in os.walk(pasta_destino):
            for arquivo in arquivos:
                if arquivo != "atualizador.py":  # Ignora o arquivo de atualização
                    caminho_origem = os.path.join(raiz, arquivo)
                    caminho_destino = os.path.join(caminho_atual, os.path.relpath(caminho_origem, pasta_destino))
                    os.makedirs(os.path.dirname(caminho_destino), exist_ok=True)
                    shutil.move(caminho_origem, caminho_destino)

        # Remove a pasta da atualização
        if os.path.exists(pasta_destino):
            shutil.rmtree(pasta_destino)

    except Exception as e:
        print(f"Ocorreu um erro ao substituir os arquivos: {str(e)}")

def main(page: ft.Page):
    # Pega a última release do GitHub
    try:
        url_atualizacao, versao_nova = obter_url_ultima_release(usuario_github, repositorio_github, seu_token_github)
        print(f"Baixando versão: {versao_nova}")
    except Exception as e:
        print(f"Erro ao buscar a última versão: {str(e)}")
        return

    # Define uma pasta temporária para extração
    pasta_destino = os.path.join(os.getcwd(), "temp_atualizacao")
    os.makedirs(pasta_destino, exist_ok=True)

    # Configura a janela de progresso
    page.window_width = 400
    page.window_height = 200
    page.window_center()
    page.title = "Atualização em andamento"

    texto_status = ft.Text("Iniciando atualização...")
    progress_bar = ft.ProgressBar(width=400, value=0)
    
    page.add(
        ft.Column(
            [
                ft.Text("Atualizando o aplicativo", size=20, weight="bold"),
                texto_status,
                progress_bar,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )
    
    page.update()

    # Inicia o processo de download e extração
    novo_executavel = baixar_atualizacao(url_atualizacao, pasta_destino, page, progress_bar, texto_status)
    
    if novo_executavel:
        # Substitui todos os arquivos, exceto o `atualizador.py`
        substituir_arquivos(pasta_destino)
        
        # Adiciona um botão para fechar e iniciar o aplicativo
        def iniciar_aplicativo(e):
            subprocess.Popen([sys.executable, "Loki.exe", url_atualizacao])
            page.window_close()

        btn_iniciar = ft.ElevatedButton(text="Iniciar Aplicativo", on_click=iniciar_aplicativo)
        page.add(btn_iniciar)
        page.update()

# Executa o script do Flet
ft.app(target=main)
