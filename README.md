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

2.  Configure your local database by filling out `DATABASES` setting in `settings.py` file.

3.  Run database migrations:

    ```
    python manage.py migrate
    ```

4.  Start the backend dev server (in a different console):

    ```
    python manage.py runserver
    ```
