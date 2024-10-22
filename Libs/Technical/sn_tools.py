import flet as ft
import os, webbrowser, requests, socket, subprocess
import xml.etree.ElementTree as ET
from Libs.Data.firebase_config import db
from Libs.Data.sql_server_config import initialize_sql_server
from Libs.Public.ui import configure_main_window
from Libs.Public.utils import create_drag_area, create_drawer, show_snackbar
from Libs.Technical.compatibilidades import compatibilidade_versoes_fv,compatibilidade_versoes_checkout,compatibilidade_versoes_ge

def sn_tools_page(page: ft.Page):
    configure_main_window(page)
    page.title = "Menu Windows"
    page.window.title_bar_hidden = True
    page.window.maximizable = False
    page.window.resizable = False
    page.theme_mode = 'Dark'

    drawer = create_drawer(page)
    drawer.selected_index = 4

    drag_area = create_drag_area(page, drawer)

    icon_size = 80
    text_size = 16
    spacing = 8

    icons_with_labels = [
        (ft.icons.DESCRIPTION, "Verificar APIs no servidor", lambda e: ver_api_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Verificar IP do cliente", lambda e: ver_ip_serv_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Verificar comunicação Tomcat local", lambda e: ver_tomcat_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Conferir Versão FV", lambda e: ver_fv_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Conferir Versão Gestor", lambda e: ver_ge_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Conferir Versão Checkout", lambda e: ver_checkout_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Configurar Config", lambda e: config_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Configurar Config_compilado", lambda e: configcompilado_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Configurar Agendador", lambda e: agendador_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Abrir Tomcat e Unimake", lambda e: open_apps_conf(page), '#CC8105'),  
        (ft.icons.DESCRIPTION, "Fechar Janelas S7", lambda e: close_s7_conf(page), '#CC8105'),
        (ft.icons.DESCRIPTION, "Revogar 1 acesso", lambda e: kill_old_conf(page), '#CC8105'),
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

def ver_api_conf(page):
    # Caminhos para as pastas possíveis do Tomcat
    paths_to_check = [
        r'C:\Program Files\Apache Software Foundation\Tomcat 8.0\webapps',
        r'C:\Program Files (x86)\Apache Software Foundation\Tomcat 8.0\webapps'
    ]
    
    tomcat_webapps_path = None
    
    # Verificar se o Tomcat existe em alguma das pastas
    for path in paths_to_check:
        if os.path.exists(path):
            tomcat_webapps_path = path
            break
    
    if tomcat_webapps_path is None:
        # Exibir snackbar informando que o Tomcat não foi encontrado
        page.add(ft.SnackBar(ft.Text("O Tomcat não foi encontrado em 'Program Files' nem em 'Program Files (x86)'.", size="large"), is_error=True))
        page.update()
        return
    
    # Criação do conteúdo a ser exibido no diálogo
    arquivos_conteudo = []
    for item in os.listdir(tomcat_webapps_path):
        item_path = os.path.join(tomcat_webapps_path, item)
        if os.path.isfile(item_path) and item.endswith('.war'):
            arquivos_conteudo.append(ft.Text(f"API ->  {item}", size=16))
    
    # Verificar se há arquivos .war encontrados
    if not arquivos_conteudo:
        arquivos_conteudo.append(ft.Text("Nenhum arquivo .war encontrado no diretório.", size=16, color="red"))
    
    # Exibir o diálogo com a lista de arquivos .war ou mensagem de ausência
    dialog = ft.AlertDialog(
        title=ft.Text(f"Conteúdo da pasta '{tomcat_webapps_path}':", size=20, weight="bold"),
        content=ft.Column(arquivos_conteudo, scroll=ft.ScrollMode.AUTO),
        actions=[
            ft.TextButton("Fechar", on_click=lambda e: close_dialog(page, dialog))
        ],
    )
    
    # Adicionar o diálogo à página e exibir
    page.overlay.append(dialog)
    dialog.open = True
    page.update()

def ver_fv_conf(page):
    def on_confirm_fv(e):
        try:
            nome_ou_razao = text_field.value.strip()
            if not nome_ou_razao:
                show_snackbar(page, "Por favor, insira um nome ou razão social.", is_error=True)
                return

            # Busca os clientes que correspondem ao nome ou razão social
            clientes_filtrados = []
            clientes_data = db.child("clientes").get()
            for cliente in clientes_data.each():
                if (cliente.val().get("NOME") and nome_ou_razao.lower() in cliente.val().get("NOME").lower()) or \
                   (cliente.val().get("RAZAO") and nome_ou_razao.lower() in cliente.val().get("RAZAO").lower()):
                    clientes_filtrados.append(cliente)

            if not clientes_filtrados:
                show_snackbar(page, "Nenhum cliente encontrado com esse nome ou razão social.", is_error=True)
                return
            
            # Criação do ListView com os clientes filtrados
            client_items = []
            for cliente in clientes_filtrados:
                item = ft.ListTile(
                    title=ft.Text(cliente.val().get("NOME", ""), size=16),
                    subtitle=ft.Text(cliente.val().get("RAZAO", ""), size=14),
                    on_click=lambda e, client=cliente: on_client_select(client)
                )
                client_items.append(item)

            list_view = ft.ListView(
                controls=client_items,
                auto_scroll=True
            )

            dialog = ft.AlertDialog(
                title=ft.Text("Selecione um Cliente"),
                content=list_view,
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda e: close_dialog(page, dialog))
                ]
            )

            page.overlay.append(dialog)
            dialog.open = True
            page.update()

        except Exception as ex:
            print(f"Ocorreu um erro: {str(ex)}")  # Exibindo erro no console do VS
            show_snackbar(page, f"Ocorreu um erro: {str(ex)}", is_error=True)

    def on_client_select(cliente):
        ip = cliente.val().get("IP")
        porta = cliente.val().get("PORTA")
        url = f"http://{ip}:{porta}/ServicoS7/ServiceTesterResource/versaoWebService"
        
        try:
            # Fazendo a requisição para a URL e capturando a resposta
            response = requests.get(url)
            response.raise_for_status()  # Lança um erro se a resposta não for 200
            versao_api = response.text.strip()  # Captura o valor da versão

            # Fechar o diálogo atual
            close_dialog(page, dialog)

            # Verificar a compatibilidade da versão
            if versao_api in compatibilidade_versoes_fv:
                versao_erp = compatibilidade_versoes_fv[versao_api]["ERP"]
                versao_fv = compatibilidade_versoes_fv[versao_api]["FV"]
                texto_resultado = f"Versão API: {versao_api}\nVersões ERP compatíveis: {versao_erp}\nVersões FV compatíveis: {versao_fv}"
            else:
                texto_resultado = f"Versão API: {versao_api}\nCompatibilidade desconhecida."

            # Criar um novo diálogo para exibir o resultado
            result_dialog = ft.AlertDialog(
                title=ft.Text("Resultado da Requisição"),
                content=ft.Text(texto_resultado, size=16),
                actions=[
                    ft.TextButton("Fechar", on_click=lambda e: close_dialog(page, result_dialog))
                ]
            )

            page.overlay.append(result_dialog)
            result_dialog.open = True
            page.update()
            
        except requests.RequestException as req_ex:
            print(f"Ocorreu um erro na requisição: {str(req_ex)}")
            show_snackbar(page, f"Ocorreu um erro na requisição: {str(req_ex)}", is_error=True)

    text_field = ft.TextField(label="Nome ou Razão Social", width=400)

    # Criação e abertura do diálogo
    dialog = ft.AlertDialog(
        title=ft.Text("Buscar Cliente"),
        content=text_field,
        actions=[
            ft.TextButton("Confirmar", on_click=on_confirm_fv),
            ft.TextButton("Cancelar", on_click=lambda e: close_dialog(page, dialog))
        ]
    )

    page.overlay.append(dialog)
    dialog.open = True
    page.update()

