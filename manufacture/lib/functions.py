

def clear_console():
    import platform
    import os

    if (platform.system() == "Windows"):
        os.system("cls")
    if (platform.system() == "Linux"):
        os.system("clear")


def input_int():
    try:
        user_input = int(input())
    except ValueError:
        return
    return user_input


def display_time(seconds, granularity=2):
    result = []

    intervals = (
        ('weeks', 604800),  # 60 * 60 * 24 * 7
        ('days', 86400),    # 60 * 60 * 24
        ('hours', 3600),    # 60 * 60
        ('minutes', 60),
        ('seconds', 1),
        )

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])
