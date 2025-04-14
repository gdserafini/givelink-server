# GiveLink
Servidor do trabalho de experiência criativa - 5º período BSI PUCPR.<br>
A GiveLink consiste em uma plataforma onde doadores e instituições como ONGs, hospitais podem se conectar e realizar doações pela plataforma.
## Configuração e como rodar o projeto
### Requisitos
* Docker/Docker Desktop
### Configuração
Rode o comando para buildar a aplicação com Docker:
> docker compose up --build

Este comando irá buildar a imagem docker da aplicação contendo o servidor FastAPI (Uvicorn) e o banco de dados relacional PostgreSQL, caso seja a primeira vez que o projeto é buildado, será inserido no banco as roles de admin e user e também o usuário administrador.

Assim é possível testar o servidor em _http://localhost:8000_ e a documentação Swagger em _http://localhost:8000/docs_ ou _http://localhost:8000/redoc_

Ainda, é possível configurar e rodar os testes com:
> ./source setup_test.sh

> task tesk

### Modelagem de dados
![Data modeling](/modeling.png)

### Equipe
Dirceu
Giordano
Victor Gabriel
Vinícius Yudi