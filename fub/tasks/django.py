from fabric import task

from utils import console, source_profile, check_for_stage


TRANSLATIONS = ['el', 'en']

@task
@check_for_stage()
def compile_translations(c):
    """Run `manage.py compilemessages` for supported languages."""
    for lang in TRANSLATIONS:
        c.run(
            f'{c.venv_bin_path}/manage.py compilemessages -l {lang}',
            hide='out',
        )
    console.done('Compiled Django translations')

@task
@check_for_stage()
def migrate(c):
    """Run Django migrations."""
    c.run(f'{c.venv_bin_path}/manage.py migrate', hide='out')
    console.done('Ran Django migrations')

@task
@check_for_stage()
def collect_static(c):
    """Collect static files for Django."""
    c.run(f'{c.venv_bin_path}/manage.py collectstatic --noinput', hide='out')
    console.done('Collected static files')

@task
@check_for_stage()
def install_python_deps(c):
    """Install Python dependencies from requirements.txt."""
    with source_profile(c):
        c.run(f'{c.venv_bin_path}/pip install -r '
              f'{c.code_path}/requirements.txt', hide='out')
    console.done('Installed Python dependencies from requirements.txt')

@task
@check_for_stage()
def install_python_deps_from_setup(c):
    """Install Python dependencies from setup.py."""
    with source_profile(c):
        c.run(f'{c.venv_bin_path}/pip install -e {c.code_path}', hide='out')
    console.done('Installed Python dependencies from setup.py')
