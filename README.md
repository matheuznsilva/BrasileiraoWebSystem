# BRASILEIRAO WEBSYSTEM

Este repositorio possui o trabalho prático da disciplina de Banco de dados no curso de Ciência da
Computação na UFSJ de 2023.
Vide descrição completa na Documentação presente nesse repositório.

## Requisitos

<div>
  <img src="https://img.shields.io/badge/Python-F4D03F?style=for-the-badge&amp;logo=Python&amp;logoColor=black" alt="PYTHON">
  <img src="https://img.shields.io/badge/Flask-323330?style=for-the-badge&amp;logo=Flask&amp;logoColor=white" alt="FLASK">
  <img src="https://img.shields.io/badge/MySql-F1C40F?style=for-the-badge&amp;logo=MySql&amp;logoColor=black" alt="MYSQL">
  <img src="https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&amp;logo=javascript&amp;logoColor=F7DF1E" alt="javascript">
</div>

## Instalação

Todas as instalações abaixo são referentes ao Ubuntu

### Instalar Python

O Python geralmente já está instalado no Ubuntu, mas você pode verificar a versão digitando:

    $ python3 --version

Se não estiver instalado ou você precisar de uma versão específica, você pode instalar usando o apt:

    $ sudo apt update
    $ sudo apt install python3

### Instalar Flask

O Flask é um framework web em Python. Você pode instalar o Flask usando o `pip`, que é o gerenciador de pacotes do Python:

    $ pip install flask

### Instalar Node.js e JavaScript

#### Instalar Node.js

O Node.js é usado para executar JavaScript no lado do servidor e é frequentemente usado com aplicativos baseados em JavaScript.

Primeiro, instale o Node.js usando `apt`:

    $ sudo apt update
    $ sudo apt install nodejs

Para instalar o npm (Node Package Manager), que é o gerenciador de pacotes para Node.js:

    $ sudo apt install npm

### Instalar MySQL

#### Instalar o MySQL Server

Você pode instalar o MySQL Server através do apt:

    $ sudo apt update
    $ sudo apt install mysql-server

Durante a instalação, você será solicitado a definir uma senha para o usuário root do MySQL.

Após a instalação, inicie o serviço MySQL e habilite-o para ser executado na inicialização do sistema:

    $ sudo systemctl start mysql
    $ sudo systemctl enable mysql

#### Instalar o Cliente MySQL

Para interagir com o MySQL a partir da linha de comando ou para configurar banco de dados e tabelas, você pode instalar o cliente MySQL:

    $ sudo apt install mysql-client

## Uso

Após todas as dependencias instaladas, entre no diretorio Application via terminal

    $ cd Application/

E depois execute o comando

    $ python3 app.py

tendo executado o comando acima, abra o navegador de sua preferência e digite na barra de endereços: 

    http://localhost:5000

## Estrutura do Projeto

Brasileirao_Web_Sytem
|
|-- Application/: Este diretório contém todo o código relacionado a aplicação.
|   |
|   |-- static/: Contém arquivos estáticos como CSS, JavaScript e imagens.
|   |-- css/: Arquivos de estilo CSS.
|   |-- js/: Arquivos de script JavaScript.
|   |-- images/: Armazena imagens utilizadas no projeto.
|   |-- templates/: Arquivos HTML usando Jinja2 (usado pelo Flask) para renderizar páginas dinâmicas.
|   |-- app.py: Arquivo principal do Flask. Contém rotas, configurações e interações com a aplicação Flask.
|-- Database/: Esse diretorio contem os Scripts para criação de povoamento do banco de dados, alem de um exemplo de BD
|   |-- Example Database/: Exemplo de Banco de Dados funcional
|   |-- Population script/: Scripts de povoamento do banco de dados
|   |-- Table creation script/: Script de criação do banco de dados

## Status do Projeto

**Status do Projeto: Parcialmente Concluído**

O projeto está funcional e atende a grande parte das especificações requisitadas. No entanto, algumas modificações e ajustes são necessários para alcançar completamente os requisitos definidos.

**Conquistas Atuais:**
- Funcionalidades básicas implementadas com sucesso.
- Backend e Frontend integrados.
- Estrutura de diretórios organizada e funcional.
- CRUD (Create, Read, Update, Delete) básico funcionando.
- Interface do usuário (UI) está operacional.

**Próximos Passos:**
- Ajustar detalhes de layout e estilização.
- Implementar recursos adicionais conforme especificações.
- Melhorar a usabilidade e experiência do usuário.
- Realizar testes e correções de bugs.
- Aperfeiçoar a segurança da aplicação.
- Refatorar código para aumentar a eficiência e manutenibilidade.

O projeto encontra-se em um estágio avançado, mas ainda requer alguns ajustes e melhorias para estar totalmente alinhado com as especificações desejadas. Com os próximos passos e ajustes necessários, a expectativa é alcançar os objetivos definidos de forma satisfatória.
