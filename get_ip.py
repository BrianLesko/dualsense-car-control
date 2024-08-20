import netifaces as ni

def get_ip_address(interface_name):
    try:
        ip_address = ni.ifaddresses(interface_name)[ni.AF_INET][0]['addr']
        return ip_address
    except KeyError:
        return None


