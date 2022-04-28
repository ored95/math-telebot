import json

def load_config(configFileName="config.json"):
    with open(configFileName) as fs:
        return json.load(fs)
    return None

def load_token(cfg):
    return open(cfg['token_file']).read()

def load_author(cfg):
    return cfg['author']