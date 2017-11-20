# agent-quotes
Web service to allow agents to efficiently perform customer quotes

## Preface
The product has been designed following the django-cookiecutter layout recommended by Daniel Roy Greenfield, author of Two Scoops of Django for Django best practices.

The directory structure is as follows:
```
- agent-quotes
    - agent
        - core # core application that this feature is built on
        - quote # quote application
        - static # static files directory
        - templates # templates directory
    - config
        - settings # settings for base, local, prod, test
    - requirements # requirements for base, local, prod, test
```

The agent quoting process described in the challenge has been set up by allowing agents to view details on their quotes within a dashboard interface. Agents can overview completed quotes and new quotes and navigate to either quote type in order to visualize quote data. Agents can click "Start Quote!" to be provided with quote details and a form that will allow them to enter a price for the current quote. On quote submission, the completed quote will move to the completed quotes table in the interface and out of the new quotes table in the interface and the agent will be redirected back to the new quotes table to continue completing new quotes.

This feature has been implemented in this way to allow agents to not only complete the quoting process but also to allow them to visualize their progress as they complete quotes. With this functionality, agents will feel more accomplished and will be able to see their quotes like tasks on a kanban board.

Further data could be added to the Quote model to allow for further inspection of the customer quote on the agent quoting page.

# Usage
Currently setup for python 3.6

## Create a Virtual Environment
```
cd agent-quotes
mkvirtualenv --python=$(which python3) agent-quotes
pip install -r requirements/local.txt
```

## Setup Up Postgres
1. Install Postgres [On a Mac: https://postgresapp.com/] - make sure to install the CLI tools as well.
2. Create a database with the dev credentials
```
# create user databaseuser with password 'databasepass';
# create database databasename;
# grant all privileges on database databasename to databaseuser;
```

3. Set up .env file in your local repository
```
vi .env
```
It should look something like this, except for with production credentials.
```
DEBUG=on
SECRET_KEY=SECRET_KEY
DATABASE_URL=psql://databaseuser:databasepass@127.0.0.1:5432/databasename
```
In our example case, it will look like so:
```
DEBUG=on
SECRET_KEY=SECRET_KEY
DATABASE_URL=psql://databaseuser:databasepass@127.0.0.1:5432/databasename
```

## Set up environment variables for VirtualEnv (with virtualenvwrapper)
You can automatically set env vars by adding this to ~/.virtualenvs/<your-virt-env-name>/bin/postactivate:
```
export DJANGO_SETTINGS_MODULE=config.settings.local
export DJANGO_READ_DOT_ENV_FILE=True
```

To make sure this gets cleaned up when you deactivate the virtualenv, add the following to ~/.virtualenv/<your-virt-env-name>/bin/postdeactivate:
```
unset DJANGO_SETTINGS_MODULE
unset DJANGO_READ_DOT_ENV_FILE=True
```

## Migrate
```
./manage.py migrate
```

## Load database with Sample Quote Data using management command
```
./manage.py load_quotes
```

## Start up Django
```
./manage.py runserver
```

The page should now be visible at:
`localhost:8000/quote/dashboard/`

It is assumed that this feature would not live at the root URL and so it has all been arranged so that the root URL is vacant and all application features live at quote/.

## API
The API endpoint for agent-specific performance metrics is:
```
localhost:8000/quote/performance/pk/
```
where pk is the primary key of the agent to be assessed.
No authentication is required at this time for read operations but could be added if desired.

## Running Tests
pytest is in use for testing. We can run tests by running:
```
pytest
```
from the agent-quotes directory.
To run tests on specific applications, run:
```
pytest path/to/app
```
e.g
```
pytest agent/quote
```
Use the -s argument to account for ipdb statements when debugging


## Installing Linters
This repositiory is using Flake8 for Python Linting.
```
# outside your virtualenv
pip install flake8

# find your linter file
hash -r
which flake8 # confirm this returns something
```

## CI
```
tox
```

This will execute both py.test and flake8 linting and output the results (including code coverage numbers to stdout).

If you need to refresh your environment for new/outdated dependencies, run:
```
tox -r
```

CircleCI is currently set up for this repository.
