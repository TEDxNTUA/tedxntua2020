from invoke import Collection

from . import apache, django, git, npm
from .deploy import deploy
from .stages import staging, production


namespace = Collection(
    apache,
    django,
    git,
    npm,
    staging,
    production,
    deploy,
)
