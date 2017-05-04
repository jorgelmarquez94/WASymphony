from collections import namedtuple
from copy import deepcopy
from functools import partial
from Symphony.lexer import Types, DUPLICATED_OPERATORS
from math import sqrt, log, floor, ceil
from random import random
from operator import (add, sub, mul, truediv, mod, eq, gt, lt, ge, le, and_,
                      or_, pos, neg, not_)


# Local memory sector declaration
MEMORY_SECTORS = (
    ('global_', 10_000),
    ('temporal', 130_000),
    ('constant', 200_000),
    ('local', 250_000),
    ('end', 350_000),
)

# Actual runtime memory. It has a type dictionary for each sector
memory = {sector[0]: {type_ : {} for type_ in Types}
          for sector in MEMORY_SECTORS[:-1]}

# Activation records used to initialize a function's context
activation_records = []
# List for keeping track of where to return after a function
stored_program_counters = []

# Function parameters (special and user-defined)
parameters = []
# List of print calls and musical notes
output = ([], [])

class UninitializedError(Exception):
    """ Raised when a variable address has no value in memory """


class ArityError(Exception):
    """ Raise when some structure is repeated an invalid number of times """


class ChangeContext(Exception):
    """ Indicate a content change to trigger a storage of context """
    def __init__(self, goto_line):
        self.goto_line = goto_line


def generate_memory_addresses(end_addresses=False):
    """Generate a tuple of memory addresses

    This function is used by the VM and the parser. It returns the starting and
    ending address of every sector and type to allow a fast lookup of what the
    type of an address is and to count how many variables of the same type have
    been assigned per sector
    """
    ADDRESS_TUPLE = namedtuple('ADDRESSES', [address[0] for address
                                             in MEMORY_SECTORS[:-1]])

    # Begin with the global starting address
    current_address = MEMORY_SECTORS[0][1]
    addresses = []
    for sector in MEMORY_SECTORS[1:]:
        # Get the address of the next sector to calculate sector sizes
        next_address = sector[1]
        sector_size = next_address - current_address

        # Determine where the address of each type in the sector starts
        type_start_addresses = [starting_address for starting_address in
                                range(current_address, next_address,
                                      int(sector_size / len(Types)))]

        # Generate an additional field indicating the end of each type
        # address if requested by the caller
        if end_addresses:
            type_end_addresses = type_start_addresses[1:] + [next_address]

            type_addresses = dict(zip(Types, zip(type_start_addresses,
                                                 type_end_addresses)))
        else:
            type_addresses = dict(zip(Types, type_start_addresses))

        addresses.append(type_addresses)
        current_address = next_address

    return ADDRESS_TUPLE._make(addresses)


addresses = generate_memory_addresses(end_addresses=True)


def value(address):
    """ Return the memory's value associated with an address """
    try:
        address = int(address)
    except ValueError:
        # Array pointer was found, so remove '&' at the beginning
        address = value(address[1:])

    try:
        return get_address_container(address)[address]
    except KeyError as e:
        raise UninitializedError(f'Sorry, but you tried to use a variable '
                                 f'before assignment. Please check your program')


def store(value_to_store, address):
    """ Store a value inside a memory address """
    try:
        address = int(address)
    except ValueError:
        # Array pointer was found, so remove '&' at the beginning
        address = value(address[1:])

    get_address_container(address)[address] = value_to_store


def get_address_container(address):
    """ Get the internal list containing an address. Used by value and store """
    for i, sector in enumerate(MEMORY_SECTORS[-2::-1], start=1):
        sector_name, sector_address = sector
        # If the address is bigger than this sector, it is contained here
        if address >= sector_address:
            for type_address in addresses[-i].items():
                type_, (start_address, end_address) = type_address
                # If an address is between the start and end, it belongs here
                if start_address <= address < end_address:
                    return memory[sector_name][type_]


def store_param(address):
    parameters.append(address)


def print_(end='\n'):
    """ Add a print call to the output """
    parameter = value(parameters.pop())

    if isinstance(parameter, bool):
        parameter = str(parameter).lower()
    else:
        parameter = str(parameter)

    output[0].append(parameter + end)
    # print(printed_value, end=end)


