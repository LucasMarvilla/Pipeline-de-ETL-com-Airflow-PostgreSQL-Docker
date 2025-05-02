from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import requests
import pandas as pd

def criar_tabela(**context):
    hook = PostgresHook(postgres_conn_id='postgres_etl')
    create_sql = """
        CREATE TABLE IF NOT EXISTS covid_paises (
            id SERIAL PRIMARY KEY,
            pais VARCHAR(100),
            casos INTEGER,
            mortes INTEGER,
            recuperados INTEGER,
            data_insercao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """
    hook.run(create_sql)

def extrair_dados():
    url = "https://disease.sh/v3/covid-19/countries"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def transformar_dados(**context):
    raw_data = context['ti'].xcom_pull(task_ids='extrair_dados')
    df = pd.DataFrame(raw_data)

    # Seleciona e renomeia colunas
    df = df[['country', 'cases', 'deaths', 'recovered']]
    df.columns = ['pais', 'casos', 'mortes', 'recuperados']

    registros = list(df.itertuples(index=False, name=None))
    return registros

def carregar_dados(**context):
    registros = context['ti'].xcom_pull(task_ids='transformar_dados')
    hook = PostgresHook(postgres_conn_id='postgres_etl')

    insert_sql = """
        INSERT INTO covid_paises (pais, casos, mortes, recuperados)
        VALUES (%s, %s, %s, %s);
    """
    hook.insert_rows(table='covid_paises', rows=registros, target_fields=['pais', 'casos', 'mortes', 'recuperados'])

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='etl_covid',
    default_args=default_args,
    description='ETL DAG para dados da COVID',
    schedule='@daily',
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    criar_tabela_task = PythonOperator(
        task_id='criar_tabela',
        python_callable=criar_tabela,
    )

    extrair = PythonOperator(
        task_id='extrair_dados',
        python_callable=extrair_dados
    )

    transformar = PythonOperator(
        task_id='transformar_dados',
        python_callable=transformar_dados,
    )

    carregar = PythonOperator(
        task_id='carregar_dados',
        python_callable=carregar_dados,
    )

    # Definindo a ordem das tarefas
    criar_tabela_task >> extrair >> transformar >> carregar
