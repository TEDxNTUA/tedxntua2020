from functools import wraps, update_wrapper

from fabric import task

from . import stages


def source_profile(c):
    return c.prefix('. ~/.bash_profile')

def task_factory(factory, *args, **kwargs):
    def wrapper(func):
        # Create task_func
        task_func = factory(*args, **kwargs)
        # Make task_func look like func (copy name etc)
        task_func = update_wrapper(task_func, func)
        # Return task
        return task(task_func)
    return wrapper

def check_for_stage(_func=None, *, which=True, use_default=None):
    """
    Check if task function runs in the context of an allowed stage.

    Parameters
    ----------
    which : bool or list of str (default True)
        If True, any stage is allowed. If it's a list, the stage must be in it.
        If False, the check is skipped.
    use_default : str or None (default None)
        If not None and no stage is active, it activates the stage with the
        given name before running the task.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(c, *args, **kwargs):
            try:
                if which is True: # If True, check for any stage.
                    c._stage
                elif which:
                    # If False, skip check. Otherwise, use as whitelist.
                    if c._stage not in which:
                        raise RuntimeError(
                            f'This command requires one of the following '
                            f'stages to be active: {which}'
                        )
                return func(c, *args, **kwargs)
            except AttributeError:
                if use_default is None:
                    print('This command requires a stage to be active')
                # If use_default is set, activate the respective stage
                stage_task = getattr(stages, use_default)
                stage_task(c)
                return func(c, *args, **kwargs)
            except RuntimeError as e:
                print(e)
        return wrapper

    if _func is None:
        return decorator
    return decorator(_func)