def ver_ge_conf(page):
    def on_confirm_ge(e):
        try:
            nome_ou_razao = text_field.value.strip()
            if not nome_ou_razao:
                show_snackbar(page, "Por favor, insira um nome ou razão social.", is_error=True)
                return

            # Busca os clientes que correspondem ao nome ou razão social
            clientes_filtrados = []
            clientes_data = db.child("clientes").get()
            for cliente in clientes_data.each():
                if (cliente.val().get("NOME") and nome_ou_razao.lower() in cliente.val().get("NOME").lower()) or \
                   (cliente.val().get("RAZAO") and nome_ou_razao.lower() in cliente.val().get("RAZAO").lower()):
                    clientes_filtrados.append(cliente)

            if not clientes_filtrados:
                show_snackbar(page, "Nenhum cliente encontrado com esse nome ou razão social.", is_error=True)
                return
            
            # Criação do ListView com os clientes filtrados
            client_items = []
            for cliente in clientes_filtrados:
                item = ft.ListTile(
                    title=ft.Text(cliente.val().get("NOME", ""), size=16),
                    subtitle=ft.Text(cliente.val().get("RAZAO", ""), size=14),
                    on_click=lambda e, client=cliente: on_client_select(client)
                )
                client_items.append(item)

            list_view = ft.ListView(
                controls=client_items,
                auto_scroll=True
            )

            dialog = ft.AlertDialog(
                title=ft.Text("Selecione um Cliente"),
                content=list_view,
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda e: close_dialog(page, dialog))
                ]
            )

            page.overlay.append(dialog)
            dialog.open = True
            page.update()

        except Exception as ex:
            print(f"Ocorreu um erro: {str(ex)}")
            show_snackbar(page, f"Ocorreu um erro: {str(ex)}", is_error=True)

    def on_client_select(cliente):
        ip = cliente.val().get("IP")
        porta = cliente.val().get("PORTA")
        url = f"http://{ip}:{porta}/ServicoGE/servicosResource/versaoWebService"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            versao_api = response.text.strip()

            close_dialog(page, dialog)

            if versao_api in compatibilidade_versoes_ge:
                versao_erp = compatibilidade_versoes_ge[versao_api]["ERP"]
                versao_fv = compatibilidade_versoes_ge[versao_api]["FV"]
                texto_resultado = f"Versão API: {versao_api}\nVersões ERP compatíveis: {versao_erp}\nVersões FV compatíveis: {versao_fv}"
            else:
                texto_resultado = f"Versão API: {versao_api}\nCompatibilidade desconhecida."

            # Criar um novo diálogo para exibir o resultado
            result_dialog = ft.AlertDialog(
                title=ft.Text("Resultado da Requisição"),
                content=ft.Text(texto_resultado, size=16),
                actions=[
                    ft.TextButton("Fechar", on_click=lambda e: close_dialog(page, result_dialog))
                ]
            )

            page.overlay.append(result_dialog)
            result_dialog.open = True
            page.update()
            
        except requests.RequestException as req_ex:
            print(f"Ocorreu um erro na requisição: {str(req_ex)}")
            show_snackbar(page, f"Ocorreu um erro na requisição: {str(req_ex)}", is_error=True)

    text_field = ft.TextField(label="Nome ou Razão Social", width=400)

    # Criação e abertura do diálogo
    dialog = ft.AlertDialog(
        title=ft.Text("Buscar Cliente"),
        content=text_field,
        actions=[
            ft.TextButton("Confirmar", on_click=on_confirm_ge),
            ft.TextButton("Cancelar", on_click=lambda e: close_dialog(page, dialog))
        ]
    )

    page.overlay.append(dialog)
    dialog.open = True
    page.update()

