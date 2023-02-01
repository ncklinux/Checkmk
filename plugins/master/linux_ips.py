#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
from .agent_based_api.v1 import *
import os


def discover_linux_ips(section):
    yield Service()

def ping_linux_ips(section):
    for ip in section:
        if os.system("ping -4 -c 1 " + ip + " > /dev/null 2>&1") == 0:
            yield Result(state=State.OK, summary="IP up!")
        else:
            yield Result(state=State.CRIT, summary="IP down!")


register.check_plugin(
    name = "linux_ips",
    service_name = "IPs",
    discovery_function = discover_linux_ips,
    check_function = ping_linux_ips,
)
