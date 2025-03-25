# GiveLink
Servidor do trabalho de experiência criativa - 5º período BSI PUCPR.
## Configuração e como rodar o projeto
### Requisitos
* Docker/Docker Desktop
### Configuração
Rode o comando para buildar a aplicação com Docker:
> docker compose up --build

Assim é possível testar o servidor em _http://localhost:8000_ e a documentação Swagger em _http://localhost:8000/docs_

Ainda, é possível rodar os testes com:
> task test

### Modelagem de dados
![Data modeling](/modeling.png)