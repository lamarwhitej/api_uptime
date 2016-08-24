import argparse
from ConfigParser import SafeConfigParser
import json
from multiprocessing import Pipe, Process

import test


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
            required=False, default=60, type=int)


def entry_point():
    cl_args = ArgumentParser().parse_args()

    # Initialize Config Variables
    config = SafeConfigParser()
    config.read("os.cnf")
    version = config.get("openstack", "version")
    user = config.get("openstack", "user")
    password = config.get("openstack", "password")
    tenant = config.get("openstack", "tenant")
    auth_url = config.get("openstack", "auth_url")
    services_list = config.get("openstack", "version")
    server_id = cl_args.server_id or config.get("openstack", "server_id")

    services = [service.strip() for service in (cl_args.services or services_list).split(",")]

    mad = test.ApiUptime(version, user, password, tenant, auth_url)

    pipes = []
    for s in services:
        p, c = Pipe()
        pipes.append(p)
        Process(target=mad.uptime, args=(c,s,cl_args.times,server_id,)).start()
        c.close()

	outputs = [pipe.recv() for pipe in pipes]
    final_output = {k: v for d in outputs for k, v in d.items()}

    print json.dumps(final_output)


if __name__ == "__main__":
    entry_point()
