import mysql.connector
from datetime import datetime

def conectar_banco():
    # Substitua os valores abaixo pelos seus próprios dados de conexão ao banco de dados MySQL
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='073119',
        database='BRASFOOT'
    )
def converter_data(data_hora):
    datahoraobj = datetime.strptime(data_hora, "%d/%m/%Y-%H:%M")
    dataconvertida = datahoraobj.strftime("%Y/%m/%d-%H:%M")
    return dataconvertida

def inserir_partidas():
    arquivo_partidas = 'novo_arquivo.txt'  # Nome do arquivo de texto com os dados das partidas

    try:
        db = conectar_banco()
        cursor = db.cursor()
        rodada = 1
        count = 0;

        with open(arquivo_partidas, 'r') as arquivo:
            linhas = arquivo.readlines()
            num_partidas = len(linhas)

            for linha in linhas:
                dados_partida = linha.strip().split()

                # Obtém os dados da linha
                data_hora = dados_partida[0]
                mandante_id = int(dados_partida[1])
                gols_mandante = int(dados_partida[2])
                gols_visitante = int(dados_partida[3])
                visitante_id = int(dados_partida[4])
                
                # Obtém o estádio com base no ID da equipe mandante
                cursor.execute(f"SELECT Estadio FROM Equipe WHERE ID_Equipe = {mandante_id}")
                estadio = cursor.fetchone()[0]

                # Insere os dados da partida na tabela Partidas
                sql = "INSERT INTO Partidas (Rodada, DiaHora, EquipeMandanteID, GolsMandante, GolsVisitante, EquipeVisitanteID, Estadio_Partida) " \
                      "VALUES (%s, %s, %s, %s, %s, %s, %s)"
                val = (rodada, data_hora, mandante_id, gols_mandante, gols_visitante, visitante_id, estadio)
                cursor.execute(sql, val)
                count += 1
                # A cada 10 partidas inseridas, incrementa o número da rodada
                if count % 10 == 0:
                    rodada += 1

        db.commit()
        cursor.close()
        db.close()
        print(f"{num_partidas} partidas foram inseridas com sucesso no banco de dados!")

    except mysql.connector.Error as error:
        print(f"Erro ao inserir partidas: {error}")

# Chama a função para inserir as partidas no banco de dados
inserir_partidas()


""" from datetime import datetime

# Função para converter o formato da data e hora
def converter_formato(data_hora):
    formato_entrada = "%d/%m/%Y-%H:%M"
    formato_saida = "%Y-%m-%d-%H:%M:%S"

    # Converter a string para objeto datetime
    data_hora_obj = datetime.strptime(data_hora, formato_entrada)

    # Converter para o novo formato desejado
    nova_data_hora = data_hora_obj.strftime(formato_saida)
    
    return nova_data_hora

# Abrir o arquivo de entrada
with open('info_partidas.txt', 'r') as arquivo_entrada:
    linhas = arquivo_entrada.readlines()

# Abrir o arquivo de saída
with open('novo_arquivo.txt', 'w') as arquivo_saida:
    for linha in linhas:
        # Separe a linha nos espaços para acessar a data e hora
        partes = linha.split(' ')
        data_hora = partes[0]

        # Chame a função para converter o formato da data e hora
        nova_data_hora = converter_formato(data_hora)
        
        # Escreva a nova linha no arquivo de saída
        partes[0] = nova_data_hora
        nova_linha = ' '.join(partes)
        arquivo_saida.write(nova_linha) """
