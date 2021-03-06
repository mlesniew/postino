import email.charset
import email.header
import email.mime.multipart
import email.mime.text
import email.utils

from .address import parse_addresses


# Email using utf-7 should use Quoted Printables for non-ascii chars.  This
# way the message will be at least partially human-readable
email.charset.add_charset('utf-7', email.charset.QP, email.charset.QP)


def encode_header(value, encoding='utf7'):
    value = str(value)
    try:
        return email.header.Header(value.encode('ascii'))
    except UnicodeError:
        return email.header.Header(value.encode(encoding), encoding)


def encode_address_header(addresses):
    ret = email.header.Header()

    for idx, address in enumerate(addresses):
        if idx != 0:
            ret.append(', ')
        try:
            ret.append(address.encode('ascii'))
        except UnicodeError:
            # non-ascii?
            name, address = email.utils.parseaddr(address)
            ret.append(name.encode('utf-7'), 'utf-7')
            ret.append(' <%s>' % address)

    return ret


def construct_body(text, html):

    def text_part(content, subtype):
        MT = email.mime.text.MIMEText
        try:
            return MT(content.encode('ascii'), subtype, 'ascii')
        except UnicodeError:
            return MT(content.encode('utf-7'), subtype, 'utf-7')

    tp = text_part(text, 'plain') if text else None
    hp = text_part(html, 'html') if html else None

    if tp and hp:
        # both parts are non-empty
        message = email.mime.multipart.MIMEMultipart('alternative', None, [tp, hp])
    else:
        # at most one part is non-empty
        message = tp or hp or text_part('', 'plain')

    return message


def set_headers(
        msg,
        subject,
        to=[],
        cc=[],
        bcc=[],
        fromaddr=[]):

    if subject:
        msg['Subject'] = encode_header(subject)

    msg['Date'] = encode_header(email.utils.formatdate(None, True, True))

    if to:
        msg['To'] = encode_address_header(to)
    if cc:
        msg['CC'] = encode_address_header(cc)
    if bcc:
        msg['BCC'] = encode_address_header(bcc)
    if fromaddr:
        msg['From'] = encode_address_header(fromaddr)


def construct(
        subject='',
        text='',
        html='',
        to=[],
        cc=[],
        bcc=[],
        fromaddr=[]):

    # prepare body
    msg = construct_body(text, html)

    # parse parameters
    to = parse_addresses(to)
    cc = parse_addresses(cc)
    bcc = parse_addresses(bcc)
    fromaddr = parse_addresses(fromaddr)

    # set headers
    set_headers(
        msg,
        subject=subject.replace('\n', ' ').replace('\r', ' '),
        to=to,
        cc=cc,
        bcc=bcc,
        fromaddr=fromaddr)

    recipients = [email.utils.parseaddr(addr)[1] for addr in to + cc + bcc]
    fromline = ', '.join(email.utils.parseaddr(addr)[1] for addr in fromaddr)

    return msg, fromline, recipients
