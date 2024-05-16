Step 4: pyATS Shell Useful Libraries
####################################

**Value Proposition:** Streamline your network automation workflows with pyATS libraries like Dq, designed to simplify data querying and manipulation. 
The Dq library empowers you to efficiently extract and analyze device data using intuitive Python syntax, saving you time and effort. 
With Dq, you can leverage advanced querying capabilities to access specific information from complex data structures with ease, enabling you to focus on developing sophisticated automation solutions. 
Maximize your productivity and leverage the power of pyATS libraries to enhance your network automation expertise.

To use the **Dq** library, you need to follow the steps below:

#. Enter the following command to run the pyATS shell command from the Bash shell and specify the YAML testbed file as the parameter. This shell is where you can run the Python code.

    .. tip:: 
        
        The interactive shell might take some time to load (approximately 20 seconds)

    .. code-block:: bash

        pyats shell --testbed-file pyats_testbed.yaml

#. Create variables (Python objects) to call devices easily (csr - 'csr1000v-1' device).

    .. code-block:: python

        csr = testbed.devices["csr1000v-1"]

#. Connect and collect the output from the CSR device.

    .. code-block:: python

        csr.connect()
        csr_output = csr.parse('show ip route')

#. Explore csr_output by typing ``csr_output`` and try to find the routes for **OSPF**.

    .. code-block:: python

        {'vrf': {'default': {'address_family': {'ipv4': {'routes': {'10.0.0.4/30': {'route': '10.0.0.4/30',
        'active': True,
        'metric': 41,
        'route_preference': 110,
        'source_protocol_codes': 'O',
        'source_protocol': 'ospf',
        'next_hop': {'next_hop_list': {1: {'index': 1,
            'next_hop': '10.0.0.18',
            'updated': '18:21:31',
            'outgoing_interface': 'GigabitEthernet3'},
            2: {'index': 2,
            'next_hop': '10.0.0.14',
            'updated': '18:21:31',
            'outgoing_interface': 'GigabitEthernet2'}}}},
        '10.0.0.8/30': {'route': '10.0.0.8/30',
        'active': True,
        'metric': 51,
        'route_preference': 110,
        'source_protocol_codes': 'O',
        'source_protocol': 'ospf',
        'next_hop': {'next_hop_list': {1: {'index': 1,
            'next_hop': '10.0.0.18',
            'updated': '18:21:26',
            'outgoing_interface': 'GigabitEthernet3'},
            2: {'index': 2,
            'next_hop': '10.0.0.14',
            'updated': '18:21:26',
            'outgoing_interface': 'GigabitEthernet2'}}}},
        '10.0.0.12/30': {'route': '10.0.0.12/30',
        'active': True,
        'source_protocol_codes': 'C',
        'source_protocol': 'connected',
        'next_hop': {'outgoing_interface': {'GigabitEthernet2': {'outgoing_interface': 'GigabitEthernet2'}}}},
        '10.0.0.13/32': {'route': '10.0.0.13/32',
        'active': True,
        'source_protocol_codes': 'L',
        'source_protocol': 'local',
        'next_hop': {'outgoing_interface': {'GigabitEthernet2': {'outgoing_interface': 'GigabitEthernet2'}}}},
        '10.0.0.16/30': {'route': '10.0.0.16/30',
        'active': True,
        'source_protocol_codes': 'C',
        'source_protocol': 'connected',
        'next_hop': {'outgoing_interface': {'GigabitEthernet3': {'outgoing_interface': 'GigabitEthernet3'}}}},
        '10.0.0.17/32': {'route': '10.0.0.17/32',
        'active': True,
        'source_protocol_codes': 'L',
        'source_protocol': 'local',
        'next_hop': {'outgoing_interface': {'GigabitEthernet3': {'outgoing_interface': 'GigabitEthernet3'}}}},
        '192.168.0.1/32': {'route': '192.168.0.1/32',
        'active': True,
        'metric': 2,
        'route_preference': 110,
        'source_protocol_codes': 'O',
        'source_protocol': 'ospf',
        'next_hop': {'next_hop_list': {1: {'index': 1,
            'next_hop': '10.0.0.18',
            'updated': '18:21:32',
            'outgoing_interface': 'GigabitEthernet3'},
            2: {'index': 2,
            'next_hop': '10.0.0.14',
            'updated': '18:21:32',
            'outgoing_interface': 'GigabitEthernet2'}}}},
        '192.168.0.3/32': {'route': '192.168.0.3/32',
        'active': True,
        'source_protocol_codes': 'C',
        'source_protocol': 'connected',
        'next_hop': {'outgoing_interface': {'Loopback0': {'outgoing_interface': 'Loopback0'}}}},
        '192.168.100.1/32': {'route': '192.168.100.1/32',
        'active': True,
        'metric': 52,
        'route_preference': 110,
        'source_protocol_codes': 'O',
        'source_protocol': 'ospf',
        'next_hop': {'next_hop_list': {1: {'index': 1,
            'next_hop': '10.0.0.18',
            'updated': '18:21:26',
            'outgoing_interface': 'GigabitEthernet3'},
            2: {'index': 2,
            'next_hop': '10.0.0.14',
            'updated': '18:21:26',
            'outgoing_interface': 'GigabitEthernet2'}}}}}}}}}}

.. note::
    
    It's much simpler to use the **Dq** library to query the output of the device.

#. Import the **Dq** library.

    .. code-block:: python

        from genie.utils import Dq

#. Make a specific query to the output of the CSR device.

    .. code-block:: python

        csr_output.q.contains('ospf').get_values('routes')

.. tip::
    
    The **Dq** library is very useful to query the output of the device. You can find more information about the **Dq** library in the `pyATS Useful Libraries <https://pubhub.devnetcloud.com/media/genie-docs/docs/userguide/utils/index.html>`_.


.. sectionauthor:: Luis Rueda <lurueda@cisco.com>, Jairo Leon <jaileon@cisco.com>

