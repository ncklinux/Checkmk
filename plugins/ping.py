#!/bin/python3
print("<<<ping>>>")

try:
    import os
    import sys
    import subprocess
    import socket
    import psutil
except ImportError:
    import os
    import sys
    import subprocess
    import socket
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'psutil', '-q'], check=True)
    import psutil


class Ping:

    def ping(self):
        for ip in list(self.get_ip_addresses(socket.AF_INET)):
            if os.system("ping -4 -c 1 " + ip[1] + " > /dev/null 2>&1") == 0:
                print(ip[1], '= up!')
            else:
                print(ip[1], '= down!')
        for ip in list(self.get_ip_addresses(socket.AF_INET6)):
            if os.system("ping -6 -c 1 " + ip[1] + " > /dev/null 2>&1") == 0:
                print(ip[1], '= up!')
            else:
                print(ip[1], '= down!')

    # noinspection PyMethodMayBeStatic
    def get_ip_addresses(self, family):
        for interface, snics in psutil.net_if_addrs().items():
            for snic in snics:
                if snic.family == family:
                    yield interface, snic.address


test = Ping()
test.ping()
