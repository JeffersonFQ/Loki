# Loki

    Esse aplicativo surgiu da ideia de simplificar diversos processos interno utilizado na minha atual empresa, otimizando o tempo e reduzindo possiveis erros

    O aplicativo conta com uma interface grafica onde o usuário pode desde acessar a maquina do servidor do cliente em poucos cliques, como tambem diversas ferramentas que simplificam processo feitos para a configuração da base, configurações no baco de dados e verificações internas.

## Bibliotecs utilizadas

- FLET - Interface gráfica
- ELEVATE - Direitos de Administrador
- PYREBASE4 - Base de dados dos clientes e Autenticação do usuário
- PYPERCLIP - Copiar para a área de transferência
- GDOWN - Obter Instalador do Drive
- PYGETWINDOW - Controlar janela nativa do Windows
- FIREBASE-ADMIN - Controlar Permissões de usuário
- PYWEBVIEW - Abrir Visualização na Web

## Painéis

### Login

    Pagina inicial do sistema, que conta com um verificador de credenciais pelo pyrebase, decidi adotar por somente a login do usuario, a criação dos acessos ficaram por parte do administrador do sistema.

### Clientes

    Nessa página o cliente consegue fazer o acesso aos ambientes dos clientes, edição dos dados do cliente e criação dos mesmos.

### Scripts SQL

    Nessa página, temos um gerenciador de arquivos na maquina, onde nas pastas do sistema, ele buscar por scripts SQL, e os executa de forma rápida e intuitiva, executando até mesmo scripts com declare, onde a interfaçe slicita quais informações incluir nessas variáveis.

### Wiki SN

    Aqui temos funções básca, que apenas redirecionam o usuário para paginas da Web, onde estarão localizadas as páginas da Wiki interna, tornando tudo mais simples.

### Menu Técnico

    O menu técnico é bastante abrangente, centralizado tudo que é feito na parte técnica dentro do sistema, nele temos 6 funções principais:

- Windows Tools : Aqui temos diversos atalhos do windows, como por exemplo o regedit.
- Ferramentas : Aqui contamos com ferramentas utilitárias, como renomear a maquina, abrir algumas pastas e links.
- SN Tools : Aqui possuimos diversas ferramentas internas que são utilizadas somente para a empresa.
- Rede e Firewall : Aqui conseguimos configurar todos os parametros de rede que utilizamos que fogem do padrão de instalação.
- Verificações : Aqui podemos fazer diversas verificações no banco de dados e maquina do cliente.
- Instalações : Aqui temos todos os softwares de terceiro que instalamos para a funcionalidade do sistema.

### Migração

    As migrações hoje, são feitas manualmente, essa função vai incluir uma forma mais fácil e simples de migrarmos dados entre bases de clientes, desde outros bancos de dados, a arquivos de excel.

### API Movdesk

    Em desenvolvimento.

### Configurações

    Em desenvoltimento .

### Sair

    Aqui saimos do sistema.