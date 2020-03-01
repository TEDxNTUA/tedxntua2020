from fabric import task

import hosts
from utils import check_for_stage, console


CLOUDLINUX_SELECTOR_PATH = '/usr/sbin/cloudlinux-selector'

@task(hosts=hosts.DEFAULT_HOSTS)
@check_for_stage()
def restart_application(c, app_root):
    """Restart Cloudlinux Python application."""
    console.status(f'Restarting {app_root} application')
    c.run(f'{CLOUDLINUX_SELECTOR_PATH} restart --interpreter python '
          f'--app-root {app_root} --user tedxntua --json',
          hide='out')
    console.done('Restarted')
