#!/usr/bin/env python3

import click
import subprocess


@click.command()
def main():
    """Stop docker compose"""
    click.echo('Stopping Stowdo containers...')
    subprocess.call(['docker-compose', 'down'])
    click.echo('Done')


if __name__ == '__main__':
    main()