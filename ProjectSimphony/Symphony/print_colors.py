def print_color(color_code, *args, **kwargs):
    print(color_code, end='')
    print(*args, **kwargs)

    NORMAL_COLOR_CODE = '\033[0m'
    print(NORMAL_COLOR_CODE, end='')


def print_red(*args, **kwargs):
    print_color('\033[91m', *args, **kwargs)


def print_green(*args, **kwargs):
    print_color('\033[92m', *args, **kwargs)
