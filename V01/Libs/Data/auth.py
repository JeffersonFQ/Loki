from Libs.Data.firebase_config import auth
from Libs.Public.utils import show_snackbar
from Libs.Public.menu import menu_page

MASTER_USERNAME = ""
MASTER_PASSWORD = ""

def login(username, password, page):

    if username == MASTER_USERNAME and password == MASTER_PASSWORD:
        show_snackbar(page, "Bem-Vindo Mestre! Vamos começar!")
        page.clean()
        menu_page(page)
        return

    try:
        user = auth.sign_in_with_email_and_password(username, password)
        show_snackbar(page, f"Login bem-sucedido! Bem-vindo, {username}!")
        page.clean()
        menu_page(page)
    except Exception as ex:
        handle_error(ex, page)

def register(username, password, page):
    try:
        auth.create_user_with_email_and_password(username, password)
        show_snackbar(page, "Cadastro realizado com sucesso! Você pode fazer login agora.")
    except Exception as ex:
        handle_registration_error(ex, page)

def handle_error(error, page):
    message = {
        "wrong-password": "Senha incorreta. Tente novamente.",
        "user-not-found": "E-mail não encontrado. Você pode se registrar.",
        "invalid-email": "E-mail inválido. Verifique o formato."
    }.get(error.args[0], "Erro ao fazer login. Tente novamente.")
    
    show_snackbar(page, message, is_error=True)

def handle_registration_error(error, page):
    message = {
        "email-already-in-use": "Esse e-mail já está em uso.",
        "invalid-email": "E-mail inválido. Verifique o formato.",
        "weak-password": "A senha deve ter pelo menos 6 caracteres."
    }.get(error.args[0], "Erro ao cadastrar usuário. Tente novamente.")

    show_snackbar(page, message, is_error=True)

