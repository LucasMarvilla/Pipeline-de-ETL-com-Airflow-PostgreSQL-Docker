## Projeto: Pipeline de ETL com Airflowm PostgreSQL e Docker
Tecnologias utilizadas: Python, SQL, Apache Airflow, PostgreSQL/MySQL, Docker, Linux

### Descrição do Projeto:

Este projeto tem como objetivo a construção de um pipeline de ETL (Extração, Transformação e Carga) totalmente automatizado e orquestrado com Apache Airflow em ambiente Docker.

O pipeline realiza a extração de dados de uma API pública de Covid-19, seguida de uma etapa de transformação utilizando Python, onde os dados são tratados e estruturados para posterior análise. Após a transformação, os dados são carregados em um banco de dados relacional (PostgreSQL ou MySQL), organizados em um modelo dimensional simples com tabelas de fatos e dimensões normalizadas.

### Destaques do Projeto:

Utilização do Apache Airflow para agendamento e controle do fluxo de dados, com execução automática dos jobs em diferentes etapas.

Ambiente Dockerizado, garantindo portabilidade, reprodutibilidade e isolamento do ambiente de execução.

Logs detalhados no Airflow, permitindo fácil monitoramento e depuração de falhas.

Aplicação de boas práticas de modelagem de dados com normalização e estruturação em esquema dimensional no banco de dados.
Este guia explica a sequência correta de comandos para subir o Apache Airflow utilizando Docker Compose.

## Pré-requisitos

- Docker e Docker Compose instalados
- Projeto do Airflow com o arquivo `docker-compose.yaml` devidamente configurado

## Passo a passo

### 1. Inicializar o ambiente do Airflow

Antes de subir os containers, é necessário inicializar o Airflow. Esse passo prepara o banco de dados, aplica as migrações e cria o usuário admin padrão.

```bash
docker compose up airflow-init
```

> ⚠️ Este comando deve ser executado **somente na primeira vez** ou sempre que os volumes forem removidos.

### 2. Subir os containers

Depois que a inicialização for concluída com sucesso, você pode subir todos os serviços normalmente:

```bash
docker-compose up -d
```

### 3. Acessar a interface Web do Airflow
1. criar conexão do airflow com postgresql

```bash
docker exec -it projetoairflow-airflow-scheduler-1 airflow connections add 'postgres_etl' --conn-uri 'postgresql+psycopg2://airflow:airflow@postgres:5432/airflow'
```

2. A interface web geralmente estará disponível no seguinte endereço:


[http://localhost:8080]


Use as credenciais criadas durante a inicialização (`airflow-init`) para fazer login.
3. Faça login com as credenciais definidas no `.env`:
   - **Username:** `airflow`
   - **Password:** `airflow`

## Observações

- Se ocorrerem erros após subir os containers, verifique se o `airflow-init` foi executado com sucesso.
- Para parar e remover os containers, utilize:

```bash
docker-compose down
```
### 🔗 Conexão ao PostgreSQL via pgAdmin

1. Acesse o pgAdmin no navegador:  
   [http://localhost:5050]

2. Faça login com as credenciais definidas no `.env`:
   - **Email:** `admin@admin.com`
   - **Senha:** `admin`

3. Clique com o botão direito em “Servers” > **Create** > **Server**.

4. Na aba **General**, defina um nome como:
   - `Projeto` ou o que preferir.

5. Na aba **Connection**, insira:
   - **Host name/address:** `postgres`  
   - **Port:** `5432`  
   - **Username:** `airflow`  
   - **Password:** `airflow`
   - **database:** `airflow`  
   - Marque a opção **Save Password**.

6. Clique em **Save**. Agora você pode acessar o banco `Projeto`.

### 🔗 visualização no PostgreSQL via pgAdmin

1. expende servers -> airflow -> schemas -> tables -> covid_paises