def ver_checkout_conf(page):
    def on_confirm_checkout(e):
        try:
            nome_ou_razao = text_field.value.strip()
            if not nome_ou_razao:
                show_snackbar(page, "Por favor, insira um nome ou razão social.", is_error=True)
                return

            # Busca os clientes que correspondem ao nome ou razão social
            clientes_filtrados = []
            clientes_data = db.child("clientes").get()
            for cliente in clientes_data.each():
                if (cliente.val().get("NOME") and nome_ou_razao.lower() in cliente.val().get("NOME").lower()) or \
                   (cliente.val().get("RAZAO") and nome_ou_razao.lower() in cliente.val().get("RAZAO").lower()):
                    clientes_filtrados.append(cliente)

            if not clientes_filtrados:
                show_snackbar(page, "Nenhum cliente encontrado com esse nome ou razão social.", is_error=True)
                return
            
            # Criação do ListView com os clientes filtrados
            client_items = []
            for cliente in clientes_filtrados:
                item = ft.ListTile(
                    title=ft.Text(cliente.val().get("NOME", ""), size=16),
                    subtitle=ft.Text(cliente.val().get("RAZAO", ""), size=14),
                    on_click=lambda e, client=cliente: on_client_select(client)
                )
                client_items.append(item)

            list_view = ft.ListView(
                controls=client_items,
                auto_scroll=True
            )

            dialog = ft.AlertDialog(
                title=ft.Text("Selecione um Cliente"),
                content=list_view,
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda e: close_dialog(page, dialog))
                ]
            )

            page.overlay.append(dialog)
            dialog.open = True
            page.update()

        except Exception as ex:
            print(f"Ocorreu um erro: {str(ex)}")
            show_snackbar(page, f"Ocorreu um erro: {str(ex)}", is_error=True)

    def on_client_select(cliente):
        ip = cliente.val().get("IP")
        porta = cliente.val().get("PORTA")
        url = f"http://{ip}:{porta}/ServicoCheckout/servicosResource/versaoWebService"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            versao_api = response.text.strip()

            close_dialog(page, dialog)

            if versao_api in compatibilidade_versoes_checkout:
                versao_erp = compatibilidade_versoes_checkout[versao_api]["ERP"]
                versao_fv = compatibilidade_versoes_checkout[versao_api]["FV"]
                texto_resultado = f"Versão API: {versao_api}\nVersões ERP compatíveis: {versao_erp}\nVersões FV compatíveis: {versao_fv}"
            else:
                texto_resultado = f"Versão API: {versao_api}\nCompatibilidade desconhecida."

            # Criar um novo diálogo para exibir o resultado
            result_dialog = ft.AlertDialog(
                title=ft.Text("Resultado da Requisição"),
                content=ft.Text(texto_resultado, size=16),
                actions=[
                    ft.TextButton("Fechar", on_click=lambda e: close_dialog(page, result_dialog))
                ]
            )

            page.overlay.append(result_dialog)
            result_dialog.open = True
            page.update()
            
        except requests.RequestException as req_ex:
            print(f"Ocorreu um erro na requisição: {str(req_ex)}")
            show_snackbar(page, f"Ocorreu um erro na requisição: {str(req_ex)}", is_error=True)

    text_field = ft.TextField(label="Nome ou Razão Social", width=400)

    # Criação e abertura do diálogo
    dialog = ft.AlertDialog(
        title=ft.Text("Buscar Cliente"),
        content=text_field,
        actions=[
            ft.TextButton("Confirmar", on_click=on_confirm_checkout),
            ft.TextButton("Cancelar", on_click=lambda e: close_dialog(page, dialog))
        ]
    )

    page.overlay.append(dialog)
    dialog.open = True
    page.update()

