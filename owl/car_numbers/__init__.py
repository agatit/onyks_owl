import functools

from .generate import *
from .calculate import *


def fix(number: str):
    path = os.path.dirname(__file__)

    if len(number) == 12:
        with open(os.path.join(path, "substitutions_map.json")) as f:
            substitutions_map = json.load(f)  
        iter = list_substitution_fixes(number, substitutions_map)
        max = functools.reduce(lambda a, b: a if a[1] > b[1] else b, iter)        
        return max[0]
    elif len(number) == 11:
        with open(os.path.join(path, "deletions_map.json")) as f:
            deletions_map = json.load(f)  
        iter = list_deletion_fixes(number, deletions_map)
        max = functools.reduce(lambda a, b: a if a[1] > b[1] else b, iter)        
        return max[0]
    elif len(number) == 13:
        with open(os.path.join(path, "insertions_map.json")) as f:
            insertions_map = json.load(f)
        iter = list_insertion_fixes(number, insertions_map)
        max = functools.reduce(lambda a, b: a if a[1] > b[1] else b, iter)        
        return max[0] 
    else:
        raise Exception("This method can only fix strings that are 11, 12 or 13 characters long")
