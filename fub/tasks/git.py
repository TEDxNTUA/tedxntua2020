from fabric import task

from .utils import task_factory


@task(help={
    'force': 'Use `reset --hard` instead of `pull` for syncing with origin',
})
def pull(c, force=False):
    """
    Sync master with origin.

    Returns
    -------
    old_head : str
        Hash of HEAD before syncing.
    new_head : str
        Hash of new HEAD after syncing.
    """
    old_head = c.run('git rev-parse HEAD', hide='out').stdout.strip()
    if force:
        c.run(
            'git fetch && git checkout master && git reset --hard origin/master',
            hide='out',
        )
    else:
        c.run('git checkout master && git pull origin master', hide='out')

    new_head = c.run('git rev-parse HEAD', hide='out').stdout.strip()
    return old_head, new_head

def check_files_changed_factory(path):
    def func(c, old_head, new_head):
        out = c.run(
            f'git diff --name-only {old_head} {new_head} -- {path}',
            hide='out',
        )
        return bool(out)

    return func

check_translations_changed = check_files_changed_factory('*.po')
check_migrations_changed = check_files_changed_factory('*/migrations/*.py')
check_python_deps_changed = check_files_changed_factory('requirements.txt')
check_npm_deps_changed = check_files_changed_factory('bundles/package.json')
