import platform, subprocess, webbrowser, socket, requests, psutil, pyodbc
import flet as ft
from Libs.Public.ui import configure_main_window
from Libs.Data.sql_server_config import initialize_sql_server
from Libs.Public.utils import create_drag_area, create_drawer, show_snackbar

def analytics_page(page: ft.Page):
    configure_main_window(page)
    page.title = "Menu Windows"
    page.window.title_bar_hidden = True
    page.window.maximizable = False
    page.window.resizable = False
    page.theme_mode = 'Dark'

    drawer = create_drawer(page)
    drawer.selected_index = 3

    drag_area = create_drag_area(page, drawer)

    icon_size = 80 
    text_size = 16
    spacing = 8

    icons_with_labels = [
        (ft.icons.DESCRIPTION, "Verificar Empresas da Base", lambda e: empresa_ver(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Verificar Usuario/Senha", lambda e: pessoa_ver(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Verificar Versão ERP", lambda e: versao_erp_ver(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Verificar Versão Java", lambda e: java_ver(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Verificar Status Sefaz", lambda e: sefaz_ver(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Verificar abertura de Porta", lambda e: openport_ver(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Verificar Odin", lambda e: odin_ver(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Verificar configurações completas", lambda e: all_config_ver(page), '#CC8105'),
    ]

    num_columns = 3
    rows = []
    for i in range(0, len(icons_with_labels), num_columns):
        columns = []
        for icon, label, on_click, color in icons_with_labels[i:i + num_columns]:
            column = ft.Column(
                controls=[
                    ft.IconButton(
                        icon,
                        tooltip=label,
                        on_click=on_click,
                        icon_size=icon_size,
                        style=ft.ButtonStyle(
                            icon_color=color
                        )
                    ),
                    ft.Text(label, text_align=ft.TextAlign.CENTER, size=text_size)
                ],
                spacing=spacing,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            )
            columns.append(column)

        row = ft.Row(
            spacing=20,
            controls=columns,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        rows.append(row)

    icons_container = ft.Column(
        controls=rows,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    back_button = ft.TextButton(
        text="Voltar",
        on_click=lambda e: go_to_technical_page(page),
        style=ft.ButtonStyle(
            bgcolor="#7B0000",
            color=ft.colors.WHITE,
            padding=ft.padding.symmetric(horizontal=20, vertical=12)
        ),
    )

    main_container = ft.Container(
        content=ft.Column(
            controls=[
                drag_area,
                ft.Row(
                    controls=[back_button],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(content=icons_container, margin=ft.Margin(left=60, top=18, right=60, bottom=0))
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=ft.padding.all(0),
        margin=ft.Margin(left=0, right=0, top=0, bottom=0),
    )

    page.add(main_container)
    page.update()

def empresa_ver(page):
    conn = initialize_sql_server()

    if conn is None:
        dialog = ft.AlertDialog(
            title=ft.Text("Erro de Conexão"),
            content=ft.Text("Não foi possível conectar ao banco de dados."),
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()
        return

    cursor = conn.cursor()
    query = "SELECT CODIGO, RAZAOSOCIAL, CNPJ FROM EMPRESA"
    
    try:
        cursor.execute(query)
        dados = cursor.fetchall()

        colunas = [
            ft.DataColumn(ft.Text("Código")),
            ft.DataColumn(ft.Text("Razão Social")),
            ft.DataColumn(ft.Text("CNPJ"))
        ]

        linhas = []
        for row in dados:
            linhas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(row.CODIGO))),
                        ft.DataCell(ft.Text(row.RAZAOSOCIAL)),
                        ft.DataCell(ft.Text(row.CNPJ))
                    ]
                )
            )

        dialog = ft.AlertDialog(
            title=ft.Text("Dados da Empresa"),
            content=ft.DataTable(
                columns=colunas,
                rows=linhas,
            ),
            on_dismiss=lambda e: print("Diálogo fechado.")
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    except Exception as e:
        dialog = ft.AlertDialog(
            title=ft.Text("Erro ao Consultar"),
            content=ft.Text(f"Ocorreu um erro ao consultar a tabela: {str(e)}"),
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    finally:
        cursor.close()
        conn.close()

def pessoa_ver(page):
    conn = initialize_sql_server()

    if conn is None:
        dialog = ft.AlertDialog(
            title=ft.Text("Erro de Conexão"),
            content=ft.Text("Não foi possível conectar ao banco de dados."),
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()
        return

    cursor = conn.cursor()
    query = """SELECT CODIGO, NOME, USUARIO, SENHA FROM PESSOA 
            WHERE USUARIO IS NOT NULL AND SENHA IS NOT NULL AND CODIGO NOT IN (1 ,3, 20000)
        """
    
    try:
        cursor.execute(query)
        dados = cursor.fetchall()

        colunas = [
            ft.DataColumn(ft.Text("Código")),
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Usuário")),
            ft.DataColumn(ft.Text("Senha"))
        ]

        linhas = []
        for row in dados:
            linhas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(row.CODIGO))),
                        ft.DataCell(ft.Text(row.NOME)),
                        ft.DataCell(ft.Text(row.USUARIO)),
                        ft.DataCell(ft.Text(row.SENHA))
                    ]
                )
            )

        dialog = ft.AlertDialog(
            title=ft.Text("Dados da Empresa"),
            content=ft.DataTable(
                columns=colunas,
                rows=linhas,
            ),
            on_dismiss=lambda e: print("Diálogo fechado.")
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    except Exception as e:
        dialog = ft.AlertDialog(
            title=ft.Text("Erro ao Consultar"),
            content=ft.Text(f"Ocorreu um erro ao consultar a tabela: {str(e)}"),
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    finally:
        cursor.close()
        conn.close()

def versao_erp_ver(page):
    conn = initialize_sql_server()

    if conn is None:
        dialog = ft.AlertDialog(
            title=ft.Text("Erro de Conexão"),
            content=ft.Text("Não foi possível conectar ao banco de dados."),
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()
        return

    cursor = conn.cursor()
    query = """
        SELECT TOP 1 ID, NOMECOMPUTADOR, VERSAOERP 
        FROM VERSAOSISTEMA 
        ORDER BY ID DESC
    """

    try:
        cursor.execute(query)
        dados = cursor.fetchone()

        if dados is None:
            dialog = ft.AlertDialog(
                title=ft.Text("Nenhum dado encontrado"),
                content=ft.Text("A tabela VERSAOSISTEMA está vazia."),
            )
            page.overlay.append(dialog)
            dialog.open = True
            page.update()
            return

        colunas = [
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nome Computador")),
            ft.DataColumn(ft.Text("Versão ERP"))
        ]

        linha = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(str(dados.ID))),
                ft.DataCell(ft.Text(dados.NOMECOMPUTADOR)),
                ft.DataCell(ft.Text(dados.VERSAOERP))
            ]
        )

        dialog = ft.AlertDialog(
            title=ft.Text("Última Versão no SQL"),
            content=ft.DataTable(
                columns=colunas,
                rows=[linha],
            ),
            on_dismiss=lambda e: print("Diálogo fechado.")
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    except Exception as e:
        dialog = ft.AlertDialog(
            title=ft.Text("Erro ao Consultar"),
            content=ft.Text(f"Ocorreu um erro ao consultar a tabela: {str(e)}"),
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    finally:
        cursor.close()
        conn.close()

def java_ver(page):
    try:
        resultado = subprocess.run(["java", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if resultado.returncode != 0:
            dialog = ft.AlertDialog(
                title=ft.Text("Erro"),
                content=ft.Text("Java não está instalado ou não está no PATH."),
            )
            page.overlay.append(dialog)
            dialog.open = True
            page.update()
            return

        primeira_linha = resultado.stderr.splitlines()[0]

        arquitetura = platform.architecture()[0]
        arquitetura_texto = "64 bits" if arquitetura == "64bit" else "32 bits"

        dialog = ft.AlertDialog(
            title=ft.Text("Versão do Java"),
            content=ft.Text(f"{primeira_linha}\nArquitetura: {arquitetura_texto}"),
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    except Exception as e:
        dialog = ft.AlertDialog(
            title=ft.Text("Erro"),
            content=ft.Text(f"Ocorreu um erro ao verificar a versão do Java: {str(e)}"),
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

def sefaz_ver(page):
    try:
        webbrowser.open("https://www.nfe.fazenda.gov.br/portal/disponibilidade.aspx?versao=4.00")
    except Exception as e:
        show_snackbar(page, f"Erro ao acessar o link", is_error=True)

def openport_ver(page):
    def obter_ip_publico():
        try:
            response = requests.get("https://httpbin.org/ip")
            return response.json().get("origin")
        except Exception as e:
            return f"Erro ao obter IP público: {str(e)}"

    def check_port(ip: str, porta: int):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        try:
            resultado = sock.connect_ex((ip, porta))
            return resultado == 0
        except Exception as e:
            return f"Erro ao verificar: {str(e)}"
        finally:
            sock.close()

    ip_local = obter_ip_publico()

    ip_field = ft.TextField(label="Endereço IP", value=ip_local)
    porta_field = ft.TextField(label="Porta", value="80", keyboard_type=ft.KeyboardType.NUMBER)

    def verificar(e):
        try:
            porta = int(porta_field.value)
            ip = ip_field.value
            is_open = check_port(ip, porta)

            if isinstance(is_open, bool):
                status = "ABERTA" if is_open else "FECHADA"
                mensagem = f"A porta {porta} no endereço {ip} está {status}."
            else:
                mensagem = is_open
            resultado_dialog = ft.AlertDialog(
                title=ft.Text("Verificação de Porta"),
                content=ft.Text(mensagem),
            )

            page.overlay.append(resultado_dialog)
            resultado_dialog.open = True
            page.update()
        except ValueError:
            show_snackbar(page, "Por favor, insira um número válido para a porta.",is_error=True)

    dialog = ft.AlertDialog(
        title=ft.Text("Verificar Porta"),
        content=ft.Column(controls=[ip_field, porta_field]),
        actions=[
            ft.TextButton("Verificar", on_click=verificar),
            ft.TextButton("Cancelar", on_click=lambda e: close_dialog(page, dialog)),
        ],
    )

    page.overlay.append(dialog)
    dialog.open = True
    page.update()

def odin_ver(page):
    url = "http://snsistemas.ddns.net:6060/"

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            show_snackbar(page ,f"Odin está no ar!", is_error=False)
        else:
            show_snackbar(page ,f"Odin retornou o status: {response.status_code}", is_error=True)
    except requests.ConnectionError:
        show_snackbar(page ,f"Odin está fora do ar ou inacessível.", is_error=True)
    except requests.Timeout:
        show_snackbar(page ,f"O tempo de resposta do Odin foi excedido.", is_error=True)
    except Exception as e:
        show_snackbar(page ,f"Ocorreu um erro: {str(e)}", is_error=True)

def all_config_ver(page):
    nome_maquina = socket.gethostname()

    def verificar_portas_firewall(portas):
        status = {}
        for porta in portas:
            result = subprocess.run(f'netsh advfirewall firewall show rule name=all | findstr {porta}', 
                                    capture_output=True, text=True, shell=True)
            status[porta] = "sim" if str(porta) in result.stdout else "não"
        return status

    portas_status = verificar_portas_firewall([7071, 1433])

    def verificar_pastas_compartilhadas(pastas):
        status = {}
        for pasta in pastas:
            result = subprocess.run(f'net share | findstr "{pasta}"', capture_output=True, text=True, shell=True)
            status[pasta] = "sim" if pasta in result.stdout else "não"
        return status

    pastas = ['C/S7', 'C/S7/INTERFACE', 'C/S7/IMAGENS', 'C/S7/COMPILADOS', 'C/UNIMAKE', 'C/S7/NFE']
    pastas_status = verificar_pastas_compartilhadas(pastas)

    def verificar_sql_server_ativo():
        return "sim" if any(proc.info['name'] and 'sqlservr' in proc.info['name'].lower() 
                            for proc in psutil.process_iter(['pid', 'name'])) else "não"

    sql_server_ativo = verificar_sql_server_ativo()

    def verificar_base_sql(nome_base):
        try:
            with pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=master;Trusted_Connection=yes;') as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"SELECT name FROM sys.databases WHERE name = '{nome_base}'")
                    return "sim" if cursor.fetchone() else "não"
        except Exception as e:
            return f"erro: {e}"

    base_aa_existe = verificar_base_sql('base_aa')

    status_text = f"Nome da máquina: {nome_maquina}\n" \
                  f"Porta 7071 aberta: {portas_status[7071]}\n" \
                  f"Porta 1433 aberta: {portas_status[1433]}\n" \
                  f"SQL Server ativo: {sql_server_ativo}\n" \
                  f"Base 'base_aa' existe: {base_aa_existe}\n" \
                  f"Pastas compartilhadas:\n" + "\n".join(f"  - {pasta}: {status}" for pasta, status in pastas_status.items())

    dialog = ft.AlertDialog(
        title=ft.Text("Verificação de Sistema"),
        content=ft.Text(status_text),
        on_dismiss=lambda e: close_dialog(page, dialog)
    )
    page.dialog = dialog
    page.dialog.open = True
    page.update()


def close_dialog(page, dialog):
    dialog.open = False
    page.update()

def go_to_technical_page(page):
    from Libs.Technical.technical import technical_page
    page.clean()
    technical_page(page)
    page.update()