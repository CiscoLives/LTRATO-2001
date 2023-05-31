Step 3: Verify the Routing Information using Parsers and pyATS Learn
####################################################################

**Value Proposition:** In this test case, we have the list of critical routes (this is usually a device's loopback interface) and we must check that these loopbacks are installed in the routing information base (RIB) of all the devices in the testbed.

The high-level logic of the tests will be the following:

- Connect to each device in the testbed.
- Learn the routing information from the device's RIB.
- Verify that all critical routes are present in the device's RIB.

#. Let's connect to the pyATS shell and check our idea.

    .. code-block:: bash

        pyats shell --testbed-file pyats_testbed.yaml

#. Paste the following code into the pyATS shell:

    .. code-block:: python

        csr = testbed.devices['csr1000v-1']
        asa = testbed.devices['asav-1']
        nx = testbed.devices['nx-osv-1']
        csr.connect(log_stdout=False)
        asa.connect(log_stdout=False)
        nx.connect(log_stdout=False)

    pyATS uses the **learn** method to collect the set of show commands output for a feature configured on the device, get its snapshot, and store it in a structured format (Python dictionary).

    .. code-block:: python

        csr_routes = csr.learn('routing')
        nx_routes = nx.learn('routing')

    Now we can observe the structure of the parsed outputs. We will start with the parsed output for the **csr1000v-1**.

#. Paste the following code into the pyATS shell:

    .. code-block:: python

        import pprint
        pprint.pprint(csr_routes.info)

#. Observe the output in pyATS shell:

    .. code-block:: bash
        :emphasize-lines: 17, 18

        In [3]: import pprint
            ...: pprint.pprint(csr_routes.info)
        {'vrf': {'Mgmt-intf': {'address_family': {'ipv4': {'routes': {'0.0.0.0/0': {'active': True,
                                                                            'metric': 0,
                                                                            'next_hop': {'next_hop_list': {1: {'index': 1,
                                                                                                               'next_hop': '198.18.1.1'}}},
                                                                            'route': '0.0.0.0/0',
                                                                            'route_preference': 1,
                                                                            'source_protocol': 'static',
                                                                            'source_protocol_codes': 'S*'},
                                                              '198.18.1.201/32': {'active': True,
                                                                                  'next_hop': {'outgoing_interface': {'GigabitEthernet1': {'outgoing_interface': 'GigabitEthernet1'}}},
                                                                                  'route': '198.18.1.201/32',
                                                                                  'source_protocol': 'local',
                                                                                  'source_protocol_codes': 'L'}}}}},
         'default': {'address_family': {'ipv4': {'routes': {'10.0.0.12/30': {'active': True,
                                                                             'next_hop': {'outgoing_interface': {'GigabitEthernet2': {'outgoing_interface': 'GigabitEthernet2'}}},
                                                                             'route': '10.0.0.12/30',
                                                                             'source_protocol': 'connected',
                                                                             'source_protocol_codes': 'C'},
                                                            '10.0.0.13/32': {'active': True,
                                                                             'next_hop': {'outgoing_interface': {'GigabitEthernet2': {'outgoing_interface': 'GigabitEthernet2'}}},
                                                                             'route': '10.0.0.13/32',
                                                                             'source_protocol': 'local',
                                                                             'source_protocol_codes': 'L'},

        # ...
    
    Now we understand that the routes for **csr1000v-1** are stored under the following path:

    .. code-block:: python

        pprint.pprint(csr_routes.info['vrf']['default']['address_family']['ipv4']['routes'])

    For **nx-osv-1**, RIB routes are stored under the same path as for **csr1000v-1**:

    .. code-block:: python

        pprint.pprint (nx_routes.info['vrf']['default']['address_family']['ipv4']['routes'])

#. Exit the pyATS shell using the **exit** command.

#. Open the file task3step3.py in **Nano** editor.

    .. code-block:: bash

        nano task3step3.py

#. Review the content of the **routes** test case. Note that we use the path to routes from the previous step to get the routing information. First, we'll get a snapshot of the **routing** feature.

    .. code-block:: python
        :emphasize-lines: 9

            @aetest.test
            def routes(self, device):
                """
                Verify that all devices have golden_routes installed in the RIB
                """

                if (device.os == 'iosxe') or (device.os == 'nxos'):

                    output = device.learn('routing')
                    rib = <<replace me>>  # noqa: E999

8. Then we compare the loopback routes stored in **golden_routes list** with the content of rib. If the loopback route is not found, then we force the test case to fail.

    .. code-block:: python

        golden_routes = ['192.168.0.3/32', '192.168.0.1/32']

    .. code-block:: python
        :emphasize-lines: 1, 3

        for route in golden_routes:
            if route not in rib:
                self.failed(f'{route} is not found')
            else:
                pass
    
    .. note::
        Golden routes are /32 networks of loopback interfaces on **csr1000v-1** and **nx-osv-1**.

    Loopback0 on **csr1000v-1**:

    .. code-block:: bash
        :emphasize-lines: 6

        csr1000v-1#sh ip int br
        Interface              IP-Address      OK? Method Status                Protocol
        GigabitEthernet1       198.18.1.201    YES TFTP   up                    up
        GigabitEthernet2       10.0.0.13       YES TFTP   up                    up
        GigabitEthernet3       10.0.0.17       YES TFTP   up                    up
        Loopback0              192.168.0.3     YES TFTP   up                    up

    Loopback0 on **NX-OS**:

    .. code-block:: bash
        :emphasize-lines: 5

        nx-osv-1# sh ip interface brief vrf all
 
        IP Interface Status for VRF "default"(1)
        Interface            IP Address      Interface Status
        Lo0                  192.168.0.1     protocol-up/link-up/admin-up
        Eth1/1               10.0.0.14       protocol-up/link-up/admin-up
        Eth1/2               10.0.0.18       protocol-up/link-up/admin-up
        Eth1/3               10.0.0.6        protocol-up/link-up/admin-up
        
        IP Interface Status for VRF "management"(2)
        Interface            IP Address      Interface Status
        mgmt0                198.18.1.203    protocol-up/link-up/admin-up
        
        IP Interface Status for VRF "inside"(3)
        Interface            IP Address      Interface Status
        Lo100                192.168.100.1   protocol-up/link-up/admin-up
        Eth1/4               10.0.0.10       protocol-up/link-up/admin-up

#. Complete this test case by replacing the ``<<replace me>>`` statement with a rib variable. To accomplish this, you must paste the path to the rib routes, which you figured out during the previous step:

    .. code-block:: python

        output.info['vrf']['default']['address_family']['ipv4']['routes']

    .. code-block:: python

        # Before inserting the rib variable:
        rib = <<replace me>>  # noqa: E999

        # After inserting the rib variable:
        rib = output.info['vrf']['default']['address_family']['ipv4']['routes']

#. When you finish, save changes to file **task3step3.py** by pressing

    .. code-block:: bash

        Ctrl + O
        File Name to Write: task3step3.py
        Hit [Enter]

#. Execute the test script and check the results section:

    .. code-block:: bash

        python task3step3.py --testbed pyats_testbed.yaml

    .. image:: images/task8_labpyats.png
        :width: 75%
        :align: center
    
    |

    .. note::
        For a list of definitions of test results, please go to this `link <https://pubhub.devnetcloud.com/media/pyats/docs/results/objects.html>`__

|

.. sectionauthor:: Luis Rueda <lurueda@cisco.com>, Jairo Leon <jaileon@cisco.com>
