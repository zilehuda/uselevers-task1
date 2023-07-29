# Bill Service

This repository contains the code for FastAPI with SQL filters (Public) (https://uselevers.notion.site/FastAPI-with-SQL-filters-Public-1bcffc3c24f042519093373b526666cd)
It provides functionalities such as:

- Add new bill with sub bills
- Fetch bills with filter reference, total_from, total_to

## Directory Structure

The repository has the following directory structure:

````
.
|-- Dockerfile
|-- alembic
|   |-- ....
|-- alembic.ini
|-- app
|   |-- __init__.py
|   |-- api
|   |   |-- __init__.py
|   |   `-- bills_api.py
|   |-- config.py
|   |-- database.py
|   |-- main.py
|   |-- models.py
|   |-- repositories
|   |   |-- __init__.py
|   |   `-- bill_repository.py
|   |-- schemas.py
|   |-- services
|   |   |-- __init__.py
|   |   `-- bill_service.py
|   `-- utils
|       |-- base_model.py
|       `-- base_repository.py
|-- conftest.py
|-- docker-compose.yml
|-- readme.md
|-- requirements.txt
|-- testdbconfig.py
|-- tests
|   |-- __init__.py
|   |-- factories.py
|   `-- test_apis
|       |-- test.sqlite
|       `-- test_bills.py
````

# Installation

To install and run the app using Docker Compose, follow these steps:

1. Create a new file named `.env` from `.env.example` using a text editor:

```bash
cp .env.example .env
```

2. Open the .env file in a text editor and define the necessary environment variables.
   These variables are used to configure the application. You can use the following content

```bash
DATABASE_URL=postgresql+psycopg2://admin:password@db_service:5432/bill_db
DB_USER=admin
DB_PASSWORD=password
DB_NAME=bill_db
PGADMIN_EMAIL=admin@admin.com
PGADMIN_PASSWORD=admin
```

3. Build and start the Docker containers using Docker Compose:

```bash
docker-compose up -d
```

This command will build the Docker image and start the containers in detached mode.

4. Verify that the containers are running:

```bash
docker-compose ps
```

You should see the running containers listed

4. Now run the migrations using alembic in docker container:

```bash
docker-compose run --rm api alembic upgrade head
```

6. The app will now be accessible at http://localhost:8000.

- To access API doc: http://localhost:8000/docs
- To access pgadmin: http://127.0.0.1:5050/

You can use tools like cURL, Postman, or any other HTTP client to interact with the API endpoints.

# Code Quality and Standards

### Code Linting

Check `app` linting

```bash
ruff app
```

To fix linting issues

```bash
ruff --fix app
```

# Run Tests

Run the tests using pytest in docker:

```bash
docker-compose run --rm api pytest
```

This command will discover and execute all the tests in the project.

If you want to generate a coverage report to see the test coverage,
you can use the --cov option:

```bash
docker-compose run --rm api pytest --cov=app
```

The coverage report will show which parts of the code are covered by the tests.

Current the test coverage is 87%

```bash
                                 
Name                                  Stmts   Miss  Cover
---------------------------------------------------------
app/__init__.py                           0      0   100%
app/api/__init__.py                       0      0   100%
app/api/bills_api.py                     22      0   100%
app/config.py                            10      0   100%
app/database.py                          13      4    69%
app/main.py                               8      0   100%
app/models.py                            12      0   100%
app/repositories/__init__.py              0      0   100%
app/repositories/bill_repository.py      37     10    73%
app/schemas.py                           22      0   100%
app/services/__init__.py                  0      0   100%
app/services/bill_service.py             36      9    75%
app/utils/base_model.py                   7      0   100%
app/utils/base_repository.py              5      0   100%
---------------------------------------------------------
TOTAL                                   172     23    87%

```
