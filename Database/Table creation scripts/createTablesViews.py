import mysql.connector

def ler_arquivo_sql(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        return arquivo.read()

def executar_sql_de_arquivo(nome_arquivo):
    try:
        # Conectando ao banco de dados
        # Voce deme mudar as informações de acordo com o seu banco de dados
        conexao = mysql.connector.connect(
            host='seu_host',
            user='seu_usuario',
            password='sua_senha',
            database='seu_banco_de_dados'
        )
        
        cursor = conexao.cursor()
        
        sql = ler_arquivo_sql(nome_arquivo)
        instrucoes = sql.split(';')
        
        for instrucao in instrucoes:
            if instrucao.strip() != '':
                cursor.execute(instrucao)
        
        conexao.commit()
        
        print("Instruções SQL executadas com sucesso!")
        
    except mysql.connector.Error as erro:
        print(f"Erro ao executar instruções SQL: {erro}")
        
    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()

# Substitua 'caminho_para_o_arquivo' pelo caminho do arquivo contendo as instruções SQL
caminho_arquivo_sql = 'DB_Create_Tables.sql'

executar_sql_de_arquivo(caminho_arquivo_sql)
