from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import json
import os

# TODO inna klasa na zczytywanie plików
# TODO zrobienie requesta pod te pliki
    # hmmm, czy danie dodatkowej klasy nie opóźni wysyłki?
    # samo otwieranie pliku wteiwewte może być nudne
    # chuj, najwyżej pod optymalizację na deser
    # ...
    # i logi pewnie w plaintext'cie
# TODO wchodzenie do folderu 'examples' i zczytywanie:
    # folderów
    # plików "config"
    # plików "supervisord"
    # plików logów - folder 'tmp' 

# TODO front - mądre czytanie plików/konkatenacja danych

app = Flask(__name__)
api = Api(app)

filename = os.path.join(os.path.abspath(os.path.dirname(__file__)),'./config_default.json')
MODULES = []
CONFIG_DEFAULT = {} # TODO doprowadzić do używalności "config_default.json"
SETTINGS = {}

# TODO czytanie plików log'ów
def data_init(filename):
    ###  CONFIG_DEFAULT  ###
    f = open(filename, )
    CONFIG_DEFAULT.update(json.load(f))
    f.close()
    ###      MODULES     ###
    for key in CONFIG_DEFAULT:
        MODULES.append(key)
    ###     SETTINGS     ###
    settings_temp = {
        "modules": MODULES,
        "refresh_rate": 1000,
        "start": False
    }
    SETTINGS.update(settings_temp)

 
# onyx.com/restapp/module_x/params
# onyx.com/restapp/settings

class RestApp(Resource):
    def get(self):
        return CONFIG_DEFAULT
    def put(self):
        CONFIG_DEFAULT = request.form['data']
        return CONFIG_DEFAULT

class Module_x(Resource):
    def get(self, module_id):
        return {module_id:CONFIG_DEFAULT[module_id]}
    def put(self, module_id):
        print(type(request.form))
        print(request)
        # data = request.form.to_dict(flat=False)
        data = request.form.copy().to_dict()
        print(data)
        '''
        parser = reqparse.RequestParser()
        for x in CONFIG_DEFAULT[module_id].keys():
            print(x)
            parser.add_argument(x)
        args = parser.parse_args()
        print('Oto GET data - ', end='')
        print(args)
        CONFIG_DEFAULT[module_id] = args
        '''
        return CONFIG_DEFAULT[module_id]

class Parameter(Resource):
    def get(self, module_id, parameter):
        return CONFIG_DEFAULT[module_id][parameter]
    def put(self, module_id, parameter):
        parser = reqparse.RequestParser()
        parser.add_argument('data')
        # TODO  - stworzyć 'default_config'
        #       - zacząć na jego podstawie robić walidację, żeby mi user nie wstawiał idiotyzmów, np 'hwdp' do Int'a
        #       - znaczy 'default_config' jakby okej, ale czy walidacja u mnie czy na froncie...
        # print(request)
        args = parser.parse_args()
        print('Oto GET data - ', end='')
        print(args)
        # TODO nno działać toto działa, ale no... Czy to ma sens? Czy uwzględniłem wszystkie przypadki?
        try:
            put_in = int(args['data'])
        except:
            put_in = args['data']
        CONFIG_DEFAULT[module_id][parameter] = put_in
        return CONFIG_DEFAULT[module_id][parameter]

class Settings(Resource): # TODO kaman, od chłopa będę pobierał listę modułów? Co ten gówniak niby wie?!?!?
    def get(self):
        return SETTINGS
    def put(self):
        CONFIG_DEFAULT = request.form['data'] # TODO tu się pewnie rypnie
        return CONFIG_DEFAULT
# TODO na deser pododawać 201, 204, etc.

# class Todo(Resource):
#     def get(self, todo_id):
#         abort_if_todo_doesnt_exist(todo_id)
#         return TODOS[todo_id]

#     def delete(self, todo_id):
#         abort_if_todo_doesnt_exist(todo_id)
#         del TODOS[todo_id]
#         return '', 204

#     def put(self, todo_id):
#         args = parser.parse_args()
#         task = {'task': args['task']}
#         TODOS[todo_id] = task
#         return task, 201


# # TodoList
# # shows a list of all todos, and lets you POST to add new tasks
# class TodoList(Resource):
#     def get(self):
#         return TODOS

#     def post(self):
#         args = parser.parse_args()
#         todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
#         todo_id = 'todo%i' % todo_id
#         # TODOS[todo_id] = {'task': args['task']}
#         TODOS[todo_id] = request.form['data']
#         return TODOS[todo_id], 201


# onyx.com/restapp/module_x/params
api.add_resource(RestApp,   '/restapp')
api.add_resource(Module_x,  '/restapp/<string:module_id>')
api.add_resource(Parameter, '/restapp/<string:module_id>/<string:parameter>')
api.add_resource(Settings,  '/restapp/settings')

if __name__ == '__main__':
    data_init(filename)
    app.run(debug=True)