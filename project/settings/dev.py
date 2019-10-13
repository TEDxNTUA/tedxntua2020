'''Configuration for development mode'''
from .base import * # pylint: disable=wildcard-import
from .env import abs_path


STATICFILES_DIRS += (
    abs_path('bundles/build-dev'),
)

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': '/',
        'STATS_FILE': abs_path('bundles', 'webpack-stats.dev.json'),
    }
}