def ver_tomcat_conf(page):
    webbrowser.open('localhost:7071')

def config_conf(page):
    def on_submit(e):
        nome_serv = nome_serv_field.value
        tp_amb = tp_amb_field.value.split(" ")[0]
        servidor_uni_nfe = servidor_uni_nfe_field.value
        unidade_persistencia = unidade_persistencia_field.value
        unidade_persistencia_pdv = unidade_persistencia_pdv_field.value

        if nome_serv == "NOME DA MÁQUINA":
            nome_serv = socket.gethostname()
        if servidor_uni_nfe == "NOME DA MÁQUINA":
            servidor_uni_nfe = socket.gethostname()

        if not all([nome_serv, tp_amb, servidor_uni_nfe, unidade_persistencia, unidade_persistencia_pdv]):
            show_snackbar(page, "Todos os campos devem ser preenchidos",is_error=True)
            page.update()
            return

        try:
            xml_file = "C:\\S7\\Interface\\config.xml"
            tree = ET.parse(xml_file)
            root = tree.getroot()

            if root.find('nomeServ') is not None:
                root.find('nomeServ').text = nome_serv
            if root.find('tpAmb') is not None:
                root.find('tpAmb').text = str(tp_amb)
            if root.find('servidorUniNFe') is not None:
                root.find('servidorUniNFe').text = servidor_uni_nfe
            if root.find('unidadePersistencia') is not None:
                root.find('unidadePersistencia').text = unidade_persistencia
            if root.find('unidadePersistenciaPDV') is not None:
                root.find('unidadePersistenciaPDV').text = unidade_persistencia_pdv

            tree.write(xml_file, encoding='UTF-8', xml_declaration=True)

            show_snackbar(page, "Configurações alteradas com sucesso.", is_error=False)
            dialog.open = False

        except Exception as ex:
            show_snackbar(page, f"Erro ao alterar o arquivo: {str(ex)}", is_error=True)
        page.update()

    nome_serv_field = ft.Dropdown(
        label="Nome do Servidor",
        options=[
            ft.dropdown.Option("SERVIDOR"),
            ft.dropdown.Option("SERVIDORS7"),
            ft.dropdown.Option("NOME DA MÁQUINA")
        ]
    )

    tp_amb_field = ft.Dropdown(
        label="Tipo de Ambiente",
        options=[
            ft.dropdown.Option("1 - Produção"),
            ft.dropdown.Option("2 - Homologação"),
        ]
    )

    servidor_uni_nfe_field = ft.Dropdown(
        label="Servidor UniNFe",
        options=[
            ft.dropdown.Option("SERVIDOR"),
            ft.dropdown.Option("SERVIDORS7"),
            ft.dropdown.Option("NOME DA MÁQUINA")
        ]
    )

    unidade_persistencia_field = ft.Dropdown(
        label="Persistência ERP",
        options=[
            ft.dropdown.Option("SERVIDOR"),
            ft.dropdown.Option("SERVIDORS7"),
            ft.dropdown.Option("LOCALHOST"),
        ]
    )

    unidade_persistencia_pdv_field = ft.Dropdown(
        label="Persistência PDV",
        options=[
            ft.dropdown.Option("SERVIDOR"),
            ft.dropdown.Option("SERVIDORS7"),
            ft.dropdown.Option("LOCALHOST"),
        ]
    )

    dialog = ft.AlertDialog(
        title=ft.Text("Alterar Configurações"),
        content=ft.Column([
            nome_serv_field,
            tp_amb_field,
            servidor_uni_nfe_field,
            unidade_persistencia_field,
            unidade_persistencia_pdv_field,
        ]),
        actions=[
            ft.TextButton("Confirmar", on_click=on_submit),
            ft.TextButton("Cancelar", on_click=lambda e: close_dialog(page, dialog))
        ],
    )

    page.overlay.append(dialog)
    dialog.open = True
    page.update()

