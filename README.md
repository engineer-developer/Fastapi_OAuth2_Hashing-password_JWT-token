# Fastapi authentication 

#### Authentication type: *"OAuth2 password BEARER with JWT-token"*

###### *username, password, jwt-token are used*

---

>### Prepare virtual enviroinment
>##### The project uses poetry to install dependencies
>
>* To install dependencies in project dir run shell-command:
>
>```
>POETRY_VIRTUALENVS_IN_PROJECT=true poetry shell
>```
>
>* then run next command:
>
>```
>poetry install
>```

>### Prepare database
>##### The postgres database is used for data storage
>
>* For launch postgres database in docker container run command:
>
>```
>docker compose up -d
>```


>### Prepare environments
>##### Needed environments are placed in *.env* file
>
>* You must create and fill in the **.env** file by analogy with the **.env.template** file

>### Run project
>##### You can run project with shell-command:
>
>```
>python src/loader.py
>```
>### Logging as admin
>##### You can log as admin with follow credentials:
>* username = admin@example.com
>* password = 1234567890

>### The tests are implemented with pytest
> ##### To be able to run tests you should have database with name "*pytest_db*".
>* Example SQL commands to create database:
>```
>CREATE DATABASE "pytest_db";
>```
