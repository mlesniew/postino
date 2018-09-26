import argparse

from . import PostinoError
from . import address
from . import postino
from . import reload_config


def get_parser():
    parser = argparse.ArgumentParser(
            prog='postino',
            description='Easy email sending from the command line.')

    parser.add_argument(
            '--content',
            type=argparse.FileType('r'),
            default='-',
            help='file with email contents (defaults to stdin)')

    parser.add_argument(
            '--text',
            action='store_const',
            dest='style',
            const='text',
            help='send text email (this is the default)')

    parser.add_argument(
            '--html',
            action='store_const',
            dest='style',
            const='html',
            help='send html email')

    parser.add_argument(
            '--subject', '-s',
            help='set email subject (if not specified, subject is the first line of contents)')

    parser.add_argument(
            '--cc',
            default=[],
            action='append',
            type=address.parse_address,
            help='add CC recipients')

    parser.add_argument(
            '--bcc',
            default=[],
            action='append',
            type=address.parse_address,
            help='add BCC recipients')

    parser.add_argument(
            'recipient',
            action='append',
            type=address.parse_address,
            help='recipients')

    return parser


def main():
    try:
        parser = get_parser()
        args = parser.parse_args()

        reload_config()

        content = args.content.read().splitlines()

        if args.subject is None:
            # subject is in first line
            subject = content[0]
            del content[0]
        else:
            # subject provided on command line
            subject = args.subject

        if args.style == 'html':
            text = None
            html = '\n'.join(content)
        else:
            text = '\n'.join(content)
            html = None

        postino(text=text,
                html=html,
                subject=subject,
                to=args.recipient,
                cc=args.cc,
                bcc=args.bcc)
    except PostinoError as e:
        raise SystemExit(str(e))
    except KeyboardInterrupt:
        raise SystemExit('Abort.')


if __name__ == '__main__':
    main()
