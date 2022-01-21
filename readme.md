# Twinkly backend assignment

[![GitHub Super-Linter](https://github.com/nicolamoro/twinkly-assignment/workflows/Build/badge.svg)](https://github.com/marketplace/actions/super-linter)

## Requirements

First of all, you should create a virtual environment for installing project dependency. In order to do this you need to run:

```
virtualenv .venv
```

To install python project dependencies run:

```
cd src
pip install -r requirements.txt
```

## Environment

To run the project you need to set some environment variable. In order to do this you can create a `.env` file into the root of the project, starting from the `.env-sample` file as an example.
For a complete list of all environment variables supported take a look at the `src/config.py` file.

## Run project

To start project in development run:

```
cd src/
python app.py
```

To start project using docker:

```
docker build --pull --no-cache -t twinkly-assignment:0.1.0 -f Dockerfile .
docker run --env-file .env -p 8888:8888 -ti --rm twinkly-assignment:0.1.0
```

## Linters

To verify that imports are correctly formatted run:

```
cd src/
isort --skip=_deps --multi-line=3 --trailing-comma --check-only --diff --stdout .
```

To verify that code is correctly formatted run:

```
cd src/
black --exclude="/_deps/" --line-length=120 --check --diff .
```

To check code style consistency run:

```
cd src/
flake8 --exclude=_deps --extend-ignore=E203 --max-complexity=10 --max-line-length=120 .
```

## Unit Testing

To launch unit tests and coverage verification, run:

```
py.test --cov=src --cov-config=.coveragerc --cov-branch --cov-report=xml:cov.xml --cov-report=html:cov_html --cov-fail-under=100 --cov-report=term-missing --showlocals --verbose src/tests/
```

After this command you can check coverage report looking at:

```
cov_html/index.html
```

## API documentation

With service running, you will find documentation about implemented APIs (in Swagger format) browsing:

```
http://localhost:8888/api/1/docs
```

You can also test API calls by using file:

```
api_test/client.http
```

Using [REST Client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) for VS Code you can run them directly from there.
