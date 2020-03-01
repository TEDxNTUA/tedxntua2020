from fabric import task

import hosts
from utils import console, source_profile, check_for_stage


@task(
    help={'user': 'Username'},
    hosts=hosts.DEFAULT_HOSTS,
)
@check_for_stage()
def add_auth(c, user):
    """
    Create user for passwd authentication.
    """
    c.run(f'mkdir -p $(dirname {c.passwd_path})')
    c.run(f'htpasswd -c {c.passwd_path} {user}')
    console.done(f'Added user {user}')

@task(hosts=hosts.DEFAULT_HOSTS)
@check_for_stage()
def set_private(c):
    """Add password protection to active stage."""
    with c.cd(c.subdomain_root):
        c.run('cp private.htaccess .htaccess', hide='out')
    console.done('Enabled password protection')

@task(hosts=hosts.DEFAULT_HOSTS)
@check_for_stage()
def set_public(c):
    """Remove password protection from active stage."""
    with c.cd(c.subdomain_root):
        c.run('cp public.htaccess .htaccess', hide='out')
    console.done('Disabled password protection')
