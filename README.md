A python script that pings an OpenStack environment in-parallel using NovaClient.

To get started:

1. Install novaclient within your environment
 - apt-get install python-novaclient #this is for ubuntu
2. Pull the repository
3. Setup os.cnf file

Setup Config
=============
To set up the config the required parameters are below:

  * version=2.1
  * user=
  * password=
  * tenant=
  * auth_url=http://XX.XX.XXX.XXX:5000/v2.0

__Note:__ If you are pinging Cinder for volumes you must have a server ID specified.

Running the script
=================

This script will parse the following arguments from the command-line and pulls additional data from os.cnf

[-c/--container-name] [-s/--services] [-t/--time]

--container-name will overwrite the value in os.cnf and is required to test swift uptime.

--services is a comma-delimited list of services, defaults to the value in os.cnf

--time is the total amount of time in seconds that the script will check the api's of the given services. Defaults to 60.

To test against glance & nova:

    python call_test.py -s glance, nova

Pinging Swift (Object Storage)
=============================

If you are going to be pinging Swift you need to add a container name.

You can do this by adding it to the os_cnf file or by adding it directly in the command line.

    python call_test.py -s swift -c name-of-container


To find out more about novaclient Python API read here http://docs.openstack.org/developer/python-novaclient/api.html#module-novaclient
