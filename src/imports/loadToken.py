import os

def load(filename):
    token_name = {}
    token_literal = {}
    code = 1

    token_path = os.path.join(os.path.dirname(__file__), '..', filename)

    with open(token_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            parts = line.split(None, 1)
            if len(parts) != 2:
                continue

            name, literal = parts
            token_name[name] = code
            token_literal[literal] = code
            code += 1

    return token_name, token_literal
