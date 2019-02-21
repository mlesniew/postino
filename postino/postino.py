# coding: utf-8
import functools
import os

try:
    import markdown as markdown_module
    GOT_MARKDOWN = True
except ImportError:
    GOT_MARKDOWN = False

from .config import load
from .construct import construct
from .send import send_message


CONFIG_PATH = os.path.expanduser(os.environ.get('POSTINO_CONFIG', '~/.postino'))


def postino_raw(
        text='',
        html='',
        markdown='',
        subject='',
        to=[],
        cc=[],
        bcc=[],
        fromaddr=[],
        host='localhost',
        port=25,
        mode=None,
        login=None,
        password=None):

    if markdown:
        text = markdown
        if GOT_MARKDOWN:
            html = markdown_module.markdown(markdown)
        else:
            html = ''

    message, fromline, recipients = construct(
        text=text,
        html=html,
        subject=subject,
        to=to,
        cc=cc,
        bcc=bcc,
        fromaddr=fromaddr)

    send_message(
        message,
        recipients,
        fromline,
        host=host,
        port=port,
        mode=mode,
        login=login,
        password=password)


def Sender(**kwargs):
    return functools.partial(postino_raw, **kwargs)


default_sender = None


def reload_config(path=CONFIG_PATH):
    global default_sender
    default_sender = Sender(**load(path))


def postino(*args, **kwargs):
    if default_sender is None:
        reload_config()
    default_sender(*args, **kwargs)