def configcompilado_conf(page):
    def on_submit(e):
        nome_servidor_compilado = nome_servidor_compilado_field.value
        nome_compilado_servidor = nome_compilado_servidor_field.value
        tipo_atualizacao = tipo_atualizacao_field.value.split(" ")[0]
        tipo_estacao = tipo_estacao_field.value.split(" ")[0]

        if nome_servidor_compilado == "NOME DA MÁQUINA":
            nome_servidor_compilado = socket.gethostname()

        if not all([nome_servidor_compilado, nome_compilado_servidor, tipo_atualizacao, tipo_estacao]):
            show_snackbar(page, "Todos os campos devem ser preenchidos", is_error=False)
            page.update()
            return

        try:
            xml_file = "C:\\S7\\Interface\\configCompilado.xml"
            tree = ET.parse(xml_file)
            root = tree.getroot()

            if root.find('nomeServidorCompilado') is not None:
                root.find('nomeServidorCompilado').text = nome_servidor_compilado
            if root.find('nomeCompiladoServidor') is not None:
                root.find('nomeCompiladoServidor').text = nome_compilado_servidor
            if root.find('tipoAtualizacao') is not None:
                root.find('tipoAtualizacao').text = str(tipo_atualizacao)
            if root.find('tipoEstacao') is not None:
                root.find('tipoEstacao').text = str(tipo_estacao)

            tree.write(xml_file, encoding='UTF-8', xml_declaration=True)

            show_snackbar(page, "Configurações alteradas com sucesso.", is_error=False)
            dialog.open = False

        except Exception as ex:
            show_snackbar(page, f"Erro ao alterar o arquivo: {str(ex)}", is_error=True)

        page.update()

    nome_servidor_compilado_field = ft.Dropdown(
        label="Nome do Servidor Compilado",
        options=[
            ft.dropdown.Option("SERVIDOR"),
            ft.dropdown.Option("SERVIDORS7"),
            ft.dropdown.Option("NOME DA MÁQUINA")
        ]
    )

    nome_compilado_servidor_field = ft.Dropdown(
        label="Nome Compilado Servidor",
        options=[
            ft.dropdown.Option("S7.EXE"),
            ft.dropdown.Option("S7.JAR"),
        ]
    )

    tipo_atualizacao_field = ft.Dropdown(
        label="Tipo de Atualização",
        options=[
            ft.dropdown.Option("1 - Estação"),
            ft.dropdown.Option("2 - Servidor"),
        ]
    )

    tipo_estacao_field = ft.Dropdown(
        label="Tipo de Estação",
        options=[
            ft.dropdown.Option("1 - Estação"),
            ft.dropdown.Option("2 - Servidor"),
        ]
    )

    dialog = ft.AlertDialog(
        title=ft.Text("Alterar Configurações Compilado"),
        content=ft.Column([
            nome_servidor_compilado_field,
            nome_compilado_servidor_field,
            tipo_atualizacao_field,
            tipo_estacao_field,
        ]),
        actions=[
            ft.TextButton("Confirmar", on_click=on_submit),
            ft.TextButton("Cancelar", on_click=lambda e: close_dialog(page, dialog))
        ],
    )

    page.overlay.append(dialog)
    dialog.open = True
    page.update()

