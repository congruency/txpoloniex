import json
from twisted.web.client import readBody

def to_json(func):
    def read_and_decode(*args, **kwargs):
        d = func(*args, **kwargs)

        d.addCallback(readBody)

        def decode(body):
            body = body.decode('utf-8')
            return json.loads(body)

        d.addCallback(decode)

        return d

    return read_and_decode

def format_function(name):
    name = name.replace('return', '', 1)
    name = name[0].lower() + name[1:]
    return name


