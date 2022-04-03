#!/usr/bin/env python3

import click
import subprocess


@click.command()
def main():
    """Start docker compose"""

    click.echo('Starting Stowdo containers...')
    subprocess.call(['docker-compose', 'up', '-d'])
    click.echo('Done')


if __name__ == '__main__':
    main()