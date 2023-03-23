# Deslocamento de Gestantes entre Municípios no Brasil
> Análise do Acesso ao Parto Hospitalar pelo SUS na Década de 2010

A interative dashboard made with Streamlit.

## How to run

1. Clone the repository in the `dashboard` branch:
$ `git clone -b dashboard https://github.com/lucaslopes/ufrj-analytica.git `

2. Create a virtual environment for the project:
$ `python3 -m venv env`

3. Enter in project directory:
$ `cd ufrj-analytica`

4. Activate virtual environment:
$ `source env/bin/activate`

5. Update pip:
$ `pip install --upgrade pip`

6. Install dependencies:
$ `pip install -r requirements.txt`

7. Download required databases:
$ `python data_load.py`

8. Run the Dashboard:
$ `streamlit run app.py`