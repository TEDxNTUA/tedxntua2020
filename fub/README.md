# Fub

Fub is a **remote execution and deployment tool**.

It is essentially a wrapper for [Fabric](https://www.fabfile.org/) that
overrides some settings.

## Concepts
### Hosts
*Hosts* are the machines (local or remote) where the commands will be run.
Fub by default connects to the `tedxntua` host, if one exists in the user's [SSH config
file](https://docs.fabfile.org/en/2.5/concepts/configuration.html#ssh-config).
You can edit them in `fub/hosts.py` or override them through the `-H` argument
of the `fub` command (e.g. `fub -H 8.8.8.8 deploy`).

### Stages
*Stages* are the available instances of the application. We currently have two
stages, `staging` and `production`. See [here](https://softwareengineering.stackexchange.com/a/117985)
for an explanation. Stages are defined and configured in `fub/tasks/stages.py`.

### Active stage
*Active stage* is the stage for which a fub command is run. For example,
running `git.pull` when `production` is the active stage, will run a `git pull`
command in the code directory of the production instance.

## Usage
> **Tip**: Run `fub --list` to view all the available commands.

We list the most important commands below:

### `fub staging`
It sets the active stage to `staging`. Shortcut: `fub stag`.

Chain this command with others so that they run with `staging` as the active
stage.

#### Example
```
fub staging git.pull
```

### `fub production`
It sets the active stage to `production`. Shortcut: `fub prod`.

Chain this command with others so that they run with `production` as the active
stage.

#### Example
```
fub prod deploy
```

### `fub deploy`
Runs the deploy pipeline for the instance of the active stage, which by default
is the `staging` for the `deploy` command.

It executes the following functionality:
* Fetches the `master` branch of the main repository and applies the changes.
* Installs any new Python dependencies.
* Installs any new npm dependencies.
* Creates production build for frontend.
* Runs `collectstatic` command of Django.
* Compiles any new translations.
* Applies any new migrations.
* Restarts application server.

> **Tip**: Run `fub --help TASK` to read the documentation and the arguments of a
given task.

## Differences with Fabric
* The tasks are run by calling `fub task1 task2` instead of `fab task1 task2`.
* The task scripts are stored in `fub/tasks` instead of a `fabfile.py` script.
* Overridden arguments:
    * `prompt_for_passphrase` is set to `True` by default.

### How it works
Fabric by default adds a [console script](https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html)
to your project with the name `fab`.

Fub does the same in the `setup.py` by pointing to the `fub/main.py` module,
where Fub is created as a [`Fab`](https://github.com/fabric/fabric/blob/2.5/fabric/main.py)
subclass, which in turn is an [`invoke.Program`](http://docs.pyinvoke.org/en/1.1/concepts/library.html#reusing-as-a-binary)
subclass.
