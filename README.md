# Wymieniamy się książkami

A book exchange application.

## Installation (local development)

### Prerequisites

- [Python 3.11](https://www.python.org/)
- [pipenv](https://pipenv.readthedocs.io/en/latest/)
- SQLite or another database

### Installation instructions

1.  Install the Python requirements and enter the virtual environment:

    ```
    pipenv install --dev
    pipenv shell
    ```

2.  Configure your local database by filling out `DJANGO_DATABASE_URL` setting in `.env` file.

    If there is no good reason to do otherwise, it should be a [Postgres](https://www.postgresql.org/) database since that's what we are using by default on production servers.

3.  Run database migrations:

    ```
    python manage.py migrate
    ```

4.  Start the backend dev server (in a different console):

    ```
    python manage.py runserver
    ```
