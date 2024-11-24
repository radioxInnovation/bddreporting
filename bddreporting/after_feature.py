from .utils import write_text

def after_feature(func):
    def wrapper(*args, **kwargs):
        feature = args[1]
        if hasattr(feature, "log") and len( feature.log ) > 0:
            write_text( feature.log, feature.filename, feature.name, "_unknown_", feature.tags )
        result = func(*args, **kwargs)
        return result
    return wrapper
