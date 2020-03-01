from fabric import task

from . import console, hosts
from .utils import source_profile, check_for_stage


@task(hosts=hosts.DEFAULT_HOSTS)
@check_for_stage
def set_private(c):
    """Add password protection to active stage."""
    with c.cd(c.subdomain_root):
        c.run('cp private.htaccess .htaccess', hide='out')
    console.done('Enabled password protection')

@task(hosts=hosts.DEFAULT_HOSTS)
@check_for_stage
def set_public(c):
    """Remove password protection from active stage."""
    with c.cd(c.subdomain_root):
        c.run('cp public.htaccess .htaccess', hide='out')
    console.done('Disabled password protection')

@task(hosts=hosts.DEFAULT_HOSTS)
@check_for_stage
def restart_django(c):
    """Restart Django instance."""
    console.status('Restarting Django application')
    with c.cd(c.subdomain_root):
        c.run(f'{c.venv_bin_path}/python passenger_wsgi.py', hide='out')
    console.done('Restarted')
