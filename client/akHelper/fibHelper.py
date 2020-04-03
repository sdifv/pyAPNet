def ip2decimalism(ip):
    dec_value = 0
    v_list = ip.split('.')
    v_list.reverse()
    t = 1
    for v in v_list:
        dec_value += int(v) * t
        t = t * (2 ** 8)
    return str(dec_value)


def decimalism2ip(dec_value):
    dec_value = int(dec_value)
    ip = ''
    t = 2 ** 8
    for _ in range(4):
        v = dec_value % t
        ip = '.' + str(v) + ip
        dec_value = dec_value // t
    ip = ip[1:]
    return ip


def format_fib_entry(action, line, node):
    line = line.strip()
    elements = line.strip().split()
    prefix = elements[0].split('/')
    ip = ip2decimalism(prefix[0])
    length = prefix[1]
    new_line = "{} {} {} {} {} {} {}\n".format(action, "fwd", node, ip, length, elements[1], length)
    return new_line
