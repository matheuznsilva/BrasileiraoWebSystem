from flask import Flask, render_template, request, redirect, url_for, send_file
import mysql.connector
from flask_bcrypt import bcrypt
from datetime import datetime

app = Flask(__name__)

# Conecta ao banco de dados MySQL

app.config['DB_CONFIG'] = {
    'host':'localhost',
    'user':'root',
    'password':'073119',
    'database':'BRASFOOT'
}

def obter_conexao():
    return mysql.connector.connect(**app.config['DB_CONFIG'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classificacao')
def classificacao():
    with obter_conexao() as db:
        cursor = db.cursor()

        # Executar a consulta
        cursor.execute("SELECT * FROM Classificacao")

        # Obter os resultados
        resultados = cursor.fetchall()

        # Fechar a conexão
        db.close()

    return render_template('classificacao.html', tabela=resultados)
    
@app.route('/edita_partida', methods = ['GET', 'POST'])
def edita_partida():
    if request.method == 'POST':
        nova_data_hora = request.form['DataTime']
        novo_local = request.form['EstadioPartida']
        novo_rodada = request.form['rodada']
        

        try:
            db = obter_conexao()
            cursor = db.cursor()

            sql = "UPDATE Partidas SET DiaHora = %s, Local = %s, Rodada = %s WHERE ID_Partida = %s"
            val = (nova_data_hora, novo_local, novo_rodada, partida_id)
            cursor.execute(sql, val)

            db.commit()

            cursor.close()
            db.close()

            return redirect(url_for('partidas'))  # Redireciona para a página de partidas após a edição

        except mysql.connector.Error as error:
            print("Erro ao atualizar a partida:", error)
            return "Erro ao atualizar a partida"

    else:
        partida_id = 1

        try:
            db = obter_conexao()
            cursor = db.cursor()
            sql = "SELECT * FROM Partidas WHERE ID_Partida = %s"
            val = (partida_id,)
            cursor.execute(sql, val)
            partida = cursor.fetchone()

            cursor.close()
            db.close()

            return render_template('edita_partida.html', partida=partida)

        except mysql.connector.Error as error:
            print("Erro ao buscar a partida:", error)
            return "Erro ao buscar a partida"

# ----- Partidas -----
@app.route('/partidas')
def partidas():
    try:
        db = obter_conexao()
        cursor = db.cursor(dictionary=True)

        rodada = int(request.args.get('rodada', 1))
       
        cursor.execute("SELECT * From PartidasOrdenadas Where Rodada = %s", (rodada,))
        partidas = cursor.fetchall()

        # Fechar a conexão
        cursor.close()
        db.close()

        return render_template('partidas.html', partidas=partidas, rodada_atual = rodada)

    except mysql.connector.Error as error:
        print("Erro ao obter partidas:", error)
        return render_template('error.html', error=error)  # Página de erro caso ocorra um problema

@app.route('/cadastro_partida', methods=['GET', 'POST'])
def cadastro_partida():
    if request.method == 'POST':
        nova_partida = {
            'EquipeMandante': request.form['EquipeMandante'],
            'EquipeVisitante': request.form['EquipeVisitante'],
            'Estadio': request.form['EstadioPartida'],
            'DataTime': request.form['DataTime'],
            'Rodada': request.form['rodada']
        }
        try:
            db = obter_conexao()
            cursor = db.cursor()

            cursor.execute("SELECT ID_Equipe FROM Equipe WHERE Nome_Equipe = %s", (nova_partida['EquipeMandante'],))
            mandante_ID = cursor.fetchone()
            if mandante_ID:
                mandante_ID = mandante_ID[0]

            cursor.execute("SELECT ID_Equipe FROM Equipe WHERE Nome_Equipe = %s", (nova_partida['EquipeVisitante'],))
            visitante_ID = cursor.fetchone()
            if visitante_ID:
                visitante_ID = visitante_ID[0]

            sql = "INSERT INTO Partidas (Rodada, DiaHora, EquipeMandanteID, EquipeVisitanteID, Estadio_Partida, GolsMandante, GolsVisitante) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (nova_partida['Rodada'], nova_partida['DataTime'], mandante_ID, visitante_ID, nova_partida['Estadio'], 0, 0)
            cursor.execute(sql, val)
            db.commit()

            # Fechar a conexão
            cursor.close()
            db.close()

            return redirect(url_for('cadastro_partida'))
    
        except mysql.connector.Error as error:
            print("Erro ao inserir nova partida:", error)
            return redirect(url_for('cadastro_partida'))
    return render_template('cadastro_partida.html')


@app.route('/remover_partida', methods=['GET', 'POST'])
def remover_partida():
    if request.method == 'POST':
        equipe_mandante = request.form['EquipeMandante'],
        equipe_visitante = request.form['EquipeVisitante'],
        rodada = request.form['rodada']
        try:
            db = obter_conexao()
            cursor = db.cursor()

            cursor.execute("SELECT ID_Equipe FROM Equipe WHERE Nome_Equipe = %s", (equipe_mandante))
            mandante_ID = cursor.fetchone()
            if mandante_ID:
                mandante_ID = mandante_ID[0]

            cursor.execute("SELECT ID_Equipe FROM Equipe WHERE Nome_Equipe = %s", (equipe_visitante))
            visitante_ID = cursor.fetchone()
            if visitante_ID:
                visitante_ID = visitante_ID[0]

            sql = "DELETE FROM Partidas WHERE EquipeMandanteID = %s AND EquipeVisitanteID = %s AND Rodada = %s"
            val = (mandante_ID, visitante_ID, rodada)
            cursor.execute(sql, val)
            db.commit()
            print("Partida removida com sucesso.")
            # Fechar a conexão
            cursor.close()
            db.close()

            return redirect(url_for('remover_partida'))
    
        except mysql.connector.Error as error:
            print("Erro ao inserir nova partida:", error)
            return redirect(url_for('remover_partida'))
    return render_template('remover_partida.html')



@app.route('/estatisticas')
def estatisticas():
    with obter_conexao() as db:
        cursor = db.cursor()

        # Consulta para a view de Artilheiros
        cursor.execute("SELECT Nome_Equipe, Nome_Atleta, GOLS FROM Artilheiro")
        artilheiros = cursor.fetchall()

        # Consulta para a view de Cartões Vermelhos
        cursor.execute("SELECT Nome_Equipe, Nome_Atleta, CV FROM CartoesVermelhos")
        cartoes_vermelhos = cursor.fetchall()

        # Consulta para a view de Cartões Amarelos
        cursor.execute("SELECT Nome_Equipe, Nome_Atleta, CA FROM CartoesAmarelos")
        cartoes_amarelos = cursor.fetchall()

    return render_template('estatisticas.html', artilheiros=artilheiros, cartoes_amarelos=cartoes_amarelos, cartoes_vermelhos=cartoes_vermelhos)


@app.route('/gerenciamento')
def gerenciamento():
    return render_template('gerenciamento.html');  

# ----- CADASTRAR NOVA EQUIPE -----

@app.route('/cadastro_equipe', methods=['GET', 'POST'])
def cadastro_equipe():
    if request.method == 'POST':
        nova_equipe = {
            'Nome_Completo_Equipe': request.form['nome_completo'],
            'Nome_Equipe': request.form['nome_equipe'],
            'Cidade': request.form['cidade'],
            'Estado': request.form['estado'],
            'Treinador': request.form['treinador'],
            'Estadio': request.form['estadio']
        }
        try:
            db = obter_conexao()
            cursor = db.cursor()

            sql = "INSERT INTO Equipe (Nome_Equipe, Nome_Completo_Equipe, Cidade, Estado, Treinador, Estadio) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (nova_equipe['Nome_Equipe'], nova_equipe['Nome_Completo_Equipe'], nova_equipe['Cidade'], nova_equipe['Estado'], nova_equipe['Treinador'], nova_equipe['Estadio'])
            cursor.execute(sql, val)

            db.commit()

            # Fechar a conexão
            cursor.close()
            db.close()

            return redirect(url_for('cadastro_equipe'))
    
        except mysql.connector.Error as error:
            print("Erro ao inserir nova equipe:", error)
            return redirect(url_for('cadastro_equipe'))
    return render_template('cadastro_equipe.html')


@app.route('/remover_equipe', methods=['GET', 'POST'])
def remover_equipe():
    if request.method == 'POST':
        nova_equipe = {
            'Nome_Equipe' : request.form['nome_equipe']
        }
        try:
            db = obter_conexao()
            cursor = db.cursor()
            cursor.execute("SELECT ID_Equipe FROM Equipe WHERE Nome_Equipe = %s", (nova_equipe['Nome_Equipe'],))

            equipeID = cursor.fetchone()
            if equipeID:
                equipeID = int(equipeID[0])

                sql = "DELETE FROM Equipe WHERE ID_Equipe = %s"
                val = (equipeID,)
                cursor.execute(sql, val)
                db.commit()
                print("Equipe removida com sucesso.")

            # Fechar a conexão
            cursor.close()
            db.close()

            return redirect(url_for('remover_equipe'))
    
        except mysql.connector.Error as error:
            print("Erro ao remover equipe:", error)
            return redirect(url_for('remover_equipe'))
    return render_template('remover_equipe.html')


# ------ ATLETA ------
@app.route('/cadastro_atleta', methods=['GET', 'POST'])
def cadastro_atleta():
    if request.method == 'POST':
        novo_atleta = {
            'nome_atleta': request.form['nome_atleta'],
            'nome_equipe': request.form['nome_equipe'],
            'posicao': request.form['posicao'],
            'nacionalidade': request.form['nacionalidade'],
            'uniforme': request.form['uniforme'],
            'data_nascimento': request.form['data_nascimento']  # Corrigido o nome do campo
        }
        try:
            db = obter_conexao()
            cursor = db.cursor()

            # Obtém o ID da equipe com base no nome da equipe fornecido
            cursor.execute("SELECT ID_Equipe FROM Equipe WHERE Nome_Equipe = %s", (novo_atleta['nome_equipe'],))
            equipe_id = cursor.fetchone()
            
            if equipe_id:
                equipe_id = equipe_id[0]

                # Prepara e executa a query de inserção do novo atleta
                sql = "INSERT INTO Atleta (Nome_Atleta, Posicao, DataNascimento, Nacionalidade, NumeroCamisa, EquipeID, GOLS, JOGOS, CA, CV) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (
                    novo_atleta['nome_atleta'],
                    novo_atleta['posicao'],
                    novo_atleta['data_nascimento'],
                    novo_atleta['nacionalidade'],
                    novo_atleta['uniforme'],
                    equipe_id,
                    0,  # Valores padrão para GOLS, JOGOS, CA, CV
                    0,
                    0,
                    0
                )
                cursor.execute(sql, val)
                db.commit()

            # Fechar a conexão
            cursor.close()
            db.close()

            return redirect(url_for('cadastro_atleta'))
    
        except mysql.connector.Error as error:
            print("Erro ao inserir novo atleta:", error)
            return redirect(url_for('cadastro_atleta'))
    
    return render_template('cadastro_atleta.html')





@app.route('/remover_atleta', methods=['GET', 'POST'])
def remover_atleta():
    if request.method == 'POST':
        novo_atleta = {
            'nome_atleta': request.form['nome_atleta'],
            'nome_equipe': request.form['nome_equipe'],
            'posicao': request.form['posicao']
        }
        try:
            db = obter_conexao()
            cursor = db.cursor()

            cursor.execute("SELECT ID_Equipe FROM Equipe WHERE Nome_Equipe = %s", (novo_atleta['nome_equipe'],))
            equipe_id = cursor.fetchone()

            if equipe_id:
                equipe_id = equipe_id[0]  # Extrai o ID da equipe da consulta

                # Consulta os atletas da equipe com base no ID da equipe obtido anteriormente
                #cursor.execute("SELECT ID_Atleta FROM Atleta WHERE Nome_Atleta = %s, EquipeID = %s", (equipe_id,))
                cursor.execute("SELECT ID_Atleta FROM Atleta WHERE Nome_Atleta = %s AND EquipeID = %s", (novo_atleta['nome_atleta'], equipe_id))

                atleta = cursor.fetchone()

                if atleta:
                    atleta_id = int(atleta[0])  # ID do atleta a ser removido

                    sql = "DELETE FROM Atleta WHERE ID_Atleta = %s"
                    val = (atleta_id,)
                    cursor.execute(sql, val)
                    db.commit()
                    print("Atleta removido com sucesso.")

                # Fechar a conexão
                cursor.close()
                db.close()

                return redirect(url_for('remover_atleta'))

    
        except mysql.connector.Error as error:
            print("Erro ao remover equipe:", error)
            return redirect(url_for('remover_atleta'))
    return render_template('remover_atleta.html')

# ----- login -----
# Função para autenticação de usuário
def autenticar_usuario(username, password):
    try:
        db = obter_conexao()
        cursor = db.cursor(dictionary=True)

        # Consulta para verificar as credenciais do usuário
        sql = "SELECT * FROM Usuarios WHERE username = %s"
        val = (username,)
        cursor.execute(sql, val)

        user = cursor.fetchone()  # Obter o usuário se existir
        
        if user:
            hashed_password = user['password'].encode('utf-8')
            input_password = password.encode('utf-8')
            if bcrypt.checkpw(input_password, hashed_password):
                cursor.close()
                db.close()
                return user  # Retorna o usuário encontrado ou None se não existir
        cursor.close()
        db.close()
        return None  # Retorna o usuário encontrado ou None se não existir
        
    except mysql.connector.Error as error:
        print("Erro ao autenticar usuário:", error)
        return None

# Rota para lidar com o login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = autenticar_usuario(username, password)

        if user:
            # Autenticação bem-sucedida, redirecione para a página principal ou outra página
            return redirect(url_for('gerenciamento'))
        else:
            # Credenciais inválidas, renderize a página de login novamente ou exiba uma mensagem de erro
            return render_template('login.html', error="Credenciais inválidas. Tente novamente.")

    return render_template('login.html')

# Rota para lidar com o registro de usuários
@app.route('/registro', methods=['GET','POST'])
def registro():
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        nome = request.form['nome']

        if 'username' in request.form and 'password' in request.form and 'email' in request.form and 'nome' in request.form:
        # Criptografa a senha antes de armazená-la no banco de dados
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            try:
                db = obter_conexao()
                cursor = db.cursor()

                # Insere o novo usuário no banco de dados com a senha criptografada
                sql = "INSERT INTO Usuarios (username, password, email, nome_completo) VALUES (%s, %s, %s, %s)"
                val = (username, hashed_password, email, nome)
                cursor.execute(sql, val)

                db.commit()
                cursor.close()
                db.close()

                return redirect(url_for('login'))  # Redireciona para a página de login após o registro

            except mysql.connector.Error as error:
                print("Erro ao registrar usuário:", error)
                return render_template('registro.html', error="Erro ao registrar usuário.")
    else:
            return render_template('registro.html', error="Erro ao registrar usuário.")

@app.route('/change_password', methods=['GET','POST'])
def change_password():
    
    if request.method == 'POST':
        username = request.form['username']
        oldpassword = request.form['oldpassword']
        newpassword = request.form['newpassword']
            

        if 'username' in request.form and 'oldpassword' in request.form and 'newpassword' in request.form:
            try:
                db = obter_conexao()
                cursor = db.cursor()

                sql = "SELECT * FROM Usuarios WHERE username = %s"
                val = (username,)
                cursor.execute(sql, val)

                user = cursor.fetchone()

                if user:
                    hashed_password = user[2].encode('utf-8')
                    input_password = oldpassword.encode('utf-8')
                    if bcrypt.checkpw(input_password, hashed_password):
                        hashed_new_password = bcrypt.hashpw(newpassword.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                        sql_update = "UPDATE Usuarios SET password = %s WHERE username = %s"
                        cursor.execute(sql_update, (hashed_new_password, username))
                        db.commit()
                        cursor.close()
                        db.close()
                        return redirect(url_for('gerenciamento'))  # Redireciona para a página de login após o registro
                    else:
                        return render_template('change_password.html', error="Senha antiga incorreta.")  # Redireciona para a página de login após o registro
                else:
                    return render_template('change_password.html', error="Usuário não encontrado.")  # Redireciona para a página de login após o registro

            except mysql.connector.Error as error:
                print("Erro ao alterar a senha:", error)
                return render_template('change_password.html', error="Erro ao alterar senha.")
        else:
            return render_template('change_password.html', error="Preencha todos os campos.")
    else:
        return render_template('change_password.html')

if __name__ == '__main__':
    app.run(debug=True)
