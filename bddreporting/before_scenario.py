import os
from .config import Config
def before_scenario(func):
    def wrapper(*args, **kwargs):
        context = args[0]
        scenario = args[1]

        if Config.get("halt_execution_on_failure", False) and context.failed:
            context.scenario.skip("Skipping execution")

        result = func(*args, **kwargs)
        return result
    return wrapper
