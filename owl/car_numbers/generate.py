import os
import json
import functools

from .calculate import calc_digit


def list_substitution_fixes(number: str, substitutions_map):
    '''
    Generator listujący możliwe podmiany znaku spełniajace sume kontrolną
    Zwraca krotkę (numer, prawdopodobieństwo)

    '''
    if len(number) != 12:
        raise Exception("Number should have 12 digits")

    for i in range(12):
        new_number = number[:i] + str(calc_digit(number, i)) + number[i + 1:]
        yield new_number, substitutions_map[number[i]][new_number[i]]


def list_insertion_fixes(number: str, insertions_map):
    '''
    Generator listujący możliwe podmiany znaku spełniajace sume kontrolną
    Zwraca krotkę (numer, prawdopodobieństwo)
    Bazuje na prawdopodobieństwie zamiany jedenj cyfry w dwie

    '''    
    if len(number) != 13:
        raise Exception("Number should have 13 digits")

    for i in range(10):
        reduced_number =  number[:i] + "_" + number[i+2:]
        new_number = number[:i] + str(calc_digit(reduced_number, i)) + number[i+2:]
        yield new_number, insertions_map[number[i:i+2]][new_number[i]]


def list_deletion_fixes(number: str, deletions_map):
    '''
    Generator listujący możliwe podmiany znaku spełniajace sume kontrolną
    Zwraca krotkę (numer, prawdopodobieństwo)
    Bazuje na prawdopodobieństiwe zamiany cyfry w literę i zmiany dwóch cyfr w jedną

    '''    
    if len(number) != 11:
        raise Exception("Number should have 11 digits")

    ext_number = ' '+number+' '
    for i in range(12):
        extended_number =  number[:i] + "_" + number[i:]
        new_number = number[:i] + str(calc_digit(extended_number, i)) + number[i:]
        yield new_number, deletions_map[ext_number[i]][ext_number[i+1]][new_number[i]]



if __name__ == "__main__":
    path = os.path.dirname(__file__)

    with open(os.path.join(path, "substitutions_map.json")) as f:
        substitutions_map = json.load(f)
    for number in list_substitution_fixes("215138460294", substitutions_map):
        print(number)
    for number in list_substitution_fixes("215238460294", substitutions_map):
        print(number)

    with open(os.path.join(path, "insertions_map.json")) as f:
        insertions_map = json.load(f)    
    for number in list_insertion_fixes("1234567890123", insertions_map):
        print(number)        

    with open(os.path.join(path, "deletions_map.json")) as f:
        deletions_map = json.load(f)    
    for number in list_deletion_fixes("12345678901", deletions_map):
        print(number)                