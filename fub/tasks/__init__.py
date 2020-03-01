from invoke import Collection

from . import apache, django, git, npm, logs
from .deploy import deploy
from .stages import staging, production


namespace = Collection(
    apache,
    django,
    git,
    npm,
    logs,
    staging,
    production,
    deploy,
)
