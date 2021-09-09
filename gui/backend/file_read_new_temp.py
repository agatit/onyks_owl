import os
import json

DEFAULT_PATH_PROJECTS = os.path.join(os.path.abspath(os.path.dirname(__file__)),"../../examples")
DEFAULT_PATH_MODULES = os.path.join(os.path.abspath(os.path.dirname(__file__)),"../../owl")

# TODO podorabiać NULL'e
class Files():
    def __init__(self, projects_path = DEFAULT_PATH_PROJECTS, modules_path = DEFAULT_PATH_MODULES):
        self.projects_dir = projects_path
        self.modules_dir = modules_path
    def get_projects(self):
        projects = os.listdir(path = self.projects_dir)
        return json.dumps(projects)
 
    def create_project(self, name):
        pass
    def get_project_conf(self, project_id):
        file = open(self.projects_dir + '/' + project_id + '/' + 'config.json')
        config = json.load(file)
        file.close()
        return config

    def get_modules(self, project_id):
        config = self.get_project_conf(project_id)
        modules = list(config.keys())
        return json.dumps(modules)
    def get_module_data(self, project_id, module_id):
        config = self.get_project_conf(project_id)
        module = config[module_id]
        return module
    def delete_module(self, project_id, module_id):
        pass

    def get_module_params(self, project_id, module_id):
        config = self.get_project_conf(project_id)
        params = config[module_id]['params']
        return params
    def get_module_parameter(self, project_id, module_id, parameter):
        pass
    def set_module_parameter(self, project_id, module_id, parameter, value):
        pass
    def get_module_state(self, project_id, module_id):
        pass
    def set_module_state(self, project_id, module_id, value):
        pass
    def module_start(self, project_id, module_id):
        pass
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
    # print(x.get_modules('slicer'))
    # print(x.get_module_data('slicer', 'module_source_cv'))
    print(x.get_module_params('slicer', 'module_source_cv'))