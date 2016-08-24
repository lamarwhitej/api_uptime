A python script that pings an OpenStack environment in-parallel using NovaClient.

To get started:

1. Install novaclient within your environment
 - apt-get install python-novaclient #this is for ubuntu
2. Pull the repository
3. Setup test_variables config file

Setup Config
=============
To set up the config the required parameters are below:

  * version = '2.1'
  * user = ''
  * password = ''
  * tenant = ''
  * auth_url = 'http://XX.XX.XXX.XXX:5000/v2.0'

__Note:__ If you are pinging Cinder for volumes you must have a server ID specified.

Running the script
=================

The script is made to read sys args from the command line or read from the test_variables config file if you do not specify in the command line.

To run a ping on glance for example:

    python call_test.py images servers

If you do not specify a specific project it will ping all projects available (glance, nova, cinder, neutron).

Pinging Cinder (volumes)
===============

If you are going to be pinging Cinder you need to add a server id.

You can do this by adding it to the test_variables file or by adding it directly in the command line.

    python call_test.py images the-server-id

Specifying Run Time
===================

When running the script you can add a number to the command line and the script will run for X amount of time (seconds, minutes, hours).

 By default the script is set to a time interval of minutes.

    #will run the test for 60 minutes
    python call_test.py images 60
    
  * To change the time interval edit line 21 of __test.py__:
      - vi test.py
        - self.run_time = (start_time + timedelta (__minutes__=time)).strftime("%Y-%m-%dT%H:%M:%S%z")
        - self.run_time = (start_time + timedelta (__seconds__=time)).strftime("%Y-%m-%dT%H:%M:%S%z")
   



To find out more about novaclient Python API read here http://docs.openstack.org/developer/python-novaclient/api.html#module-novaclient

