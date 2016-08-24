from novaclient import client
from time import sleep
from multiprocessing import Pipe, Process

import datetime

class ApiUptime():
    def __init__(self, version, username, password, tenant, auth_url):
        self.nova = client.Client(version, username, password, tenant, auth_url)

    def _proc_helper(self, function, conn, additional_args=None):
        try:
            if additional_args is not None:
                function(additional_args)
            else:
                function()
            conn.send(True)
            conn.close()
        except:
            conn.send(False)
            conn.close()

    def _uptime(self, conn, service, times, function, additional_args=None):
        start_time = datetime.datetime.now()
	end_time = start_time + datetime.timedelta(0,float(times))
        pipes = []
        while end_time > datetime.datetime.now():
            p, c = Pipe()
            pipes.append(p)
            Process(target=self._proc_helper, args=(function, c, additional_args)).start()
	    sleep(1)
        try:
            output = [pipe.recv() for pipe in pipes]
	except:
	    pass
        self.report(conn, service, sum(output), len(output), str(start_time), str(datetime.datetime.now()))

    def uptime(self, conn, service, times, server_id=None):
        if service == "neutron":
            self._uptime(conn, "neutron", times, self.nova.networks.list)
        elif service == "glance":
            self._uptime(conn, "glance", times, self.nova.images.list)
        elif service == "nova":
            self._uptime(conn, "nova", times, self.nova.servers.list)
        elif service == "cinder":
            self._uptime(conn, "cinder", times, self.nova.volumes.get_server_volumes, server_id)

    def report(self, conn, service, success, total, start_time, end_time):
        uptime_pct = 100 * (success/total)
        conn.send({
            service: {
                "uptime_pct": uptime_pct,
                "total_requests": total,
                "successful_requests": success,
                "failed_requests": total - success,
                "start_time": start_time,
                "end_time": end_time}})
        conn.close()
