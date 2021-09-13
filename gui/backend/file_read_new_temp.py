import os
import json
import glob


DEFAULT_PATH_PROJECTS = os.path.join(os.path.abspath(os.path.dirname(__file__)),"../../examples")
DEFAULT_PATH_MODULES = os.path.join(os.path.abspath(os.path.dirname(__file__)),"../../owl")

# TODO podorabiać NULL'e, wychwytywanie kretyńskich błędów...

EMPTY_CONFIG = {
    'modules': {},
    'pipeline': {}
}
class Files():
    def __init__(self, projects_path = DEFAULT_PATH_PROJECTS, modules_path = DEFAULT_PATH_MODULES):
        self.projects_dir = projects_path
        self.modules_dir = modules_path
    
    ### DEFINICJE ###
    def get_modules(self):
        modules = os.listdir(path = self.modules_dir)
        mod = list(filter(lambda k: '.py' in k, modules))       # pliki z '.py'
        mod2 = list(filter(lambda k: '__init__' not in k, mod)) # pliki bez __init__
        return mod2
    def get_module_data(self, module_id):
        # module.py -> get_config()
            # czy coś takiego...
        pass
    
    ### ZARZĄDZANIE PROJEKTAMI ###
    def get_projects(self):
        projects = os.listdir(path = self.projects_dir)
        return json.dumps(projects)
    def create_project(self, name):
        os.mkdir(os.path.join(DEFAULT_PATH_PROJECTS, name))
        config = os.open(os.path.join(DEFAULT_PATH_PROJECTS, name, 'config.json'), os.O_CREAT)
        # TODO czy ta linijka wyżej jest na pewno gites
        # TODO jeszcze wrzucić jakiś wstępny config
        # Może wykorzystać "with"?
        config.close()
    def get_project_conf(self, project_id):
        file = open(self.projects_dir + '/' + project_id + '/' + 'config.json')
        config = json.load(file)
        file.close()
        return config
    def set_project_conf(self, project_id, data):
        with open(self.projects_dir + '/' + project_id + '/' + 'config.json') as file:
            json.dump(data,file) 
        return 'coś'    # TODO returny
                        # TODO ej, bo ogólnie to ja tu chcę 'set' a nie 'append' jbc...
    ### EDYCJA TORU PRZETWARZANIA ###
    def get_project_modules(self, project_id):
        config = self.get_project_conf(project_id)
        modules = list(config.keys())
        return json.dumps(modules)
    def get_project_module_data(self, project_id, module_id):
        config = self.get_project_conf(project_id)
        module = config[module_id]
        return module
    def delete_module(self, project_id, module_id):
        config = self.get_project_conf(project_id)
        # TODO Wypierdol ten moduł ze słownika
        return self.set_project_conf(config)

    def get_module_params(self, project_id, module_id):
        config = self.get_project_conf(project_id)
        params = config[module_id]['params']
        return params
    def get_module_parameter(self, project_id, module_id, parameter):
        config = self.get_project_conf(project_id)
        param = config[module_id]['params'][parameter]
        return param
    def set_module_parameter(self, project_id, module_id, parameter, value):
        config = self.get_project_conf(project_id)
        config[module_id]['params'][parameter] = value
        return self.set_project_conf(project_id,config)

    ### URUCHOMIENIE/DEBUG ###
    def get_module_state(self, project_id, module_id):
        config = self.get_project_conf(project_id)
        return config['modules'][module_id]['settings']['status']
    def set_module_state(self, project_id, module_id, value):
        config = self.get_project_conf(project_id)
        config['modules'][module_id]['settings']['status'] = value
        return self.set_project_conf(project_id,config)
    def module_start(self, project_id, module_id):
        config = self.get_project_conf(project_id)
        config['modules'][module_id]['settings']['status'] = True
        return self.set_project_conf(project_id,config)
        # TODO jakoś to jednak trzeba wystartować, a nie że ja tylko se zmiennom w pliku zmjenjam...
        # TODO walidacja, nie wystartuję już wystartowanego modułu
        # TODO jak ogarnę powyższe, to dopiero te pod spodem ogarnąć
    def module_stop(self, project_id, module_id):
        pass
    def module_restart(self, project_id, module_id):
        pass
    def get_module_log(self, project_id, module_id):
        pass


if __name__ == '__main__':
    x = Files()
    # print(List.get_names())
    # print(x.get_projects())
    # print(x.get_project_conf('slicer'))
    print(x.get_modules())
    # print(x.get_module_data('slicer', 'module_source_cv'))
    # print(x.get_module_params('slicer', 'module_source_cv'))