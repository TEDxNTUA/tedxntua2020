from fabric import task

from utils import console, source_profile, check_for_stage


@task
@check_for_stage()
def build_production(c):
    """Run `npm run build` in bundles directory."""
    with source_profile(c), c.cd(f'{c.code_path}/bundles'):
        c.run('npm run build', hide=True)
    console.done('Created production build')

@task
@check_for_stage()
def install_npm_deps(c):
    """Install npm dependencies from package.json."""
    with source_profile(c), c.cd(f'{c.code_path}/bundles'):
        c.run('npm i', hide=True)
    console.done('Installed npm dependencies')
