import pyodbc


def backup_database(server, database, user, password, backup_file):
    try:
        # Conectar ao banco de dados
        conn = pyodbc.connect(
            f'DRIVER={{SQL Server}};SERVER={server};UID={user};PWD={password}',
            autocommit=True  # Ativar auto-commit para evitar transações
        )
        cursor = conn.cursor()

        # Comando para backup do banco de dados
        backup_query = f"BACKUP DATABASE [{database}] TO DISK = N'{backup_file}' WITH NOFORMAT, INIT, SKIP, NOREWIND, NOUNLOAD, STATS = 10"
        
        # Executar o comando de backup
        cursor.execute(backup_query)
        print(f"Backup do banco de dados '{database}' realizado com sucesso em: {backup_file}")

    except pyodbc.Error as e:
        print(f"Erro ao realizar o backup: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")
    
    finally:
        # Fechar conexão
        cursor.close()
        conn.close()

if __name__ == "__main__":
    server = "localhost,1433"  # Ex: "localhost" ou "192.168.1.1"
    database = "base_aa"
    user = "sa"
    password = "javadeveloper"
    backup_file = r"C:\S7\Backup\MeuBanco.bak"  # Use 'r' para string bruta


    # Realizar o backup
    backup_database(server, database, user, password, backup_file)