def agendador_conf(page):
    def on_submit(e):
        agendar_ao_iniciar = agendar_ao_iniciar_field.value.split(" ")[0]

        if not agendar_ao_iniciar:
            show_snackbar(page, "Por favor, selecione uma opção.", is_error=False)
            page.update()
            return

        try:
            xml_file = "C:\\S7\\Interface\\agendadorTarefa.xml"
            tree = ET.parse(xml_file)
            root = tree.getroot()

            if root.find('agendarAoInicar') is not None:
                root.find('agendarAoInicar').text = agendar_ao_iniciar

            tree.write(xml_file, encoding='UTF-8', xml_declaration=True)

            show_snackbar(page, "Configuração alterada com sucesso.", is_error=False)
            dialog.open = False

        except Exception as ex:
            show_snackbar(page, f"Erro ao alterar o arquivo: {str(ex)}", is_error=True)
        page.update()

    agendar_ao_iniciar_field = ft.Dropdown(
        label="Agendar ao Iniciar",
        options=[
            ft.dropdown.Option("0 - Não"),
            ft.dropdown.Option("1 - Sim"),
        ]
    )

    dialog = ft.AlertDialog(
        title=ft.Text("Alterar Configuração - Agendar ao Iniciar"),
        content=ft.Column([
            agendar_ao_iniciar_field,
        ]),
        actions=[
            ft.TextButton("Confirmar", on_click=on_submit),
            ft.TextButton("Cancelar", on_click=lambda e: close_dialog(page, dialog))
        ],
    )

    page.overlay.append(dialog)
    dialog.open = True
    page.update()

def open_apps_conf(page):
    caminho_unimake = r"C:\Unimake\UniNFe\uninfe.exe"
    caminho_tomcat_64 = r"C:\Program Files\Apache Software Foundation\Tomcat 8.0\bin\Tomcat8w.exe"
    caminho_tomcat_32 = r"C:\Program Files (x86)\Apache Software Foundation\Tomcat 8.0\bin\Tomcat8w.exe"
    
    if os.path.exists(caminho_unimake):
        os.startfile(caminho_unimake)
    else:
        show_snackbar(page, f"Não foi possível encontrar o UniNFe no caminho: {caminho_unimake}", is_error=True)
    
    if os.path.exists(caminho_tomcat_64):
        os.startfile(caminho_tomcat_64)
    elif os.path.exists(caminho_tomcat_32):
        os.startfile(caminho_tomcat_32)
    else:
        show_snackbar(page, "Não foi possível encontrar o Tomcat em nenhum dos diretórios padrões.", is_error=True)

