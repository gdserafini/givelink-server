# EC-PSI BSI PUCPR
Servidor do trabalho de experiência criativa - 5º período BSI PUCPR.
## Configuração e como rodar o projeto
### Requisitos
* Python >= 3.12
### Configuração
Na pasta root, crie o ambiente virtual python com:
> python3 -m venv .venv

Ative o ambiente virtual com:
> source .venv/bin/activate

Então instale as dependências necessárias:
> pip install -r requirements.txt

Conforme instalação do taskipy e suas configurações em pyproject.toml, é possível rodar o servidor com:
> task run

Assim é possível testar o servidor em _http://localhost:8000_ e a documentação Swagger em _http://localhost:8000/docs_

Ainda, é possível rodar os testes com:
> task test