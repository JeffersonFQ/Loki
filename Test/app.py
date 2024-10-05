import flet as ft
import elevate  # Importa o elevate para elevar privilégios
import pyrebase  # Importa a biblioteca Pyrebase para interagir com o Firebase
import subprocess  # Para executar comandos no sistema
import os  # Para manipulação de arquivos e diretórios

# Configurações do Firebase
firebaseConfig = {
    'apiKey': "AIzaSyDjYwLhHAB8ZJSuFw4mmh58RKzp9tx3nVA",
    'authDomain': "loki-95d45.firebaseapp.com",
    'projectId': "loki-95d45",
    'storageBucket': "loki-95d45.appspot.com",
    'databaseURL': "https://loki-95d45-default-rtdb.firebaseio.com/",
    'messagingSenderId': "784689390439",
    'appId': "1:784689390439:web:c41456f433c5f86b9285c2",
    'measurementId': "G-18J63K96HG"
}

# Inicializa o aplicativo Firebase com as configurações
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()  # Inicializa o serviço de autenticação
db = firebase.database()  # Inicializa o serviço de banco de dados

elevate.elevate(show_console=False)  # Solicita elevação de privilégios

# Função principal que inicia o aplicativo
def main(page: ft.Page):

    login_page(page)  # Chama a função de login passando a página    
    # Configurações iniciais da página
    page.title = "Aplicativo"
    page.window_center()
    page.window.frameless = True
    page.window.bgcolor = ft.colors.BLACK  # Define a cor de fundo da janela
    page.window.title_bar_hidden = True
    page.window.width = 1150
    page.window.height = 700
    page.window.resizable = True
    page.theme_mode = 'Dark'

