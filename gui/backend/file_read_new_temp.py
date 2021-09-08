import os
import json

DEFAULT_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),"../../examples")

class Files():
    def __init__(self, default_path = DEFAULT_PATH):
        self.dir = default_path
    def get_projects(self):
        projects = os.listdir(path = self.dir)
        return projects
    def get_project_conf(self, p_name):
        file = open(self.dir + '/' + p_name + '/' + 'config.json')
        config = json.load(file)
        file.close()
        return config

if __name__ == '__main__':
    x = Files()
    # print(List.get_names())
    print(x.get_projects())
    print(x.get_project_conf('slicer'))