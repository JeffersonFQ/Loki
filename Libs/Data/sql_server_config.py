import pyodbc

# Configurações da conexão com o SQL Server
sqlServerConfig = {
    'server': 'localhost',   # Insira o nome ou endereço do servidor SQL
    'database': 'base_aa',  # Insira o nome do banco de dados
    'username': 'sa',   # Insira o nome de usuário
    'password': 'javadeveloper',     # Insira a senha
    'driver': 'ODBC Driver 17 for SQL Server'  # Certifique-se que o driver está instalado
}

# Função para inicializar a conexão com o SQL Server
def initialize_sql_server():
    conn_str = (
        f"DRIVER={{{sqlServerConfig['driver']}}};"
        f"SERVER={sqlServerConfig['server']};"
        f"DATABASE={sqlServerConfig['database']};"
        f"UID={sqlServerConfig['username']};"
        f"PWD={sqlServerConfig['password']};"
    )
    
    try:
        # Estabelecendo a conexão
        connection = pyodbc.connect(conn_str)
        print("Conexão com SQL Server estabelecida com sucesso.")
        return connection
    except Exception as e:
        print(f"Erro ao conectar com o SQL Server: {str(e)}")
        return None
