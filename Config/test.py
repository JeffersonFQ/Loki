import pyodbc

def testar_conexao_sql():
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"  # Altere se estiver usando outro driver
        "SERVER=localhost;"  # Nome ou IP do servidor SQL
        "DATABASE=base_aa;"  # Nome do banco de dados
        "UID=sa;"  # Usuário do SQL Server
        "PWD=javadeveloper;"  # Senha do usuário
    )

    try:
        # Tentando estabelecer uma conexão
        conn = pyodbc.connect(conn_str)
        print("Conexão estabelecida com sucesso!")

        # Criar um cursor para executar uma consulta simples
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION;")
        
        # Exibir a versão do SQL Server
        row = cursor.fetchone()
        print("Versão do SQL Server:", row[0])

        # Fechar a conexão
        conn.close()
        print("Conexão encerrada.")

    except pyodbc.Error as e:
        print(f"Erro ao conectar ao SQL Server: {e}")

if __name__ == "__main__":
    testar_conexao_sql()
