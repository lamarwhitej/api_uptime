import argparse
import json
from multiprocessing import Pipe, Process
import sys
import uuid

import test
from test_variables import *


class ArgumentParser(argparse.ArgumentParser):
    def __init__(self):
        desc = "Tests the uptime for a given length of time against a list of services."
        usage_string = "api-uptime [-i/--server-id] [-s/--services] [-t/--time]"

        super (ArgumentParser, self).__init__(
            usage=usage_string, description=desc)

        self.add_argument(
            "-i", "--server-id", metavar="<server id>",
            required=False, default=None)

        self.add_argument(
            "-s", "--services", metavar="<comma-delimited services list>",
            required=False, default=None)

        self.add_argument(
            "-t", "--times", metavar="<amount of seconds to run>",
            required=False, default=60)


def entry_point():
    cl_args = ArgumentParser()
    cl_args = cl_args.parse_args()
    if cl_args <> None:
        services = cl_args.services.split(",") or services_list
    services = services_list
    services = [service.strip() for service in services]

    mad = test.ApiUptime(version, user, password, tenant, auth_url)

    pipes = []
    for s in services:
        p, c = Pipe()
        pipes.append(p)
        Process(target=mad.uptime, args=(c,s,cl_args.times,cl_args.server_id,)).start()

    try:
    	outputs = [pipe.recv() for pipe in pipes]
    except:
        pass

    try:
	final_output = {}
        [final_output.update(output) for output in outputs]
    except:
	pass
    
    print json.dumps(final_output)


if __name__ == "__main__":
    entry_point()
