# Fub: Remote execution and deployment tool

Fub is essentially a wrapper for [Fabric](https://www.fabfile.org/) that
overrides some settings.

## How it works
Fabric by default adds a [console script](https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html)
to your project with the name `fab`.

Fub does the same in the `setup.py` by pointing to the `fub/main.py` module,
where Fub is created as a [`Fab`](https://github.com/fabric/fabric/blob/2.5/fabric/main.py)
subclass, which in turn is an [`invoke.Program`](http://docs.pyinvoke.org/en/1.1/concepts/library.html#reusing-as-a-binary)
subclass.

## Differences with Fabric
* The tasks are run by calling `fub task1 task2` instead of `fab task1 task2`.
* The task scripts are stored in `fub/tasks` instead of a `fabfile.py` script.
* Overridden arguments:
    * `prompt_for_passphrase` is set to `True` by default.
