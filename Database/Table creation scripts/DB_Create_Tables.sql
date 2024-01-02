/* sudo mysql -u root -p */

------- TABELAS -------

-- Tabela Usuarios

CREATE TABLE Usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL;
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    nome_completo VARCHAR(255) UNIQUE NOT NULL
);

-- Tabela Equipes

CREATE TABLE Equipe (
    ID_Equipe INT AUTO_INCREMENT PRIMARY KEY,
    Nome_Equipe VARCHAR(50) NOT NULL,
    Nome_Completo_Equipe VARCHAR(100) NOT NULL,
    Cidade VARCHAR(50),
    Estado VARCHAR(50),
    Treinador VARCHAR(100),
    Estadio VARCHAR(100)
);

-- Tabela Atletas

CREATE TABLE Atleta (
    ID_Atleta INT AUTO_INCREMENT PRIMARY KEY,
    Nome_Atleta VARCHAR(100) NOT NULL,
    Posicao VARCHAR(50),
    DataNascimento DATE,
    Nacionalidade VARCHAR(50),
    NumeroCamisa INT,
    EquipeID INT,
    GOLS INT,
    JOGOS INT,
    CA INT,
    CV INT,
    FOREIGN KEY (EquipeID) REFERENCES Equipe(ID_Equipe)
);

-- Tabela Partidas

CREATE TABLE Partidas (
    ID_Partida INT AUTO_INCREMENT PRIMARY KEY,
    Rodada INT,
    DiaHora DATETIME NOT NULL,
    EquipeMandanteID INT,
    EquipeVisitanteID INT,
    Estadio_Partida VARCHAR(100),
    GolsMandante INT,
    GolsVisitante INT,
    FOREIGN KEY (EquipeMandanteID) REFERENCES Equipe(ID_Equipe),
    FOREIGN KEY (EquipeVisitanteID) REFERENCES Equipe(ID_Equipe)
);

-- Tabela do Campeonato

CREATE TABLE Tabela_Brasileirao (
    POS INT AUTO_INCREMENT PRIMARY KEY,
    EquipeID INT,
    Pts INT,
    Jogos INT,
    Vitoria INT,
    Empate INT,
    Derrota INT,
    GP INT,
    GC INT,
    SG INT,
    CA INT,
    CV INT,
    FOREIGN KEY (EquipeID) REFERENCES Equipe(ID_Equipe)
);

------- VIEWS --------

-- View Classificação

CREATE VIEW Classificacao AS
SELECT 
    ROW_NUMBER() OVER (ORDER BY Pts DESC, Vitoria DESC, SG DESC, GP DESC, GC ASC, CV ASC, CA ASC) AS POS,
    E.Nome_Equipe as Nome,
    Pts,
    Jogos,
    Vitoria,
    Empate,
    Derrota,
    GP,
    GC,
    SG,
    CA,
    CV
FROM Tabela_Brasileirao T
JOIN Equipe E ON T.EquipeID = E.ID_Equipe;

-- View Partidas

CREATE VIEW PartidasOrdenadas AS 
SELECT p.*, e1.Nome_Equipe AS Mandante, e2.Nome_Equipe AS Visitante 
FROM Partidas p 
INNER JOIN Equipe e1 ON p.EquipeMandanteID = e1.ID_Equipe 
INNER JOIN Equipe e2 ON p.EquipeVisitanteID = e2.ID_Equipe 
ORDER BY STR_TO_DATE(p.DiaHora, '%Y-%m-%d %H:%i:%s') ASC;

-- View Artilheiros

CREATE VIEW Artilheiro AS 
SELECT A.ID_Atleta, E.Nome_Equipe, A.Nome_Atleta, A.GOLS, A.JOGOS 
FROM Atleta A 
INNER JOIN Equipe E ON A.EquipeID = E.ID_Equipe 
ORDER BY A.GOLS DESC 
LIMIT 20;

CREATE VIEW Artilheiro AS
SELECT ID_Atleta, Nome_Atleta, GOLS, JOGOS
FROM Atleta a
WHERE GOLS >= (
    SELECT DISTINCT GOLS
    FROM Atleta b
    ORDER BY GOLS DESC
    LIMIT 9, 1
) OR (
    GOLS = (
        SELECT DISTINCT GOLS
        FROM Atleta c
        ORDER BY GOLS DESC
        LIMIT 9, 1
    ) AND JOGOS < (
        SELECT MIN(JOGOS)
        FROM Atleta d
        WHERE d.GOLS = (
            SELECT DISTINCT GOLS
            FROM Atleta e
            ORDER BY GOLS DESC
            LIMIT 9, 1
        )
    )
)
ORDER BY GOLS DESC, JOGOS ASC
LIMIT 20;

-- Views Cartões

CREATE VIEW CartoesVermelhos AS
SELECT A.ID_Atleta, E.Nome_Equipe, A.Nome_Atleta, A.CV, A.JOGOS
FROM Atleta A
INNER JOIN Equipe E ON A.EquipeID = E.ID_Equipe
ORDER BY A.CV DESC
LIMIT 20;

CREATE VIEW CartoesAmarelos AS
SELECT A.ID_Atleta, E.Nome_Equipe, A.Nome_Atleta, A.CA, A.JOGOS
FROM Atleta A
INNER JOIN Equipe E ON A.EquipeID = E.ID_Equipe
ORDER BY A.CA DESC
LIMIT 20;

----------------------------------------------