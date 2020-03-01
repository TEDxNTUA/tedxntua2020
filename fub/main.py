from fabric import (
    Config as FabConfig,
    Executor,
    __version__ as fabric,
)
from fabric.main import Fab
from invoke import Argument
from invoke.config import merge_dicts


OVERRIDDEN_ARGUMENTS = [
    'prompt-for-passphrase',
]


# invoke.Config subclass that uses fub/tasks as collection instead of fabfile
class FubConfig(FabConfig):
    @staticmethod
    def global_defaults():
        defaults = FabConfig.global_defaults()
        ours = {
            'tasks': {
                'search_root': 'fub',
                'collection_name': 'tasks',
            },
        }
        merge_dicts(defaults, ours)
        return defaults

class Fub(Fab):
    prefix = 'fub'

    def _get_filtered_args(self):
        filtered_args = [
            arg for arg in super().core_args()
            if arg.name not in OVERRIDDEN_ARGUMENTS
        ]
        return filtered_args

    def core_args(self):
        filtered_args = self._get_filtered_args()
        extra_args = [
            Argument(
                names=('prompt-for-passphrase',),
                kind=bool,
                default=True,
                help='Request an upfront SSH key passphrase prompt.',
            ),
        ]
        return filtered_args + extra_args

program = Fub(
    name='Fabric',
    version=fabric,
    executor_class=Executor,
    config_class=FubConfig,
)
