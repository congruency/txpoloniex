def format_function(name):
    name = name.replace('return', '', 1)
    name = name[0].lower() + name[1:]
    return name
