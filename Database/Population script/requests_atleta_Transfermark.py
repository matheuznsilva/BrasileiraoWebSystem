import requests
from bs4 import BeautifulSoup

# Defina um cabeçalho de usuário para simular um navegador real
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Lista de URLs das equipes do Campeonato Brasileiro Série A no Transfermarkt
urls = [
    'https://www.transfermarkt.com.br/botafogo-rio-de-janeiro/startseite/verein/537/saison_id/2022',
    'https://www.transfermarkt.com.br/corinthians-sao-paulo/startseite/verein/199/saison_id/2022',
    'https://www.transfermarkt.com.br/coritiba-fc/startseite/verein/776/saison_id/2022',
    'https://www.transfermarkt.com.br/ec-cruzeiro-belo-horizonte/startseite/verein/609/saison_id/2022',
    'https://www.transfermarkt.com.br/cuiaba-ec-mt-/startseite/verein/28022/saison_id/2022',
    'https://www.transfermarkt.com.br/flamengo-rio-de-janeiro/startseite/verein/614/saison_id/2022',
    'https://www.transfermarkt.com.br/fluminense-rio-de-janeiro/startseite/verein/2462/saison_id/2022',
    'https://www.transfermarkt.com.br/fortaleza-esporte-clube/startseite/verein/10870/saison_id/2022',
    'https://www.transfermarkt.com.br/goias-ec/startseite/verein/3197/saison_id/2022',
    'https://www.transfermarkt.com.br/gremio-porto-alegre/startseite/verein/210/saison_id/2022',
    'https://www.transfermarkt.com.br/sc-internacional-porto-alegre/startseite/verein/6600/saison_id/2022',
    'https://www.transfermarkt.com.br/se-palmeiras-sao-paulo/startseite/verein/1023/saison_id/2022',
    'https://www.transfermarkt.com.br/red-bull-bragantino/startseite/verein/8793/saison_id/2022',
    'https://www.transfermarkt.com.br/fc-santos/startseite/verein/221/saison_id/2022',
    'https://www.transfermarkt.com.br/fc-sao-paulo/startseite/verein/585/saison_id/2022',
    'https://www.transfermarkt.com.br/vasco-da-gama-rio-de-janeiro/startseite/verein/978/saison_id/2022',
    # Adicione mais URLs das equipes aqui...
]

for url in urls:
    # Fazendo a requisição GET para obter o HTML da página com o cabeçalho definido
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Encontrando a tabela que contém os dados dos jogadores
        players_table = soup.find('table', class_='items')

        # Verificando se a tabela foi encontrada
        if players_table:
            # Abrindo um arquivo para escrita
            with open(f'info_atletas_{url.split("/")[-3]}.txt', 'w', encoding='utf-8') as file:
                # Iterando pelas linhas da tabela para obter as informações dos jogadores
                rows = players_table.find_all('tr', class_=lambda x: x and ('odd' in x or 'even' in x))
                for row in rows:
                    data = row.find_all('td')

                    # Extraindo os dados de cada coluna
                    numeracao = data[0].get_text(strip=True)
                    nome = data[1].get_text(strip=True)
                    posicao = data[4].get_text(strip=True)

                    # Encontrando a célula correta que contém a data de nascimento
                    celulas_zentriert = row.find_all('td', class_='zentriert')
                    if len(celulas_zentriert) >= 2:
                        nascimento = celulas_zentriert[1].get_text(strip=True)
                    else:
                        nascimento = 'N/A'

                    nacionalidade = data[6].img['title'] if data[6].img else 'N/A'

                    # Escrevendo os dados no arquivo
                    file.write(f"Nome: {nome}\nNumeração: {numeracao}\nPosição: {posicao}\n"
                               f"Nacionalidade: {nacionalidade}\nData de Nascimento: {nascimento}\n\n")
            print(f"Informações dos atletas da equipe {url.split('/')[-3]} foram coletadas e salvas no arquivo 'info_atletas_{url.split('/')[-3]}.txt'.")
        else:
            print("Tabela de jogadores não encontrada para a equipe:", url.split('/')[-3])
    else:
        print("Falha ao acessar a página:", url)
