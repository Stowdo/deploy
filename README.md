
# Stowdo Deploy

Provides some Python scripts and a docker-compose file to deploy, scale and update Stowdo services.

## Requirements

This project requires at least [Python 3.8](https://www.python.org/downloads/), [Pipenv](https://pypi.org/project/pipenv/) and [Docker Compose](https://docs.docker.com/compose/install/).

For Debian users, you can run the following commands to install Pipenv and Python 3.8 and Docker Compose:

```bash
$ apt install python3.8 pipenv docker-ce
$ sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
$ sudo chmod +x /usr/local/bin/docker-compose
```

> For older Debian versions or Ubuntu based distributions, `docker-ce` exists under the name `docker.io` or `docker`.

> Scripts found in `scripts` folder are made to work on GNU/Linux distributions. **They may not work on other operating systems**.

## Installation

First clone this repo:

```bash
$ git clone git@github.com:Stowdo/deploy.git
$ cd deploy
```

Install Python dependencies:

```bash
$ pipenv install
```

## Before running scripts

First navigate to the project root directory:

```bash
$ cd path/to/stowdo/deploy
```

Enter the virtual environment created by Pipenv:

```
$ pipenv shell
```

You can now use scripts provided!

## Usage

First setup the environment variables and create required folders:

```bash
$ ./scripts/setup.py
```

Then start all the containers:

```bash
$ ./scripts/start.py
```

You can scale (down or up) a service:

```bash
$ ./scripts/scale.py SERVICE SCALE
```

You can also update a service while running. The old containers will be shut down and destroyed after restarting the new ones. Load balancing will automatically redirect request to new containers without interruption.

```bash
$ ./scripts/update.py [OPTIONS] SERVICE VERSION
```

Finally you can shutdown Stowdo containers:

```bash
$ ./scripts/stop.py
```

## Environment Variables

Local environment variables are stored in `.env` file.

### Backend related variables

**`STOWDO_VERSION`**

The version of Stowdo API to deploy.

**`STOWDO_SECRET_KEY`**

A string used by Django to encode sensitive data. Default is auto-generated.

**`STOWDO_ENVIRONMENT`**

The current environment for Stowdo API. Should be `DEVELOPMENT` or `PRODUCTION`. Default is `PRODUCTION`.

**`STOWDO_DB_NAME`**

The name of the database to store data. Default is `stowdo_api`.

**`STOWDO_DB_HOST`**

The hostname or address of the database to connect. Default is `db`.

**`STOWDO_DB_PORT`**

The port to use to connect to the database. Default is `5432`.

**`STOWDO_DB_USER`**

The user of the database. Default is `stowdo_api`.

**`STOWDO_DB_PASSWORD`**

The password used to authenticate to the database. Default is auto-generated.

**`MINIO_HOST`**

The hostname or address with the port of the Minio database. Default is `minio:9000`.

**`MINIO_ACCESS_KEY`**

The public access key used to authenticate to the Minio database. Default is auto-generated.

**`MINIO_SECRET_KEY`**

The secret key used to secure the connection with the Minio database. Default is auto-generated.

### Frontend related variables

**`NODE_ENV`**

The current environment for Stowdo frontend. Should be `DEVELOPMENT` or `PRODUCTION`. Default is `PRODUCTION`.

**`REACT_APP_STOWDO_VERSION`**

The version of Stowdo API to deploy.

**`REACT_APP_STOWDO_API_HOST`**

The hostname or address to Stowdo API used by frontend. Default is `api.stowdo.tk`.

**`REACT_APP_STOWDO_API_PORT`**

The port to use to connect to Stowdo API. Default is `8000`.

**`REACT_APP_STOWDO_API_PROTOCOL`**

The protocol to use to connect to Stowdo API. It should be `http` or `https`. Default is `https`.