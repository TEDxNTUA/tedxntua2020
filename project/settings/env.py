'''
Adopted from Senko Rašić's article "Environment-based Django settings" at GoodCode.io

Link: https://goodcode.io/articles/django-env-settings/
Repository: https://github.com/dobarkod/django-template
'''

import os

__all__ = ['BASE_DIR', 'abs_path', 'env_bool', 'env_str', 'env_list']


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


def env_setting(key, default):
    '''Gets plain value from environment variable'''
    return os.environ.get(key, default)


def abs_path(*args):
    '''Transforms relative path from `args` to absolute path, based on project root directory'''
    return os.path.join(BASE_DIR, *args)


def env_bool(name, default=False):
    '''
    Get a boolean value from environment variable.

    If the environment variable is not set or value is not one or "true" or
    "false", the default value is returned instead.
    '''

    if name not in os.environ:
        return default
    if os.environ[name].lower() in ['true', 'yes', '1']:
        return True
    if os.environ[name].lower() in ['false', 'no', '0']:
        return False
    return default


def env_str(name, default=None):
    '''
    Get a string value from environment variable.

    If the environment variable is not set, the default value is returned
    instead.
    '''

    return os.environ.get(name, default)


def env_list(name, separator=',', default=None):
    '''
    Get a list of string values from environment variable.

    If the environment variable is not set, the default value is returned
    instead.

    When two arguments are given, the function takes two forms:
        - `env_list(name, separator)` if 2nd argument is a string, with [] as default
        - `env_list(name, default)` if 2nd argument is a list, with ',' as separator
    '''
    if isinstance(separator, list):
        default = separator
        separator = ','

    if default is None:
        default = []

    if name not in os.environ:
        return default
    return os.environ[name].split(separator)


def _load_env_file():
    envfile = abs_path('.env')
    if os.path.isfile(envfile):
        with open(envfile, 'r', encoding='utf-8') as fp:
            for line in fp:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                k, v = line.split('=', 1)
                os.environ.setdefault(k, v)


_load_env_file()
