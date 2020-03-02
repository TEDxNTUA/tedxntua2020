from fabric import task

import hosts
from utils import console, check_for_stage
from . import apache, cloudlinux, django, git, npm


@task(
    help={
        'pull': 'Use `pull` instead of `reset --hard` for syncing with origin.',
        'force': 'Force-run all deploy steps without checking for changes.',
        'build': 'Create new production build.',
    },
    hosts=hosts.DEFAULT_HOSTS,
)
@check_for_stage(use_default='staging')
def deploy(c, pull=False, force=False, build=False):
    """
    Run deploy pipeline.
    """
    console.info(f'Deploying to {c._stage}')
    if c._stage == 'production':
        # Confirm that user wants to deploy to production
        msg = 'Please make sure that you have tested this version in staging ' \
            'to avoid hiccups.\n' \
            'Are you sure you want to continue? [Y/n] '
        if not console.continue_prompt(msg):
            return

    old_head, new_head = git.pull(c, force=not pull)
    if not force and old_head == new_head:
        console.info('No updates found')
        return

    # Check for updated dependencies
    if force or git.check_python_deps_changed(c, old_head, new_head):
        console.status('Python dependencies changed')
        django.install_python_deps(c)
    if force or git.check_npm_deps_changed(c, old_head, new_head):
        console.status('npm dependencies changed')
        npm.install_npm_deps(c)

    if not build:
        console.status('[npm] Skipped creation of production build. Make sure '
            'that you have a current version in the repository. If you need to '
            'let the host handle this, rerun this command with --build. '
            'Use sparingly to avoid exhausting the host resources.')
    else:
        npm.build_production(c)
    django.collect_static(c)

    if force or git.check_translations_changed(c, old_head, new_head):
        console.status('Django translations changed')
        django.compile_translations(c)
    if force or git.check_migrations_changed(c, old_head, new_head):
        console.status('New Django migrations detected')
        django.migrate(c)

    # Restart Django
    # subdomain_root starts with '~/'
    app_root = c.subdomain_root[2:]
    cloudlinux.restart_application(c, app_root)
    console.success('Completed deployment')
