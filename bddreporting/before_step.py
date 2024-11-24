import uuid
from .config import Config
def before_step(func):
    def wrapper(*args, **kwargs):
        context = args[0]
        context.current_step_id = uuid.uuid4()

        # Hook that runs before each step.   
        context.scenario.feature
        if Config.get("halt_execution_on_failure", False):
           assert not context.failed, f"An error was logged before step: {step.name}"

        result = func(*args, **kwargs)
        return result
    return wrapper
