# Anonymization Application
---------------------------------------------------------
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This is a backend part of the anonymization project that will contain all the backend logics and provide with all the required REST APIs.

## Instructions to setup project locally.

### Pre-requisites:
- Python Programming Language (version >= 3.7.4)
- PostgreSQL & PgAdmin

### STEP: 1
- Clone the repo and navigate into the project.
- Create a virtual environment for python. Use the following commands depending upon the environment:

    For Windows:    

        `python -m venv <virtual env name>`

    For Linux based OS:

        `virtualenv  <virtual env name>`

- Setup the following environment variables carefully.
```
SECRET_KEY = "A 128 bit long string containing alphanumeric chars and symbols."

DEBUG = Set it True to enable debug output (Local Testing only)

ENVIRONMENT = To be set only for either staging or production as PROD or STAG (no need for local environment)
```


### Step: 2
- Activate the virtual environment and run the following commands.

```python
pip install -r requirements.txt
```

> NOTE: incase of any error for using `pip` replace it with `pip3`

> Note: Incase of any errors while installing dependencies check the error for hints and fix it.

### Step: 3
- Make a local.py file as the following path: 

`rest2fa\_settings\local.py`

- Edit the local.py to add your local database settings and JWT token settings for the project. Copy the details to connect to DB in the following manner.

```python
# Database Settings
# Database Settings
import os
from datetime import timedelta

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'rest2fa',
        'USER': 'postgres',
        'PASSWORD': 'edc567',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': os.environ.get('SECRET_KEY'),
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}
```

### Step: 4
- Run following commands to setup the database tables.
```python
python manage.py makemigrations accounts
python manage.py migrate
```

- Run following command to create a superuser to access the database through django admin.
```python
python manage.py createsuperuser
```
> Fill all the details for the superuser.

### Step: 5
- Run following command to start the server.
```python
python manage.py runserver
```

----------------------------------------------------------------

<span style="text-align: center;"> THE END </span>

-----------------------------------------------------------------------------------