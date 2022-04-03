#!/usr/bin/env python3

import click
import dotenv
import re
import subprocess
import time


@click.command()
@click.argument('service')
@click.argument('version')
@click.option('--scaledelay', default=20)
def main(service, version, scaledelay):
    """Deploy new version of Stowdo."""

    SERVICE_TO_VERSION = {
        'api': 'STOWDO_VERSION',
        'app': 'REACT_APP_STOWDO_VERSION',
    }
    
    if service in ('api', 'app'):
        click.echo(f'Updating {service} to v{version}...')

        dotenv_file = dotenv.find_dotenv()
        dotenv.load_dotenv(dotenv_file)
        dotenv.set_key(dotenv_file, SERVICE_TO_VERSION[service], version, quote_mode='never')

        service_names = subprocess \
            .check_output(['docker', 'ps', '-a', '--format', '\'{{.Names}}\'']) \
            .decode() \
            .split('\n')

        current_scale = 0
        for service_name in service_names:
            if re.match(fr'stowdo_{service}_\d+', service_name[1:-1]):
                current_scale += 1

        old_containers = subprocess.check_output([
            'docker-compose',
            'ps',
            '-q',
            f'{service}'
        ]).decode().split('\n')[:-1]
        
        subprocess.call([
            'docker-compose',
            'up',
            '-d',
            '--no-deps',
            '--scale',
            f'{service}={current_scale * 2}',
            '--no-recreate', 
            f'{service}',
        ])

        time.sleep(scaledelay)

        for old_container in old_containers:
            subprocess.call(['docker', 'stop', f'{old_container}'])
            subprocess.call(['docker', 'rm', f'{old_container}'])

        subprocess.call([
            'docker-compose',
            'up',
            '-d',
            '--no-deps',
            '--scale',
            f'{service}={current_scale}',
        ])

        click.echo('Done')
    else:
        click.echo(f'Unknown service {service}', err=True)


if __name__ == '__main__':
    main()