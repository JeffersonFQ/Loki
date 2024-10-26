import psutil, os, time, threading, subprocess, shutil,elevate, urllib.request
from datetime import datetime
from pystray import Icon, MenuItem as Item, Menu
from PIL import Image

# flet pack .\Fenrir.py --icon .\assets\icon3.ico --add-data "assets;assets"
elevate.elevate(show_console=False)

ICON_PATH = r"C:\Users\jeffe\Documents\Mega Pessoal\Loki\assets\icon3.png"
SOFTWARE_NAME = r"C:\Unimake\UniNFe\uninfe.exe"
POTENTIAL_FOLDERS = [r"C:\Program Files\Apache Software Foundation\Tomcat 8.0\webapps",
                    r"C:\Program Files (x86)\Apache Software Foundation\Tomcat 8.0\webapps"]
PERMITTED_FOLDERS = {"docs", "manager", "ROOT", "host-manager",
                      "ServicoS7", "snsistemasb2b-api", "ServicoCheckout",
                        "ServicoGE", "Roteirizador"}
PERMITTED_FILES = {"ServicoS7.war", "snsistemasb2b-api.war", "ServicoCheckout.war",
                   "ServicoGE.war", "Roteirizador.war"}
LOG_FILE = r"C:\Program Files\Loki\logs\monitor_log.txt"
ANYDESK_PATHS = ["C:\\Program Files\\AnyDesk\\AnyDesk.exe",
                "C:\\Program Files (x86)\\AnyDesk\\AnyDesk.exe"]
ANYDESK_URL = "https://download.anydesk.com/AnyDesk.exe"
DOWNLOAD_ANY_PATH = "C:\\Temp\\AnyDesk.exe"

def check_any():
    installed = False
    for path in ANYDESK_PATHS:
        if os.path.exists(path):
            installed = True
            anydesk_path = path
            break

    if not installed:
        print("AnyDesk não encontrado. Baixando...")
        urllib.request.urlretrieve(ANYDESK_URL, DOWNLOAD_ANY_PATH)
        print("Instalando AnyDesk...")
        subprocess.run([DOWNLOAD_ANY_PATH, '/install'], shell=True)
        anydesk_path = ANYDESK_PATHS[0]

    new_password = "snremoto7"
    command = f'echo {new_password} | "{anydesk_path}" --set-password _full_access'
    subprocess.run(command, shell=True)
    print("Senha do AnyDesk definida com sucesso.")

    for process in psutil.process_iter(['name']):
        if process.info['name'] == 'AnyDesk.exe':
            print("AnyDesk já está em execução.")
            return True

    print("AnyDesk não está em execução. Iniciando...")
    subprocess.Popen([anydesk_path])
    return False

def log_event(event_message):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{event_message}\n")
    return event_message

def check_and_run_software():
    global software_closed_count
    running = any(proc.name().lower() == os.path.basename(SOFTWARE_NAME).lower() for proc in psutil.process_iter())
    if not running:
        try:
            subprocess.Popen([SOFTWARE_NAME])
            print(f"{datetime.now()} - {SOFTWARE_NAME} foi iniciado.")
        except Exception as e:
            print(f"Erro ao tentar iniciar o software: {e}")
        else:
            software_closed_count += 1

def clean_folders():
    global files_deleted_count
    for folder in POTENTIAL_FOLDERS:
        if os.path.exists(folder):
            for root, dirs, files in os.walk(folder, topdown=False):
                if any(root.startswith(os.path.join(folder, allowed_folder)) for allowed_folder in PERMITTED_FOLDERS):
                    continue

                for name in files:
                    if not any(name.startswith(permitted) for permitted in PERMITTED_FILES):
                        file_path = os.path.join(root, name)
                        try:
                            os.remove(file_path)
                            files_deleted_count += 1
                            log_event(f"{datetime.now()} - Arquivo removido: {file_path}")
                            print(f"Arquivo removido: {file_path}")
                        except Exception as e:
                            print(f"Erro ao tentar remover {file_path}: {e}")

                for name in dirs:
                    dir_path = os.path.join(root, name)
                    if not any(name.startswith(permitted) for permitted in PERMITTED_FOLDERS):
                        try:
                            shutil.rmtree(dir_path)
                            log_event(f"{datetime.now()} - Diretório removido: {dir_path}")
                            print(f"Diretório removido: {dir_path}")
                        except Exception as e:
                            print(f"Erro ao tentar remover {dir_path}: {e}")
                    else:
                        dirs.remove(name)

def monitor_loop():
    while True:
        check_any()
        check_and_run_software()
        clean_folders()
        time.sleep(600)

def quit_tray(icon, item):
    icon.stop()
    os._exit(0)

def criar_tarefa_agendada():
    tarefa_nome = "Fenrir"

    caminho_executavel = r"C:\Program Files\Loki\Fenrir.exe"

    caminho_script = os.path.abspath(__file__)

    verificar_tarefa = f'schtasks /query /tn "{tarefa_nome}"'

    try:
        subprocess.run(verificar_tarefa, shell=True, check=True)
        print(f"Tarefa '{tarefa_nome}' já existe. Não será criada novamente.")
        return
    except subprocess.CalledProcessError:
        pass

    comando = f'schtasks /create /tn "{tarefa_nome}" /tr "{caminho_executavel}" /sc onlogon /rl highest /f'

    try:
        subprocess.run(comando, shell=True, check=True)
        print(f"Tarefa agendada '{tarefa_nome}' criada com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao criar a tarefa: {e}")

def setup_tray():
    criar_tarefa_agendada()

    if os.path.exists(ICON_PATH):
        image = Image.open(ICON_PATH)
        icon = Icon("Monitor Software", image, title="Fenrir", menu=Menu(Item("Sair", quit_tray)))

        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
        
        icon.run()
    else:
        print("O caminho do ícone não foi encontrado.")

if __name__ == "__main__":
    setup_tray()
