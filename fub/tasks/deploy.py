from fabric import task

from . import apache, django, git, npm, hosts
from .utils import check_for_stage


@task(
    help={
        'pull': 'Use `pull` instead of `reset --hard` for syncing with origin',
    },
    hosts=hosts.DEFAULT_HOSTS,
)
@check_for_stage(use_default='staging')
def deploy(c, pull=False):
    """
    Run deploy pipeline.
    """
    with c.cd(c.code_path):
        old_head, new_head = git.pull(c, force=not pull)
        if old_head == new_head:
            return

        # Check for updated dependencies
        if git.check_python_deps_changed(c, old_head, new_head):
            django.install_python_deps(c)
        if git.check_npm_deps_changed(c, old_head, new_head):
            npm.install_npm_deps(c)

        npm.build_production(c)
        django.collect_static(c)

        if git.check_translations_changed(c, old_head, new_head):
            django.compile_translations(c)
        if git.check_migrations_changed(c, old_head, new_head):
            django.migrate(c)

        # Restart Django
        apache.restart_django(c)
