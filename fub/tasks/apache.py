from fabric import task

from . import hosts
from .utils import check_for_stage


@task(hosts=hosts.DEFAULT_HOSTS)
@check_for_stage
def set_private(c):
    """Add password protection to active stage."""
    with c.cd(c.subdomain_root):
        c.run('cp private.htaccess .htaccess', hide='out')

@task(hosts=hosts.DEFAULT_HOSTS)
@check_for_stage
def set_public(c):
    """Remove password protection from active stage."""
    with c.cd(c.subdomain_root):
        c.run('cp public.htaccess .htaccess', hide='out')

@task(hosts=hosts.DEFAULT_HOSTS)
@check_for_stage
def restart_django(c):
    """Restart Django instance."""
    with c.cd(c.subdomain_root):
        c.run('python3 passenger_wsgi.py', hide='out')
