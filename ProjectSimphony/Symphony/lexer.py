from enum import IntEnum
from Symphony.ply.lex import lex


class Types(IntEnum):
    INT = 0
    CHAR = 1
    STR = 2
    BOOL = 3
    DEC = 4


class NonUserTypes(IntEnum):
    ARRAY = 5


tokens = (
    'VOID', 'INT_VAL', 'DEC_VAL', 'CHAR_VAL', 'STR_VAL', 'BOOL_VAL', 'RETURN',
    'EXPONENTIATION', 'INCREMENT', 'DECREMENT', 'EQUALS', 'GREATER_EQUAL_THAN',
    'LESS_EQUAL_THAN', 'AND', 'OR', 'NOT', 'FUN', 'WHILE', 'IF', 'ELSE',
    'ELSEIF', 'ID', 'SPECIAL_ID', 'MOD', 'PROGRAM', 'BREAK'
) + tuple(datatype.name for datatype in Types)


literals = [',', ';', '(', ')', '{', '}', '[', ']', '=', '+', '-', '*', '/', '>', '<', ]
t_GREATER_EQUAL_THAN = r'>='
t_LESS_EQUAL_THAN = r'<='
t_EXPONENTIATION = r'\*\*'
t_INCREMENT = r'\+\+'
t_DECREMENT = r'--'


OPERATOR_LIST = ['+', '-', '*', '/', '**', 'mod', 'equals', '>', '<', '>=',
                 '<=', 'and', 'or',]
OPERATORS = dict(zip(OPERATOR_LIST, [counter for counter in
                                     range(len(OPERATOR_LIST))]))

UNARY_OPERATOR_LIST = ['++', '--', '+', '-', 'not']
UNARY_OPERATORS = dict(zip(UNARY_OPERATOR_LIST, [counter for counter in
                                     range(len(UNARY_OPERATOR_LIST))]))
SELF_UPDATE_OPERATORS = ['++', '--']
DUPLICATED_OPERATORS = {'+' : 'PLUS', '-' : 'MIN'}
CONSTANT_VALS = {'true' : True, 'false' : False}


keywords_named_as_types = ['void', 'equals', 'and', 'or', 'not', 'fun', 'while',
                           'if', 'else', 'elseif', 'program', 'mod', 'int',
                           'dec', 'char', 'str', 'bool', 'return', 'break']
keywords_to_types = {keyword: keyword.upper()
                     for keyword in keywords_named_as_types}
keywords_to_types.update({keyword: 'BOOL_VAL' for keyword in CONSTANT_VALS})


special_ids = {'print', 'println', 'read', 'sqrt', 'log', 'random',
               'little_star', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'concat',
               'length', 'copy', 'get', 'to_str', 'input', 'floor', 'ceil'}


def t__MULTI_LINE_COMMENT(t):
    r'/\*(.|\n)*?\*/'
    t.lineno += t.value.count('\n')


def t_IDS_AND_KEYWORDS(t):
    r'[a-zA-Z_][0-9a-zA-Z_]*'
    if t.value in special_ids:
        t.type = 'SPECIAL_ID'
    else:
        t.type = keywords_to_types.get(t.value, 'ID')
    return t


def t_DEC_VAL(t):
    r'[+-]?[0-9]*\.[0-9]+'
    t.value = float(t.value)
    return t


def t_INT_VAL(t):
    r'[-+]?[0-9]+'
    t.value = int(t.value)
    return t


def t_CHAR_VAL(t):
    r"\'[^']\'"
    t.value = t.value[1]
    return t


def t_STR_VAL(t):
    r'\"[^"]*\"'
    t.value = t.value[1:-1]
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_eof(t):
    return None


def t_error(t):
    print("The system found a problem with how you wrote your program, so "
          + "please find the character sequence '" + t.value[0] + "' on line "
          + str(t.lexer.lineno) + " and correct it.")

"""
def t_SINGLE_LINE_COMMENT(t):

def t_MULTI_LINE_COMMENT(t):
"""

t_ignore_SINGLE_LINE_COMMENT = r'//.*'
t_ignore = " \t"


lexer = lex()
