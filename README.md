# API Test
> A Toy API

## Routes

- `/age`: Recebe o nome de uma pessoa (name), sua data de nascimento (birthdate) e uma data qualquer no futuro (date) e retorna uma frase no formato indicado, com a idade X que a pessoa tem no momento da requisição e a idade Y que ela terá na data do futuro. Lembre-se de adicionar verificações para garantir que o body está completo e que a data date é realmente no futuro. Caso contrário, retorne um erro detalhado.

- `/album-info`: Recebe o nome de um artista (NOME-DO-ARTISTA) e, utilizando a API do AudioDB, deve retornar o nome do último álbum do artista e as faixas dele. No caso de não encontrar o artista pelo nome, deve retornar um erro. No caso de haverem mais de um álbum do mesmo ano, retorne qualquer um deles

## How to run

1. Clone the repository in the `api` branch:
$ `git clone -b api https://github.com/lucaslopes/ufrj-analytica.git `

2. Enter in the project directory:
$ `cd ufrj-analytica`

3. Create a virtual environment for the project:
$ `python3 -m venv env`

4. Activate virtual environment:
$ `source env/bin/activate`

5. Update pip:
$ `pip install --upgrade pip`

6. Install dependencies:
$ `pip install -r requirements.txt`

7. Run the API in a terminal tab:
$ `python app.py`

8. Run the Tests in other terminal tab while the API is running:
$ `pytest`

9. You can see more use examples by running:
$ `python tests/test_album.py`