def get(return_address):
    """ Special function to get the nth character of a string """
    index = value(parameters.pop())
    string = value(parameters.pop())
    char = string[index]
    store(char, return_address)


def copy():
    """ Special function to copy a string into another """
    destination_address = parameters.pop()
    source_value = value(parameters.pop())
    store(source_value, destination_address)


def length(return_address):
    """ Special function to calculate the length """
    store(len(value(parameters.pop())), return_address)


def sqrt_(return_address):
    """ Special function to get the square root """
    store(sqrt(value(parameters.pop())), return_address)


def goto(jump):
    return int(jump)


def gotof(address, jump):
    if not value(address):
        return goto(jump)


def verify_limits(offset_address, min_, array_size):
    """ Check if an array access is off limits """
    offset = value(offset_address)
    array_size = int(array_size)
    min_ = int(min_)

    if not min_ <= offset < array_size:
        raise IndexError(f"Index out of bounds: {offset}. This one should be "
                         f"greater than or equal to {min_} and smaller than "
                         f"{array_size}")

def array_access(base_dir, offset_address, address_pointer):
    """ Access a validated offset """
    offset = value(offset_address)
    base_dir = int(base_dir)
    store(base_dir + offset, address_pointer)


def end_proc(function_name):
    """ Finish a function definition, Restoring a previous activation record """
    return_address = directory.functions[function_name].return_address
    if return_address != None:
        return_type = directory.functions[function_name].return_type
        try:
            # Copy the return value of a context into the previous one
            return_value = memory['local'][return_type][return_address]
            activation_records[-1][return_type][return_address] = return_value
        except KeyError:
            pass

    # Restore the previous context
    memory['local'] = activation_records.pop()
    return stored_program_counters.pop() + 1


def gosub(function_name):
    """ Save the current activation record and trigger a context change """
    activation_records.append(deepcopy(memory['local']))

    global directory
    function = directory.functions[function_name]
    # Load each argument into the function's new context
    for type_, address, argument in zip(function.parameter_types,
                                        function.parameter_addresses,
                                        parameters):
        memory['local'][type_][address] = value(argument)

    parameters.clear()
    raise ChangeContext(function.starting_quad)


def log_(return_address):
    """ Special function to get the natural logarithm """
    store(log(value(parameters.pop())), return_address)


def random_(return_address):
    """ Special function to get a random seed """
    store(random(), return_address)


def little_star():
    """ Sample song """
    C()
    C()
    G()
    G()
    A()
    A()
    G()

    F()
    F()
    E()
    E()
    D()
    D()
    C()


def A():
    output[1].append("A")


def B():
    output[1].append("B")


def C():
    output[1].append("C")


def D():
    output[1].append("D")


def E():
    output[1].append("E")


def F():
    output[1].append("F")


def G():
    output[1].append("G")


def to_str(return_address):
    """ Special function to convert to string """
    store(str(value(parameters.pop())), return_address)


def floor_(return_address):
    """ Special function for the floor operation """
    store(floor(value(parameters.pop())), return_address)


def ceil_(return_address):
    """ Special function for the ceil operation """
    store(ceil(value(parameters.pop())), return_address)


def input_(return_address):
    """ Special function to read from a user """
    global input_counter
    store(inputs[input_counter], return_address)
    input_counter += 1


# Arithmetic operations
OPERATIONS = {
    '+' : add,
    '-' : sub,
    '*' : mul,
    '/' : truediv,
    '**' : pow,
    'mod' : mod,
    'equals' : eq,
    '>' : gt,
    '<' : lt,
    '>=' : ge,
    '<=' : le,
    'and' : and_,
    'or' : or_,
    '++' : partial(add, 1),
    '--' : lambda value: sub(value, 1),
    DUPLICATED_OPERATORS['+'] : pos,
    DUPLICATED_OPERATORS['-'] : neg,
    'not' : not_,
    '=' : lambda value: value,
}

# VM functions, which operate mainly through addressess, not values
VM_FUNCTIONS = {
    'PARAM' : store_param,
    'print' : partial(print_, end=''),
    'println' : print_,
    'sqrt' : sqrt_,
    'log' : log_,
    'get' : get,
    'little_star' : little_star,
    'A' : A,
    'B' : B,
    'C' : C,
    'D' : D,
    'E' : E,
    'F' : F,
    'G' : G,
    'length' : length,
    'copy' : copy,
    'random' : random_,
    'to_str' : to_str,
    'input' : input_,
    'floor' : floor_,
    'ceil' : ceil_,
    'GOTO' : goto,
    'GOTOF': gotof,
    'ACCESS' : array_access,
    'VER' : verify_limits,
    'GOSUB' : gosub,
    'ENDPROC' : end_proc,
}

