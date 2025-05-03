# GiveLink
Servidor do trabalho de experiência criativa - 5º período BSI PUCPR.<br>
A GiveLink consiste em uma plataforma onde doadores e instituições como ONGs, hospitais podem se conectar e realizar doações pela plataforma.
## Configuração e como rodar o projeto
### Requisitos
Recomendamos rodar o projeto utilizando o Docker:
* Docker/Docker Desktop

Se deseja rodar o projeto sem o Docker, os requisitos são basicamente:
* pyhton >= 3.12

### Configuração
Para configurar as variáveis de ambiente, adicione as seguintes variáveis no arquivo .env (pasta root):

> DATABASE_URL <br>
> SECRET_KEY <br>
> ALGORITHM <br>
> ACCESS_TOKEN_EXPIRE_MINUTES <br>
> PASSWORD_TEST <br>
> POSTGRES_USER <br>
> POSTGRES_DB <br>
> POSTGRES_PASSWORD <br>

Caso esteja usando o Docker, rode o comando para buildar a aplicação:
> docker compose up --build

Este comando irá buildar a imagem docker da aplicação contendo o servidor FastAPI (Uvicorn) e o banco de dados relacional PostgreSQL.

Se não estiver usando o Docker:
> python3 -m venv .venv

> ./source .venv

> pip install -r requirements.txt

> task run

Com a configuração do projeto em pyproject.toml, o comando task run irá rodar a aplicação.

Caso seja a primeira vez que o projeto é buildado, será inserido no banco as roles de admin e user e também o usuário administrador.

Assim é possível testar o servidor em _http://localhost:8000_ e acessar a documentação Swagger em _http://localhost:8000/docs_ ou _http://localhost:8000/redoc_

Ainda, é possível configurar e rodar os testes com:
> ./source setup_test.sh

> task tesk

### Modelagem de dados
No geral o sistema contem as 5 entidades abaixo, a entidade central do sistema é a donation, no caso, é um entidade relacionamento que representa as doação executadas de um doador para uma instituição, os modelos db estão no arquivo src/models/db_schemas.py.
Os modelos pydantic estão em arquivos específicos na pasta src/models.
![Data modeling](/modeling.png)

### Funcionamento
Abaixo é possível observar o funcionamento geral do sistema em alto nível, divida nas entidades, user, donor e institution onde a entidade relacionamento donation está presente durante a execução da lógica core do sistema.
![Flow](/givelink-flow.png)

### Equipe
* Dirceu
* Giordano
* Victor Gabriel
* Vinícius Yudi
