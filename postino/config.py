import codecs
import json

from .error import PostinoConfigError


def load(filename):
    try:
        with codecs.open(filename, encoding='utf-8') as f:
            return json.loads(f.read())
    except ValueError as e:
        raise PostinoConfigError('Config malformed: ' + str(e))
    except OSError as e:
        raise PostinoConfigError('Error loading config: ' + str(e))
