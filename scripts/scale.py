#!/usr/bin/env python3

import click
import subprocess


@click.command()
@click.argument('service')
@click.argument('scale')
def main(service, scale):
    """Scale a Stowdo service."""
    
    if service in ('api', 'app'):
        click.echo(f'Scaling {service} to {scale} container(s)...')
        if subprocess.call([
            'docker-compose',
            'up',
            '-d',
            '--no-deps',
            '--scale',
            f'{service}={scale}',
            '--no-recreate',
            f'{service}'
        ]):
            click.echo('An error occured while scaling Stowdo', err=True)
        else:
            click.echo('Done')
    else:
        click.echo(f'Unknown service {service}', err=True)


if __name__ == '__main__':
    main()