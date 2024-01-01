import mysql.connector
from datetime import datetime

# Função para ler o arquivo de texto e inserir os dados no banco de dados
def inserir_atletas_from_txt(file_path, id_equipe):
    # Conexão com o banco de dados
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='073119',
        database='BRASFOOT'
    )

    cursor = db.cursor()

    # Abrir o arquivo para leitura
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        # Iterar pelo arquivo linha por linha
        if len(lines) % 6 != 0:
            print("Formato de arquivo inválido. O número de linhas não corresponde ao formato esperado.")
            return
        
        for i in range(0, len(lines), 6):  # 7 linhas por atleta conforme o formato mencionado

            if i + 5 >= len(lines):
                print("Formato de arquivo inválido. Dados incompletos para um atleta.")
                return


            nome = lines[i + 1].strip().split(': ')[1]
            numeracao = lines[i + 2].strip().split(': ')[1]
            posicao = lines[i + 3].strip().split(': ')[1]
            nacionalidade = lines[i + 4].strip().split(': ')[1]
            data_nascimento_str = lines[i + 5].strip().split(': ')[1]

            data_nascimento_str = lines[i + 5].strip().split(': ')[1].replace('(', '').replace(')', '')  # Remover parênteses extras
            data_nascimento = datetime.strptime(data_nascimento_str, '%d/%m/%Y').date()
            # Query para inserir os dados na tabela de Atletas
            insert_query = "INSERT INTO Atleta (Nome_Atleta, Posicao, DataNascimento, Nacionalidade, NumeroCamisa, EquipeID, GOLS, JOGOS, CA, CV) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (nome, posicao, data_nascimento, nacionalidade, numeracao, id_equipe, 0, 0, 0, 0)

            cursor.execute(insert_query, values)

    # Commit e fechar conexão com o banco de dados
    db.commit()
    cursor.close()
    db.close()

# Chamar a função para inserir os dados dos atletas do arquivo na tabela do banco de dados
# A lista de arquivos que deseja processar
arquivos = ['info_atletas1.txt', 
            'info_atletas3.txt', 
            'info_atletas2.txt', 
            'info_atletas4.txt', 
            'info_atletas_537.txt', 
            'info_atletas_199.txt', 
            'info_atletas_776.txt', 
            'info_atletas_609.txt', 
            'info_atletas_28022.txt', 
            'info_atletas_614.txt', 
            'info_atletas_2462.txt', 
            'info_atletas_10870.txt', 
            'info_atletas_3197.txt', 
            'info_atletas_210.txt', 
            'info_atletas_6600.txt', 
            'info_atletas_1023.txt', 
            'info_atletas_8793.txt', 
            'info_atletas_221.txt', 
            'info_atletas_585.txt', 
            'info_atletas_978.txt',]

# Defina o ID da equipe inicial
id_equipe_inicial = 1

for idx, caminho_arquivo in enumerate(arquivos, start=1):
    id_equipe = id_equipe_inicial + idx - 1
    inserir_atletas_from_txt(caminho_arquivo, id_equipe)
