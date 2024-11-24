import uuid
from .config import Config
def after_step(func):
    def wrapper(*args, **kwargs):
        context = args[0]
        step = args[1] 
        result = func(*args, **kwargs)
        return result
    return wrapper
