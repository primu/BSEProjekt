import os
from conf import PROJECT_ROOT


def full_path_for(path):
    return os.path.join(PROJECT_ROOT, path)