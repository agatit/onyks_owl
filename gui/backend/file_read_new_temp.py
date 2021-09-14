import os
import json
import glob


DEFAULT_PATH_PROJECTS = os.path.join(os.path.abspath(os.path.dirname(__file__)),"../../examples")
DEFAULT_PATH_MODULES = os.path.join(os.path.abspath(os.path.dirname(__file__)),"../../owl")

EMPTY_CONFIG = {
    'modules': {},
    'pipeline': {}
}
ERROR_RETVAL = {
    'message': 'OOpsie, Something went wrong :('
} # TODO nieno, więcej tych retval'ów żeby było wiadomo co gdzie dokładnie...
# TODO w jednym z configów jest "comment". Może to też uwzględnić...
class Files():
    def __init__(self, projects_path = DEFAULT_PATH_PROJECTS, modules_path = DEFAULT_PATH_MODULES):
        self.projects_dir = projects_path
        self.modules_dir = modules_path
    
    ### DEFINICJE ###
    def get_modules(self):
        modules = os.listdir(path = self.modules_dir)
        mod = list(filter(lambda k: '.py' in k, modules))       # pliki z '.py'
        mod2 = list(filter(lambda k: '__init__' not in k, mod)) # pliki bez __init__
        mod3 = [x.replace('.py', '') for x in mod2]
        return mod3
    def get_module_data(self, module_id):
        # module.py -> get_config()
            # czy coś takiego...
        pass
    
    ### ZARZĄDZANIE PROJEKTAMI ###
    def get_projects(self):
        projects = os.listdir(path = self.projects_dir)
        # return json.dumps(projects, ensure_ascii=False)
        return projects
    def create_project(self, name):
        try:
            os.mkdir(os.path.join(DEFAULT_PATH_PROJECTS, name)) 
            # TODO Jeżeli folder istnieje
                # jeżeli w folderze jest 'config.json'
                    # wywal błąd, że już taki moduł istnieje
                # else
                    # stwórz config
                    # return 0
            with open(os.path.join(DEFAULT_PATH_PROJECTS, name, 'config.json'), 'w') as file:
                json.dump(EMPTY_CONFIG,file, ensure_ascii=False, indent=4) # TODO 'skipkeys'?
            return 'coś' # TODO returny
        except:
            return ERROR_RETVAL

    def get_project_conf(self, project_id):
        try:
            with open(os.path.join(self.projects_dir, project_id, 'config.json')) as file:
                config = json.load(file)
            return config
        except:
            return ERROR_RETVAL
    def set_project_conf(self, project_id, data):
        try:
            with open(os.path.join(self.projects_dir, project_id, 'config.json'), 'w') as file:
                json.dump(data,file, ensure_ascii=False, indent=4) # TODO 'skipkeys'? 
            return 'coś'    # TODO returny
        except:
            return ERROR_RETVAL
    ### EDYCJA TORU PRZETWARZANIA ###
    def get_project_modules(self, project_id):
        try:
            config = self.get_project_conf(project_id)
            modules = list(config['modules'].keys())
            return modules
        except:
            return ERROR_RETVAL
    def add_project_module(self, project_id, module_name):
        modules = self.get_modules()
        if module_name in modules:
            config = self.get_project_conf(project_id)
            config['modules'][module_name] = self.get_module_data(module_name)
            return 'coś'
        else:
            return ERROR_RETVAL
    def get_project_module_data(self, project_id, module_id):
        config = self.get_project_conf(project_id)
        if config['modules'][module_id]:
            module = config['modules'][module_id]
            return module
        else:
            return ERROR_RETVAL
    def delete_project_module(self, project_id, module_id):
        config = self.get_project_conf(project_id)
        if config['modules'][module_id]:
            del config['modules'][module_id]
            return self.set_project_conf(project_id, config)
        else:
            return ERROR_RETVAL
    def get_module_params(self, project_id, module_id):
        config = self.get_project_conf(project_id)
        if config['modules'][module_id]['params']:
            params = config['modules'][module_id]['params']
            return params
        else:
            return ERROR_RETVAL
        ''')YM projekcie, w TYM module, jest TAKI parametr
        jeżeli nie ma...
        co jeżeli nie ma? będzie NULL czy glizda?
        glizda całkiem
        także try catchy więcej...
        a teraz lece jakieś configi poprzerabiać na nową modłę
        albo nie, to potem
        logi?
        # TODO jak pójdzie całkiem nowa implementacja 'config.json' to pewnie trzeba będzie popoprawiać rzeczu tu i tam...
        '''
        
    def get_module_parameter(self, project_id, module_id, parameter):
        config = self.get_project_conf(project_id)
        param = config['modules'][module_id]['params'][parameter]
        return param
    def set_module_parameter(self, project_id, module_id, parameter, value):
        config = self.get_project_conf(project_id)
        config['modules'][module_id]['params'][parameter] = value
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
    # print(x.get_project_conf('perspective_transform'))
    print(x.get_modules())
    # print(x.get_project_modules('perspective_transform'))
    # print(x.delete_project_module('perspective_transform','module_sink_file'))
    # print(x.get_project_modules('perspective_transform'))
    # print(x.get_module_data('perspective_transform', 'module_source_cv'))
    # print(x.get_module_params('perspective_transform', 'module_source_cv'))
    
    # print(x.create_project('xddd'))
    # print(x.get_projects())
    # print(x.get_module_params('perspective_transform', 'module_sink_file'))