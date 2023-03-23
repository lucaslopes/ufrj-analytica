# Deslocamento de Gestantes entre Municípios no Brasil
> Análise do Acesso ao Parto Hospitalar pelo SUS na Década de 2010

A interative dashboard made with Streamlit.

## How to run

Clone the repository in the `dashboard` branch:
$ `git clone -b dashboard https://github.com/lucaslopes/ufrj-analytica.git `

Create a virtual environment for the project:
$ `python3 -m venv env`

Activate virtual environment:
$ `source env/bin/activate`

Update pip:
$ `pip install --upgrade pip`

Install dependencies:
$ `pip install -r requirements.txt`

Download required databases:
$ `python data_load.py`

Run the Dashboard:
$ `streamlit run app.py`