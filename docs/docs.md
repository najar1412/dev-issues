# Issues
# Extended documentation
---

## Installation

Installation is done in 3 parts. Database set up, software setup and configuration.

### Database
Issues uses sqlalchemy and postgres for the database. It may or may not work with other databases that sqlalchemy supports.


>Create a postgres database called `issues` and set permissions
>```
>$ sudo -u postgres psql
>postgres=# CREATE DATABASE issues;
>postgres=# CREATE USER postgres_username WITH PASSWORD 'postgres_password';
>postgres=# ALTER ROLE postgres_username SET client_encoding TO 'utf8';
>postgres=# ALTER ROLE postgres_username SET default_transaction_isolation TO 'read committed';
>postgres=# ALTER ROLE postgres_username SET timezone TO 'UTC';
>postgres=# GRANT ALL PRIVILEGES ON DATABASE issues TO >postgres_username;
>```

### Software

Virtual env is via ana/miniconda. Dependences are located in `/environment.yml`. This can easily be changed into `requirements.txt`, for pip.

>Build and install environment.
>```shell
>~/dev_issues$ conda create env
>```

>Activate.
>```shell
>~/dev_issues$ source activate issues_env
>(issues_env):~/dev_issues/$
>```

>Start up api
>```shell
>(issues_env):~/dev_issues/$ cd issues_api
>(issues_env):~/dev_issues/issues_api/$ python api.py
>```

###### Optional

>Start up frontend
>```shell
>(issues_env):~/dev_issues/$ cd issues
>(issues_env):~/dev_issues/issues/$ python app.py
>```

### Configuration

Currently configuration is limited to database location and logon information.

All config files should be located in `/issues_api/config`

>cred.py
>```python
>"""postgressql database info"""
>username = 'postgres_username'
>password = 'postgres_password'
>ip = '127.0.0.1'
>ip_local = '127.0.0.1'
>```
