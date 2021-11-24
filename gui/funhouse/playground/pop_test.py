# print('x')
# print('DDDDDD')

import sys
import importlib.abc
import importlib
import importlib.util
import os


mod_nam = os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../../owl/module_perspective_transform.py'))
mod_nam_2 = os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../../owl'))
# x = importlib.import_module('Module', sys.argv[1])
# print(mod_nam)
# w = importlib.import_module('Module', mod_nam)

# print(importlib.abc.Finder.find_module('Module', '../../owl/module_perspective_transform.py'))
# mpf = importlib.abc.MetaPathFinder()
# print(mpf.find_module(fullname='Module', path=mod_nam_2))

# w = importlib.import_module('Module', '../../owl/module_perspective_transform.py')
def my_import(name):
    print(name)
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

# x = w("./../../examples/perspective_transform/config.json")
# x.get_config()

if __name__ == '__main__':
    
    """
    sys.path.append(str(mod_nam_2))
    module = importlib.import_module('owl')
    class_ = getattr(module, 'Module')
    instance = class_()
    """
    
    sys.path.append(mod_nam_2)
    xd = 'module_perspective_transform'
    # from xd import Module
    # from module_perspective_transform import Module
    # w = importlib.import_module('Module', xd)
    w = importlib.util.find_spec('module_perspective_transform', mod_nam_2)
    print(w)
    module = importlib.util.module_from_spec(w)
    sys.modules['module_perspective_transform'] = module
    x = sys.modules['module_perspective_transform']()
    print(x.get_config())
    # w = importlib.import_module('Module', mod_nam)
    # x = Module()
    
    '''
    sys.path.append(str(mod_nam))
    from owl import Module
    # from sys.path[-1] import Module
    x = Module()
    y = x.get_config()
    '''
    # def import_file(full_name, path):
    #     """Import a python module from a path. 3.4+ only.

    #     Does not call sys.modules[full_name] = path
    #     """
    #     from importlib import util

    #     spec = util.spec_from_file_location(full_name, path)
    #     mod = util.module_from_spec(spec)

    #     spec.loader.exec_module(mod)
    #     return mod

    # import_file('Module', mod_nam)

    # import importlib.machinery
    # modulename = importlib.machinery.SourceFileLoader('Module',mod_nam).load_module()

    # print(sys.argv)
    # # w = my_import(mod_nam)
    # # print(len(sys.argv))

    # ldr = importlib.abc.Loader()
    # print(ldr.load_module('Module', __file__= mod_nam))
    
    """
    import importlib.util
    import sys

    # For illustrative purposes.

    file_path = mod_nam
    module_name = 'Module'

    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module_class = importlib.util.module_from_spec(spec)
    # sys.modules[module_name] = module
    mc2 = spec.loader.create_module(spec)
    spec.loader.exec_module(module_class)
    # module_class.get_config()
    pass
    module_class = None
    """
    '''
    Odpalanie modułu w ten sposób ma problemy z wczytaniem dodatkowych modułów lokalnych dla siebie(stream_video)
    ale takto działa, ale włąśnie nie do końca
    dopóki nie będzie do końca, 'multiprocessing' odpada
    '''

    # import importlib.util
    # import sys

    # def import_module(name, package=None):
    #     """An approximate implementation of import."""
    #     absolute_name = importlib.util.resolve_name(name, package)
    #     try:
    #         return sys.modules[absolute_name]
    #     except KeyError:
    #         pass

    #     path = None
    #     if '.' in absolute_name:
    #         parent_name, _, child_name = absolute_name.rpartition('.')
    #         parent_module = import_module(parent_name)
    #         path = parent_module.__spec__.submodule_search_locations
    #     for finder in sys.meta_path:
    #         spec = finder.find_spec(absolute_name, path)
    #         if spec is not None:
    #             break
    #     else:
    #         msg = f'No module named {absolute_name!r}'
    #         raise ModuleNotFoundError(msg, name=absolute_name)
    #     module = importlib.util.module_from_spec(spec)
    #     sys.modules[absolute_name] = module
    #     spec.loader.exec_module(module)
    #     if path is not None:
    #         setattr(parent_module, child_name, module)
    #     return module
    # import_module('Module')