# Signature of special functions
SPECIAL_SIGNATURES = {
    'print' : (None, [{type_ for type_ in Types}]),
    'println' : (None, [{type_ for type_ in Types}]),
    'to_str' : (Types.STR, [{type_ for type_ in Types}]),
    'get' : (Types.CHAR, [{Types.STR}, {Types.INT}]),
    'sqrt' : (Types.DEC, [{Types.INT, Types.DEC}]),
    'log' : (Types.DEC, [{Types.INT, Types.DEC}]),
    'random' : (Types.DEC, []),
    'little_star' : (None, []),
    'A' : (None, []),
    'B' : (None, []),
    'C' : (None, []),
    'D' : (None, []),
    'E' : (None, []),
    'F' : (None, []),
    'G' : (None, []),
    'length' : (Types.INT, [{Types.STR}]),
    'copy' : (None, [{Types.STR}, {Types.STR}]),
    'to_str' : (Types.STR, [{type_ for type_ in Types}]),
    'input' : (Types.STR, []),
    'floor' : (Types.INT, [{Types.DEC}]),
    'ceil' : (Types.INT, [{Types.DEC}]),
}


def handle_vm_function(quad, current_quad_idx):
    """ Manage a vm function """
    try:
        operation = VM_FUNCTIONS[quad[0]]
        address1 = quad[1]
        return operation(address1)
    except TypeError:
        # Thrown if function needs two parameters
        address2 = quad[2]

        try:
            return operation(address1, address2)
        except TypeError:
            address3 = quad[3]
            return operation(address1, address2, address3)
    except IndexError:
        # No quad 0: parameterless
        try:
            return operation()
        except TypeError:
            # Only input would raise such an exception here
            raise ArityError(f"The wrong amount of input lines was submitted")
    except ChangeContext as e:
        stored_program_counters.append(current_quad_idx)

        return e.goto_line
    except KeyError:
        raise NotImplementedError(f"This operation isn't supported yet "
                                  f"({quad[0]})")


def handle_operation(operation, quad):
    """ Handle an arithmetical operation """
    address1 = quad[1]
    address2 = quad[2]

    try:
        address3 = quad[3]
    except IndexError:
        # Only 1 operand and 1 address to store the result
        result = operation(value(address1))
        store(result, address2)
    else:
        try:
            # 2 operands and 1 address to store the result
            value1 = value(address1)
            value2 = value(address2)
            result = operation(value1, value2)
            store(result, address3)
        except ZeroDivisionError as e:
            raise ZeroDivisionError(f'Oops! You tried to divide {value1} by 0. '
                                    f'Please correct your program') from e


def output_after_cleanup():
    global inputs
    global input_counter

    if input_counter != len(inputs):
        raise ArityError(f"The wrong amount of input lines was submitted")

    return output


def play_note(lines, constants, directory_, inputs_):
    """ Entry point for orchestra """
    global directory
    directory = directory_
    global inputs
    inputs = inputs_
    global input_counter
    input_counter = 0

    memory['constant'] = constants

    # Clean the output
    for list_ in output:
        list_.clear()

    line_list = [line.split() for line in lines.split('\n')]

    current_quad_idx = 0
    while current_quad_idx < len(line_list):
        try:
            quad = line_list[current_quad_idx]
        except IndexError:
            # Finish when accessing non-existent quadruple (naive GOTO did it)
            return output_after_cleanup()

        try:
            operation = OPERATIONS[quad[0]]
        except KeyError:
            vm_result = handle_vm_function(quad, current_quad_idx)

            if vm_result is not None:
                current_quad_idx = vm_result
            else:
                current_quad_idx += 1
        except IndexError:
            # Empty operation (empty line) might only be found at the end
            return output_after_cleanup()
        else:
            handle_operation(operation, quad)
            current_quad_idx += 1

    return output_after_cleanup()
