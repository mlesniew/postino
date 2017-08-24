import codecs
import json
import os

from . import Sender


CONFIG_PATH = os.path.expanduser(os.environ.get('POSTINO_CONFIG', '~/.postino'))

sender = None


def reload():
    global sender
    with codecs.open(CONFIG_PATH, encoding='utf-8') as f:
        settings = json.loads(f.read())
    sender = Sender(**settings)


def send(*args, **kwargs):
    if sender is None:
        reload()
    sender(*args, **kwargs)