# Função que define a página de login
def login_page(page: ft.Page):
    page.title = "Tela de Login"
    page.window.padding = 0
    page.window.border = None
    page.window.margin = 0
    page.window.title_bar_hidden = True
    page.window.width = 1150
    page.window.height = 700
    page.window.resizable = False
    page.theme_mode = 'Dark'

    def show_snackbar(message, is_error=False, color='green'):
        bgcolor = 'red' if is_error else color
        snackbar = ft.SnackBar(
            content=ft.Text(message, color=ft.colors.WHITE),
            bgcolor=bgcolor,
            action="OK!",
            behavior=ft.SnackBarBehavior.FLOATING,
            duration=3000,
            width=400
        )
        page.snack_bar = snackbar  # Define o Snackbar na página
        page.snack_bar.open = True  # Abre o Snackbar
        page.update()

    def login(e):
        username = username_input.value
        password = password_input.value

        if username == "master" and password == "123":
            show_snackbar("Login master bem-sucedido!", is_error=False)
            page.clean()
            menu_page(page)
            return

        if not username and not password:
            username_input.border_color = ft.colors.RED
            password_input.border_color = ft.colors.RED
            page.update()
            show_snackbar("Por favor, preencha o e-mail e a senha.", is_error=True)
            return
        elif not username:
            username_input.border_color = ft.colors.RED
            page.update()
            show_snackbar("Por favor, preencha o e-mail.", is_error=True)
            return
        elif not password:
            password_input.border_color = ft.colors.RED
            page.update()
            show_snackbar("Por favor, preencha a senha.", is_error=True)
            return

        try:
            user = auth.sign_in_with_email_and_password(username, password)
            show_snackbar(f"Login bem-sucedido! Bem-vindo, {username}!", is_error=False)
            page.clean()
            menu_page(page)
        except Exception as ex:
            handle_error(str(ex))

    def register(e):
        username = username_input.value
        password = password_input.value
        
        if not username or not password:
            show_snackbar("Por favor, preencha todos os campos.", is_error=True)
            return

        try:
            auth.create_user_with_email_and_password(username, password)
            show_snackbar("Cadastro realizado com sucesso! Você pode fazer login agora.")
        except Exception as ex:
            handle_registration_error(str(ex))

    def handle_error(error_message):
        if "wrong-password" in error_message:
            show_snackbar("Senha incorreta. Tente novamente.", is_error=True)
        elif "user-not-found" in error_message:
            show_snackbar("E-mail não encontrado. Você pode se registrar.", is_error=True)
        elif "invalid-email" in error_message:
            show_snackbar("E-mail inválido. Verifique o formato.", is_error=True)
        else:
            show_snackbar("Erro ao fazer login. Tente novamente.", is_error=True)

    def handle_registration_error(error_message):
        if "email-already-in-use" in error_message:
            show_snackbar("Esse e-mail já está em uso.", is_error=True, color='yellow')
        elif "invalid-email" in error_message:
            show_snackbar("E-mail inválido. Verifique o formato.", is_error=True)
        elif "weak-password" in error_message:
            show_snackbar("A senha deve ter pelo menos 6 caracteres.", is_error=True)
        else:
            show_snackbar("Erro ao cadastrar usuário. Tente novamente.", is_error=True)

    def close_app(e):
        page.window.close()

    username_input = ft.TextField(label="E-mail", width=300, border_color=ft.colors.WHITE)
    password_input = ft.TextField(label="Senha", password=True, width=300, can_reveal_password=True, border_color=ft.colors.WHITE)
    password_input.on_submit = login
    login_button = ft.ElevatedButton("Fazer Login", on_click=login, color="#fdc43f")
    register_button = ft.ElevatedButton("Cadastrar", on_click=register, color="#fdc43f")

    logo = ft.Image(src="./Resources/logo2.svg", width=250, height=250)

    logo_container = ft.Container(content=logo, alignment=ft.Alignment(0, 0))
    username_container = ft.Container(content=username_input, alignment=ft.Alignment(0, 0))
    password_container = ft.Container(content=password_input, alignment=ft.Alignment(0, 0))
    login_button_container = ft.Container(content=login_button, alignment=ft.Alignment(0, 0))
    register_button_container = ft.Container(content=register_button, alignment=ft.Alignment(0, 0))

    drag_area = ft.WindowDragArea(
        ft.Container(
            content=ft.Row(
                controls=[ft.IconButton(ft.icons.CLOSE, on_click=close_app, icon_color=ft.colors.WHITE)],
                alignment=ft.MainAxisAlignment.END,
            ),
            bgcolor=ft.colors.TRANSPARENT,
            width=1150,
            height=50,
            padding=0
        ),
        expand=True,
        maximizable=False
    )
    
    app_container = ft.Container(
        content=ft.Column(
            controls=[
                logo_container,
                username_container,
                password_container,
                login_button_container,
                register_button_container
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=30,
        ),
        width=1150,
        height=650,
    )

    main_container = ft.Container(
        content=ft.Column(
            controls=[
                drag_area,
                app_container,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        width=1150,
        height=700,
        expand=True,
    )

    page.add(main_container)
    page.update()

# Funções do menu
def create_drag_area(page: ft.Page, open_drawer):
    drag_area = ft.WindowDragArea(
        ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(ft.icons.MENU, on_click=open_drawer, icon_color=ft.colors.WHITE),
                    ft.IconButton(ft.icons.CLOSE, on_click=lambda e: page.window.close(), icon_color=ft.colors.WHITE)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                expand=True
            ),
            bgcolor=ft.colors.TRANSPARENT,
            padding=ft.padding.all(0),
            margin=ft.Margin(left=0, right=0, top=0, bottom=0)
        ),
        expand=True
    )
    return drag_area

def go_to_login(page: ft.Page):
    page.clean()
    login_page(page)
    page.update()

def create_client_button(client_id, client_name):
    image_path = f"./Resources/Clientes/{client_name}.png"
    
    if not os.path.exists(image_path):
        image_path = "./Resources/Clientes/default.png"  # Imagem padrão

    return ft.Container(
        content=ft.Column(
            alignment=ft.MainAxisAlignment.END,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Image(src=image_path, width=100, height=100),
                    ]
                ),
                ft.Container(
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.SETTINGS,
                                on_click=lambda e: on_settings_click(e),
                                tooltip="Editar informações do cliente",
                                padding=ft.padding.only(right=0),
                            ),
                            ft.Text(client_name, color=ft.colors.BLACK, style="bodyLargeBold"),
                        ]
                    ),
                    bgcolor=ft.colors.YELLOW,
                    height=40,
                    width=200,
                ),
            ],
            spacing=0,
        ),
        width=200,
        height=150,
        bgcolor=ft.colors.WHITE,
        border_radius=ft.BorderRadius(
            top_left=20,
            top_right=20,
            bottom_left=20,
            bottom_right=20
        ),
        on_click=lambda e: on_folder_button_click(client_id),
    )

