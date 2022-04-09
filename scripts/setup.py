#!/usr/bin/env python3

import click
import dotenv
import os
import secrets


def get_random_secret_key():
    """
    Return a 50 character random string.
    """
    length = 50
    chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
    return ''.join(secrets.choice(chars) for i in range(length))


@click.command()
def main():
    """Prepare the environment before starting Stowdo."""

    click.echo('Welcome to Stowdo Deploy setup.')
    click.echo('This script will let you define variables for your local environment.')
    click.echo('The proposals in brackets are the default values. Leave blank to use them.')

    secret_key = get_random_secret_key()
    database_key = get_random_secret_key()
    minio_access_key = get_random_secret_key()
    minio_secret_key = get_random_secret_key()

    envs = {
        'COMPOSE_PROJECT_NAME': 'stowdo',
        'STOWDO_VERSION': click.prompt('Backend version', default='1.0.0'),
        'STOWDO_SECRET_KEY': click.prompt(
            'API secret key [default is auto-generated]',
            default=secret_key,
            hide_input=True,
            show_default=False,
        ),
        'STOWDO_ENVIRONMENT': click.prompt('Backend environment', default='PRODUCTION'),
        'STOWDO_DB_NAME': click.prompt('Database name', default='stowdo_api'),
        'STOWDO_DB_HOST': click.prompt('Database host', default='db'),
        'STOWDO_DB_PORT': click.prompt('Database port', default=5432, type=click.types.INT),
        'STOWDO_DB_USER': click.prompt('Database user', default='stowdo_api'),
        'STOWDO_DB_PASSWORD': click.prompt(
            'Database password [default is auto-generated]',
            default=database_key,
            hide_input=True,
            show_default=False,
        ),
        'MINIO_HOST': click.prompt('Minio host', default='minio') \
            + ':' \
            + str(click.prompt('Minio port', default=9000, type=click.types.INT)),
        'MINIO_ACCESS_KEY': click.prompt(
            'Minio access key [default is auto-generated]',
            default=minio_access_key,
            show_default=False,
        ),
        'MINIO_SECRET_KEY': click.prompt(
            'Minio secret key [default is auto-generated]',
            default=minio_secret_key,
            hide_input=True,
            show_default=False,
        ),
        'NODE_ENV': click.prompt('Frontend environment', default='PRODUCTION'),
        'REACT_APP_STOWDO_VERSION': click.prompt('Frontend version', default='1.0.0'),
        'REACT_APP_STOWDO_API_HOST': click.prompt('API host once deployed', 'api.stowdo.tk'),
        'REACT_APP_STOWDO_API_PORT': click.prompt('API port once deployed', '8000'),
        'REACT_APP_STOWDO_API_PROTOCOL': click.prompt('API protocol once deployed', default='https'),
    }

    click.echo('Saving environment variables...')
    dotenv_file = dotenv.find_dotenv()

    if not dotenv_file:
        dotenv_file = '.env'

    dotenv.load_dotenv(dotenv_file)
    
    for key, value in envs.items():
        dotenv.set_key(dotenv_file, key, str(value), quote_mode='never')
    
    click.echo('Done')
    click.echo('Creating data folders...')

    for folder in ('db-data', 'letsencrypt', 'minio-data', 'proxy-data'):
        try:
            os.mkdir(folder)
        except Exception:
            click.echo(f'Unable to create folder {folder}')

    click.echo('Done')


if __name__ == '__main__':
    main()
