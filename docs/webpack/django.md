# Webpack: Django integration

[django-webpack-loader](https://github.com/owais/django-webpack-loader) is used to support referencing Webpack bundles in Django's templates.

## Data flow

1. A Django template uses `django-webpack-loader`'s directives to reference a Webpack bundle.
1. `django-webpack-loader` looks at the Django settings to get `BUNDLE_DIR_NAME` and `STATS_FILE`.
1. It then creates URLs that map to Webpack's bundles and substitutes the template directives with these URLs by render time.

## Configuration

### Default configuration

Taken from [the official repo](https://github.com/owais/django-webpack-loader/blob/master/webpack_loader/config.py):

```python
DEFAULT_CONFIG = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'webpack_bundles/',
        'STATS_FILE': 'webpack-stats.json',
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': [r'.+\.hot-update.js', r'.+\.map']
    }
}
```

If your configuration does not contain one of the above keys, then the default value will be used.

### Base

```python
# project/settings/base.py

INSTALLED_APPS = [
    ...,
    'webpack_loader',
    ...
]
```

### Dev

```python
# project/settings/dev.py

# django-webpack-loader will use this as a base directory for the `BUNDLE_DIR_NAME` configuration.
STATICFILES_DIRS = (
    abs_path('bundles/build-dev'),
)

WEBPACK_LOADER = {
    'DEFAULT': {
        # Webpack outputs bundles in bundles/build-dev/ when in development mode.
        'BUNDLE_DIR_NAME': '/',
        'STATS_FILE': abs_path('bundles', 'webpack-stats.dev.json'),
    }
}
```

### Production

```python
# project/settings/prod.py

STATICFILES_DIRS = (
    abs_path('bundles/dist'),
)

WEBPACK_LOADER = {
    'DEFAULT': {
        # Webpack outputs bundles in bundles/dist/ when in production mode.
        'BUNDLE_DIR_NAME': '/',
        'STATS_FILE': abs_path('bundles', 'webpack-stats.prod.json')
    }
}
```

## Useful links

* [Examples from the repository](https://github.com/owais/django-webpack-loader/tree/master/examples)