def ver_ip_serv_conf(page):
    def on_confirm(e):
        try:
            nome_ou_razao = text_field.value.strip()
            if not nome_ou_razao:
                show_snackbar(page, "Por favor, insira um nome ou razão social.", is_error=True)
                return

            clientes_filtrados = []
            clientes_data = db.child("clientes").get()
            for cliente in clientes_data.each():
                if (cliente.val().get("NOME") and nome_ou_razao.lower() in cliente.val().get("NOME").lower()) or \
                   (cliente.val().get("RAZAO") and nome_ou_razao.lower() in cliente.val().get("RAZAO").lower()):
                    clientes_filtrados.append(cliente)

            if not clientes_filtrados:
                show_snackbar(page, "Nenhum cliente encontrado com esse nome ou razão social.", is_error=True)
                return

            client_items = []
            for cliente in clientes_filtrados:
                item = ft.ListTile(
                    title=ft.Text(cliente.val().get("NOME", ""), size=16),
                    subtitle=ft.Text(cliente.val().get("RAZAO", ""), size=14),
                    on_click=lambda e, client=cliente: on_client_select(client)
                )
                client_items.append(item)

            list_view = ft.ListView(
                controls=client_items,
                auto_scroll=True
            )

            dialog = ft.AlertDialog(
                title=ft.Text("Selecione um Cliente"),
                content=list_view,
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda e: close_dialog(page, dialog))
                ]
            )

            page.overlay.append(dialog)
            dialog.open = True
            page.update()

        except Exception as ex:
            print(f"Ocorreu um erro: {str(ex)}")
            show_snackbar(page, f"Ocorreu um erro: {str(ex)}", is_error=True)

    def on_client_select(cliente):
        ip = cliente.val().get("IP")
        porta = cliente.val().get("PORTA")
        url = f"http://{ip}:{porta}"
        webbrowser.open(url)
        close_dialog(page, dialog)

    text_field = ft.TextField(label="Nome ou Razão Social", width=400)

    dialog = ft.AlertDialog(
        title=ft.Text("Buscar Cliente"),
        content=text_field,
        actions=[
            ft.TextButton("Confirmar", on_click=on_confirm),
            ft.TextButton("Cancelar", on_click=lambda e: close_dialog(page, dialog))
        ]
    )

    page.overlay.append(dialog)
    dialog.open = True
    page.update()

def close_s7_conf(page):
    try:
        comando_javaw = "taskkill /f /im javaw.exe"
        subprocess.run(["powershell", "-Command", comando_javaw], check=True)
        comando_java = "taskkill /f /im java.exe"
        subprocess.run(["powershell", "-Command", comando_java], check=True)

        show_snackbar(page, "S7 finalizado com sucesso.", is_error=False)

    except subprocess.CalledProcessError as e:
        show_snackbar(page, f"Erro ao finalizar os processos: {e}", is_error=True)

def kill_old_conf(page):
    query = """
    DECLARE @spid INT;
    
    -- Seleciona o processo com o last_batch mais antigo
    SELECT TOP 1 @spid = spid
    FROM MASTER..SYSPROCESSES 
    WHERE PROGRAM_NAME IN ('SN_PDV', 'SN_S7ERP')
    ORDER BY last_batch ASC;

    -- Executa o comando KILL se um spid for encontrado
    IF @spid IS NOT NULL
    BEGIN
        DECLARE @sql NVARCHAR(50);
        SET @sql = 'KILL ' + CAST(@spid AS NVARCHAR(10));
        EXEC sp_executesql @sql;
    END
    """

    connection = initialize_sql_server()

    if connection:
        try:
            connection.autocommit = True
            cursor = connection.cursor()
            
            cursor.execute(query)
            show_snackbar(page, "Comando executado com sucesso", is_error=False)
        
        except Exception as e:
            show_snackbar(page, f"Erro ao executar o script: {e}", is_error=True)
        finally:
            cursor.close()
            connection.close()

def close_dialog(page, dialog):
    dialog.open = False
    page.update()

def go_to_technical_page(page):
    from Libs.Technical.technical import technical_page
    page.clean()
    technical_page(page)
    page.update()
