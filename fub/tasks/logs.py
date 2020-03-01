from fabric import task

from utils import check_for_stage


@task
@check_for_stage()
def passenger(c):
    """
    Show Passenger logs.
    """
    c.run(f'cat {c.code_path}/logs/passenger.log')
