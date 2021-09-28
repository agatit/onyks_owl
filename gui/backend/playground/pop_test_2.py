import importlib.util
import sys
import os

mod_nam = os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../../owl/module_perspective_transform.py'))
mod_nam_2 = os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../../owl'))
mod_nam_3 = '.home.hubert.Documents.GitHub.onyks_owl.owl.module_perspective_transform'

def import_module(name, package=None):
    """An approximate implementation of import."""
    absolute_name = importlib.util.resolve_name(name, package)
    try:
        return sys.modules[absolute_name]
    except KeyError:
        pass

    path = None
    if '.' in absolute_name:
        parent_name, _, child_name = absolute_name.rpartition('.')
        parent_module = import_module(parent_name)
        path = parent_module.__spec__.submodule_search_locations
    for finder in sys.meta_path:
        spec = finder.find_spec(absolute_name, path)
        if spec is not None:
            break
    else:
        msg = f'No module named {absolute_name!r}'
        raise ModuleNotFoundError(msg, name=absolute_name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[absolute_name] = module
    spec.loader.exec_module(module)
    if path is not None:
        setattr(parent_module, child_name, module)
    return module

if __name__ == '__main__':
    sys.path.append(mod_nam_2)
    w = importlib.util.find_spec('module_perspective_transform', mod_nam)
    itertools = importlib.import_module('module_perspective_transform')
    # print(w)
    js = "./examples/perspective_transform/config.json"

    x = itertools.Module(['module_perspective_transform',js])
    # x = itertools.Module('module_perspective_transform','./../../examples/perspective_transform/config.json')
    # x = itertools.Module('xd')
    print(x.get_config())
    module = importlib.util.module_from_spec(w)
    sys.modules['module_perspective_transform'] = module
    print(x)
    # itertools = importlib.import_module('time')
    # print(itertools)
    # itertools.sleep(5)