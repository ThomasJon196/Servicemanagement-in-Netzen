import socket
from colorhash import ColorHash

file_path = './resources/count.txt'

def render_miniwhoami():
    counter = get_counter()
    hostname = socket.gethostname()

    html_body = f"""
    <div style="background-color:{get_hex_color(hostname)}">
        <p>Hostname: {hostname}</p>
        <p>IPv4-add: {get_ip4()}</p>
        <p>IPv6-add: {get_ip6()}</p>
        <p>Access count: {counter}</p>
    </div>
    """
    return html_body

def get_counter():
    try:
        with open(file_path, 'r') as file:
            count = file.readline()
            count = int(count) + 1
        with open(file_path, 'w') as file:
            file.write(str(count))
    except FileNotFoundError:
        print('count.txt file not found. Creating new one.')
        count = 1
        with open(file_path, 'w') as file:
            file.write('1')

    return count

def get_hex_color(obj):
    c = ColorHash(obj)
    return c.hex

def get_ip4():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def get_ip6():

   try:
        sv6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        sv6.connect(("2620:119:35::35", 80))
        ip = sv6.getsockname()[0]
   except:
        ip = '::1'

   return ip 
