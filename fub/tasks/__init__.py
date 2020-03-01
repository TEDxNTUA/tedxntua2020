from invoke import Collection

from . import django, git, npm
from .apache import set_private, set_public, restart_django
from .deploy import deploy
from .stages import staging, production


namespace = Collection(
    django,
    git,
    npm,
    set_private,
    set_public,
    restart_django,
    staging,
    production,
    deploy,
)
