from pathlib import Path

# Define o caminho da pasta
pasta = Path('C:/Users/jeffe/Documents/Mega Pessoal/SCRIPT')

# Busca todos os arquivos .sql
arquivos_sql = list(pasta.rglob('*.sql'))

# Imprime os caminhos dos arquivos encontrados
for arquivo in arquivos_sql:
    print(arquivo)
