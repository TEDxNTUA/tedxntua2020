'''
Setup script

Usage: pip install .

For development purposes, run: pip install -e .[dev]
'''
from setuptools import setup, find_packages
from _version import __version__

setup(
    name='tedxntua<VAR:YEAR>',
    version=__version__,
    packages=find_packages(),
    scripts=['manage.py'],
    url='<VAR:REPO_URL>',
    author='TEDxNTUA IT Team <VAR:YEAR>',
    author_email='webmaster@tedxntua.com',
    install_requires=[
        'dj-database-url',
        'Django',
        'mysqlclient',
        'django-versatileimagefield',
        'django-webpack-loader',
        'django-parler',
    ],
    extras_require={
        'dev': [
            'django-extensions',
        ],
    },
)