def on_folder_button_click(client_id):
    try:
        client_data = db.child("clientes").child(client_id).get()

        if client_data.each():
            client_info = client_data.val()
            anydesk_id = client_info.get("CONEXAO")
            password = client_info.get("SENHA")

            if anydesk_id and password:
                command = f'echo {password} | "C:\\Program Files (x86)\\AnyDesk\\AnyDesk.exe" {anydesk_id} --with-password'
                subprocess.run(command, shell=True)
                print(f"Conectando ao AnyDesk com ID: {anydesk_id} e senha: {password}")
            else:
                print("ID do AnyDesk ou senha não encontrados.")
                ft.snack_bar("ID do AnyDesk ou senha não encontrados.", open=True)
        else:
            print("Cliente não encontrado.")
            ft.snack_bar("Cliente não encontrado.", open=True)

    except Exception as e:
        print(f"Erro ao acessar o cliente: {e}")
        ft.snack_bar("Erro ao acessar o cliente.", open=True)

def on_settings_click(e):
    print("Ícone de engrenagem clicado!")

def menu_page(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.title = "Menu Principal"
    page.window.title_bar_hidden = True
    page.window.maximizable = False
    page.window.width = 1150
    page.window.height = 700
    page.window.resizable = False
    page.theme_mode = 'Dark'

    def handle_change(e):
        page.clean()
        selected_index = drawer.selected_index

        pages = [
            'Libs.menu_page',
            'Libs.db_function_page',
            'Libs.dashboard_page',
            'Libs.wiki_page',
            'Libs.technical_page',
            'Libs.movdesk_page',
            'Config.setting'
        ]
        
        if selected_index < len(pages):
            module = __import__(pages[selected_index], fromlist=[''])
            module.page(page)
        elif selected_index == 7:
            go_to_login(page)

        page.close(drawer)

    drag_area = create_drag_area(page, lambda e: page.open(drawer))

    drawer = ft.NavigationDrawer(
        on_change=handle_change,
        controls=[
            ft.Container(
                content=ft.Image(
                    src="./Resources/logo3.svg",
                    width=150,
                    height=150,
                    fit=ft.ImageFit.CONTAIN,
                ),
                padding=ft.padding.all(40),
                alignment=ft.alignment.center,
            ),
            ft.NavigationDrawerDestination(label="Clientes", icon=ft.icons.PEOPLE_ALT),
            ft.NavigationDrawerDestination(label="Scripts SQL", icon=ft.icons.ALL_INBOX),
            ft.NavigationDrawerDestination(label="Dashboard", icon=ft.icons.TRENDING_UP),
            ft.NavigationDrawerDestination(label="WikiSN", icon=ft.icons.BOOK_SHARP),
            ft.NavigationDrawerDestination(label="Menu Técnico", icon=ft.icons.BUILD),
            ft.NavigationDrawerDestination(label="API Movdesk", icon=ft.icons.SWAP_VERT_CIRCLE_ROUNDED),
            ft.NavigationDrawerDestination(label="Configurações", icon=ft.icons.SETTINGS_OUTLINED),
            ft.NavigationDrawerDestination(label="Sair", icon=ft.icons.EXIT_TO_APP_OUTLINED),
        ],
    )

    drawer.selected_index = 0

    main_container = ft.Container(
        content=ft.Column(
            controls=[drag_area],
            expand=True,
        ),
        padding=ft.padding.all(0),
        margin=ft.Margin(left=0, right=0, top=0, bottom=0)
    )

    search_field = ft.TextField(
        hint_text="Pesquisar clientes...",
        on_change=lambda e: update_client_list(e.control.value),
        width=400,
    )

    search_container = ft.Container(
        content=search_field,
        padding=ft.padding.all(20),
    )

    main_container.content.controls.append(search_container)

    all_clients = []
    clients_data = db.child("clientes").get()

    if clients_data.each():
        for client in clients_data.each():
            client_id = client.key()
            client_info = client.val()
            if client_info:
                client_name = client_info.get("NOME", "Cliente Desconhecido")
                button = create_client_button(client_id, client_name)
                all_clients.append((client_id, client_name, button))
                main_container.content.controls.append(button)
            else:
                print(f"Informações do cliente com ID {client_id} não encontradas.")
    else:
        print("Nenhum cliente encontrado.")

    def update_client_list(search_text):
        main_container.content.controls = [drag_area, search_container]
        filtered_clients = [button for client_id, client_name, button in all_clients if search_text.lower() in client_name.lower()]
        main_container.content.controls.extend(filtered_clients)
        page.update()

    page.add(main_container)
    page.update()

# Executa o aplicativo
ft.app(target=main)
