import pyodbc

sqlServerConfig = {
    'server': 'localhost',
    'database': 'base_aa',
    'username': 'sa',
    'password': 'javadeveloper',
    'driver': 'ODBC Driver 17 for SQL Server'
}

def initialize_sql_server():
    conn_str = (
        f"DRIVER={{{sqlServerConfig['driver']}}};"
        f"SERVER={sqlServerConfig['server']};"
        f"DATABASE={sqlServerConfig['database']};"
        f"UID={sqlServerConfig['username']};"
        f"PWD={sqlServerConfig['password']};"
    )
    
    try:
        connection = pyodbc.connect(conn_str)
        print("Conexão com SQL Server estabelecida com sucesso.")
        return connection
    except Exception as e:
        print(f"Erro ao conectar com o SQL Server: {str(e)}")
        return None
