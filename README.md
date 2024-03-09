# Wymieniamy się książkami

A book exchange application.
Database: https://console.neon.tech/app/projects/fragrant-rice-35415342
Deployment environment: https://wymieniamy-sie.vercel.app/

## Installation (local development)

### Prerequisites

- [Python 3.9](https://www.python.org/)
- [pipenv](https://pipenv.readthedocs.io/en/latest/)
- PostgreSQL database

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

### Cleaning and importing data

Run scripts:

```
data/clean_data_books.ipynb
```

```
python manage.py import_books
```