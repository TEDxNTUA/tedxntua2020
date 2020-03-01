from fabric import task


@task(
    aliases=['stag'],
)
def staging(ctx):
    """
    Set staging as the active stage.
    """
    ctx._stage = 'staging'
    ctx.code_path = '~/project2020dev'
    ctx.subdomain_root = '~/subdomains/2020dev'
    ctx.venv_bin_path = '~/virtualenv/subdomains/2020dev/3.7/bin'
    ctx.passwd_path = '~/.htpasswds/2020dev/passwd'

@task(
    aliases=['prod'],
)
def production(ctx):
    """
    Set production as the active stage.
    """
    ctx._stage = 'production'
    ctx.code_path = '~/project2020'
    ctx.subdomain_root = '~/subdomains/2020'
    ctx.venv_bin_path = '~/virtualenv/subdomains/2020/3.7/bin'
    ctx.passwd_path = '~/.htpasswds/2020/passwd'
