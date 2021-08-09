import os
import configparser

MY_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),"../../examples")

# for root, dirs, files in os.walk(".", topdown=False):
# #    for name in files:
# #       print(os.path.join(root, name))
# #    for name in dirs:
# #       print(os.path.join(root, name))
#     print(root)
#     print(dirs)
#     print(files)
#     print("___________________________________________")

# print(os.listdir(path='./examples'))

path = os.path.join(MY_PATH, 'multiple_sources')
file = os.path.join(path, 'supervisord.conf')
logs_path = os.path.join(path, 'tmp')
cp = configparser.ConfigParser()
# print(file)
# x = open(file)
# print(x.read())
config = cp.read(file)
# print(config)
# print(type(cp))
# print(type(config))
# print(cp.sections())
sec_list = []
for item in cp.sections():
    print(item)
    # if item.startswith("program:"):
        # modules.append(item.removeprefix('program:'))
        # print(item.removeprefix('program:'))
        # print(item[8:])
        # sec_list.append(item[8:])

# log_file_list = os.listdir(path=logs_path)
# ez = open(logs_path + '/' + log_file_list[1])
# print(ez.read())
# matching = [s for s in log_file_list if "" in s]
# for mod in sec_list:
#     if any(mod + '-stderr' in s for s in log_file_list):
#         # print('xd')
#         # print(log_file_list)
#         print(mod + '-stderr')
#     if any(mod + '-stdout' in s for s in log_file_list):
#         print('dx')
#         # print(x)

# xd = []
# for mod in sec_list:
#     matching = [s for s in log_file_list if mod + '-stdout' in s]
#     # print(matching)
#     # print(len(matching))
#     if matching:
#         xd.append(matching[0])

# print(xd)

# print(cp['program:sink']['numprocs'])