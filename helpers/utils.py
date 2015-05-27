import importlib
import os

from conf import PROJECT_ROOT


def full_path_for(path):
    return os.path.join(PROJECT_ROOT, path)

def get_class(module,  class_name):
        module = importlib.import_module(module)
        cls = getattr(module, class_name)
        return cls
