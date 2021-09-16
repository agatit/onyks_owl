import os
import json
import glob
import shutil
import subprocess

from logs_test import Project#, Module


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
class Files():  # To to byłaby klasa główna, jej podklasą 'Project', a 'Project'a podklasą 'Module'
                # TODO zmienić nazwę tej klasy żeby lepiej się kwalifilowała w koncepcję
                # TODO może niektóre operacje plikowe zwalić na 'Project'
    def __init__(self, projects_path = DEFAULT_PATH_PROJECTS, modules_path = DEFAULT_PATH_MODULES):
        self.projects_dir = projects_path
        self.modules_dir = modules_path
        # TODO czasem 'dir', czasem 'path', nieno, ujednolicić to!
        self.projects = {}
        # for project in os.listdir(path = self.projects_dir): # TODO winksza walidacja, sprawdzić też config.json. Oddzielna funkcja
        #     self.add_project(project)

    
    ### DEFINICJE ###
    def get_modules(self):
        modules = os.listdir(path = self.modules_dir)
        mod = list(filter(lambda k: '.py' in k, modules))       # pliki z '.py'
        mod2 = list(filter(lambda k: '__init__' not in k, mod)) # pliki bez __init__
        mod3 = [x.replace('.py', '') for x in mod2]
        return mod3
    def get_module_data(self, module_id):
        # proc = subprocess.Popen(['python3', os.path.join(self.modules_dir, module_id + '.py'), os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../examples/perspective_transform/config.json')], stdin=subprocess.PIPE ,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc = subprocess.Popen(['python3'], stdin=subprocess.PIPE ,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print (proc.communicate(b'import os\nos.getcwd()', timeout=15))
        # print (proc.communicate(b'os.getcwd()'))
        print (proc.communicate(b'from module_perspective_transform import Module'))
        print (proc.communicate('x = Module("./../examples/perspective_transform/config.json")'))
        print (proc.communicate('x.get_config()'))
        proc.kill()
        # module.py -> get_config()
            # czy coś takiego...
        pass
    
    ### ZARZĄDZANIE PROJEKTAMI ###
    '''
    Walidacja projektu:
    - Jeżeli nie istnieje plik 'project/config.json', to znaczy że projektu nie ma
        - Więc jeżeli istnieje folder 'project', to można go wywalić, cnie? # TODO
    - Jeżeli plik 'project/config.json' istnieje, to mamy projekt!
        - sprawdzać układ pliku 'config.json'? # TODO
    '''
    def get_projects(self):
        return self.projects.keys()
        # TODO zaczynam się bardziej opierać na danych w pamięci. Nie wiem jak będzie wyglądało zarządzanie później, ale pewnie wskazane byłoby uwzględnienie jakiegoś refresh'a
    def add_project(self, name):
        if not os.path.isfile(os.path.join(self.projects_dir, name, 'config.json')):
            print(f'Project {name} nonexistent')
            if os.path.exists(os.path.join(self.projects_dir, name)):
                shutil.rmtree(os.path.join(self.projects_dir, name))
                print('Invalid directory removed')
        else:
            print(f'Project {name} found!')
            if name == 'perspective_transform':
                self.projects[name] = Project(os.path.join(self.projects_dir, name), self.modules_dir)
                print(f'Project {name} added!') # TODO if self.projects[name] is not None ?
    '''
    Chwila, mam add_project() do dodawania już istniejących projektów
    i create_project() do dodawania nowiutkich projektów
    ...
    na pewno powinienem stworzyć metodę validate_project() strikte pod walidację
    i może wyjebać add_project() po tym...
    
    Zaraz chwila! Po zrobieniu add_project() w __init__ mam posprzątane, create_project może na lajcie tworzyć bez walidowania
    '''

    def create_project(self, name):
        try:
            os.mkdir(os.path.join(self.projects_dir, name))
            with open(os.path.join(self.projects_dir, name, 'config.json'), 'w') as file:
                json.dump(EMPTY_CONFIG,file, ensure_ascii=False, indent=4)
            self.add_project(name)
            return 'coś' # TODO returny
        except:
            return ERROR_RETVAL

    def get_project_conf(self, project_id):
        return self.projects[project_id].get_config()
    def set_project_conf(self, project_id, data):
        return self.projects[project_id].set_config(data)
        
    ### EDYCJA TORU PRZETWARZANIA ###
    def get_project_modules(self, project_id):
        return self.projects[project_id].get_modules()
        
    def add_project_module(self, project_id, module_name):
        return self.projects[project_id].add_module(module_name)
        
        modules = self.get_modules()
        if module_name in modules:
            config = self.get_project_conf(project_id)
            config['modules'][module_name] = self.get_module_data(module_name)
            return 'coś'
        else:
            return ERROR_RETVAL
    def get_project_module_data(self, project_id, module_id):
        # return self.projects[project_id].get_module_data(module_id)
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
    # print(x.get_modules())
    # print(x.get_project_modules('perspective_transform'))
    # print(x.delete_project_module('perspective_transform','module_sink_file'))
    # print(x.get_project_modules('perspective_transform'))
    # print(x.get_project_module_data('perspective_transform', 'module_source_cv'))
    # print(x.get_module_params('perspective_transform', 'module_source_cv'))
    
    # print(x.create_project('xddd'))
    # print(x.get_projects())
    # print(x.get_module_params('perspective_transform', 'module_sink_file'))
    print(x.get_module_data('module_source_cv'))