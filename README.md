# devops-pipeline-python-data-model-example

[![python](https://img.shields.io/badge/python-v3.7.X-green.svg)](https://www.python.org/)
[![pip](https://img.shields.io/badge/pip-v18.1-yellow.svg)](https://pypi.org/project/pip/)
[![docker](https://img.shields.io/badge/docker-v19.03.X-blue.svg)](https://www.docker.com/)
[![docker-compose](https://img.shields.io/badge/docker_compose-v1.24.X-blue.svg)](https://docs.docker.com/compose/)

>A simple Python project to test ADL DevOps Data Model Pipelines.
>A project to provide code to the data scientists to update the pipeline. Based on data-commons-integration-template
>
>Developed with all :heart: in the world by ADL DevOps team

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Test](#test)

## Prerequisites

You will need the following things properly installed on your computer.

* [Git](http://git-scm.com/)
* [Docker](https://docs.docker.com/compose/install/)
* [Docker-compose](https://docs.docker.com/compose/install/)
* [Pre-commit](https://pre-commit.com/#install)
* [Virtual-environment](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/)

### Installation

* `git clone git@github.com:avaldigitallabs/devops-pipeline-python-data-model-example.git` this repository
* change into the new directory `cd devops-pipeline-python-data-model-example`

You will need to run:

```bash
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

### Test

```bash
$pytest
```

### Run with jobs

```bash
python main.py --job=dummy
```

## Run with Docker

### Build Docker Environment

```bash
docker build -t image_name:tag .
```

### Run with Docker container

```bash
docker run image_name:tag python main.py --job=dummy
```

### Run test with Docker container

```bash
docker run image_name:tag pytest
```

## Code Style & Quality Checker

```bash
$ flake8 .

$ black .

$ pylint $module_folder
```

## Unit Test Coverage

```bash
$ pytest --cov=bocc_data_pipeline/ tests/
```

## Contributing

If you find this repo useful here's how you can help:

1. Send a Merge Request with your awesome new features and bug fixes
2. Wait for a Coronita :beer: you deserve it.

## Further Reading / Useful Links

* [Docker](https://www.docker.com/get-started)
* [Docker-compose](https://docs.docker.com/compose/gettingstarted/)


### Usage

Replace variables <name_use_case> <stack> in the file config.ini, with the values from your project

```
Usage: main.py [OPTIONS]

Options:
  --job TEXT                    Job name  [prep, fe, scoring, training]
  --period TEXT                 Starting Year Month day (yyyy-mm-ddThh:mm:ssZ)
  --aws_job_id TEXT             number sent by the event that launches the execution, for testing place a random number (10)
  --env TEXT                    'dev' for development, 'prod' for production environment, 'stg for stage environment 'ds' for Data Sciences
```

## Run in local environment
Create virtual environment with your favorite method.

### (optional) Pro tip: pyenv + pipenv
Pipenv Doc: https://docs.pipenv.org/en/latest/

pyenv + pipenv:

- https://hackernoon.com/reaching-python-development-nirvana-bb5692adf30c
- https://gioele.io/pyenv-pipenv

### Run with local environment Preparation
```
python main.py --job=prep --period=2022-02-16T14:55:15Z --aws_job_id=10 --env=dev
```

### Run with local environment Feature Engineering
```
python main.py --job=fe --period=2022-02-16T14:55:15Z --aws_job_id=10 --env=dev
```

### Run with local environment Scoring
```
python main.py --job=scoring --period=2022-02-16T14:55:15Z --aws_job_id=10 --env=dev
```
