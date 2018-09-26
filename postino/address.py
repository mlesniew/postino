import email.utils


def parse_address(addr):
    if isinstance(addr, tuple):
        if len(addr) != 2:
            raise ValueError('Address tuple should have exactly two elements')
        addr_tuple = tuple(addr)
    elif isinstance(addr, str):
        addr_tuple = email.utils.parseaddr(addr)
    else:
        raise ValueError('Email address should be a string or a tuple')
    if not addr_tuple[1]:
        raise ValueError('Invalid email address')
    return email.utils.formataddr(addr_tuple)


def parse_addresses(addr):
    if not addr:
        return []
    elif isinstance(addr, tuple):
        return [parse_address(addr)]
    elif isinstance(addr, str):
        # the provided parameter is a string
        address_tuples = email.utils.getaddresses([addr])
        return [email.utils.formataddr(at) for at in address_tuples]
    elif isinstance(addr, (list, set)):
        return [parse_address(a) for a in addr]
    else:
        raise ValueError('addr should be a str, tuple, list or set')
