Step 3: Verify the Routing Information using Parsers and pyATS Learn
####################################################################

**Value Proposition:** In this test case, we have the list of critical routes (usually this is a device’s loopback interface) and we must check that these loopbacks are installed in the routing information base (RIB) of all the devices in the testbed.

The high-level logic of the test will be as follows:

- Connect to each device in the testbed.
- Learn routing information from RIB of the devices.
- Verify whether all the critical routes are presented in the device's RIB.

#. Let's connect to the pyATS shell and check our idea.

    .. code-block:: bash

        pyats shell --testbed-file pyats_testbed.yaml

#. Input the following code into pyATS shell:

    .. code-block:: python

        csr = testbed.devices['csr1000v-1']
        asa = testbed.devices['asav-1']
        nx = testbed.devices['nx-osv-1']
        csr.connect()
        asa.connect()
        nx.connect()

    pyATS uses the **learn** method to collect the set of show commands output for a feature configured on the device, in order to get its snapshot and store it into a structured format (Python dictionary).

    .. code-block:: python

        csr_routes = csr.learn('routing')
        nx_routes = nx.learn('routing')

    Now we can observe the structure of the parsed outputs. We are starting with the parsed output for **csr1000v-1**.

#. Input the following code into pyATS shell:

    .. code-block:: python

        import pprint
        pprint.pprint(csr_routes.info)

#. Observe the output in pyATS shell:

    .. code-block:: bash
        :emphasize-lines: 2, 16

        {
            "vrf": {"default": {"address_family": {"ipv4": {"routes": {
                                "10.0.0.12/30": {
                                    "active": True,
                                    "next_hop": {
                                        "outgoing_interface": {
                                            "GigabitEthernet2": {
                                                "outgoing_interface": "GigabitEthernet2"
                                            }
                                        }
                                    },
                                    "route": "10.0.0.12/30",
                                    "source_protocol": "connected",
                                    "source_protocol_codes": "C"
                                },
                                "10.0.0.13/32": {
                                    "active": True,
                                    "next_hop": {
                                        "outgoing_interface": {
                                            "GigabitEthernet2": {
                                                "outgoing_interface": "GigabitEthernet2"
                                            }
                                        }
                                    },
                                    "route": "10.0.0.13/32",
                                    "source_protocol": "local",
                                    "source_protocol_codes": "L"
                                }
                            }
                        }
                    }
                }
            }
        }
        <...>
    
    Now we understand that RIB routes for **csr1000v-1** are stored under the following path:

    .. code-block:: python

        pprint.pprint(csr_routes.info['vrf']['default']['address_family']['ipv4']['routes'])

    For **nx-osv-1**, RIB routes are stored under the same path as for **csr1000v-1**:

    .. code-block:: python

        pprint.pprint (nx_routes.info['vrf']['default']['address_family']['ipv4']['routes'])

#. Exit the pyATS shell using the **exit** command.

#. Open the file task8_labpyats.py in Nano editor.

    .. code-block:: bash

        nano task8_labpyats.py

#. Review the content of **routes** testcase. Note that we use the path to routes in RIB from the previous step to get the routing information. First, we'll get a snapshot of the **routing** feature.

    .. code-block:: python
        :emphasize-lines: 9

            @aetest.test
            def routes(self, device):
                """
                Verify that all device have golden_routes installed in RIB
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

#. Complete this test case by replacing the ``<<replace me>>`` statement with a rib variable. To accomplish this, you must paste the path to the rib routes, which was explored in the previous step:

    .. code-block:: python

        output.info['vrf']['default']['address_family']['ipv4']['routes']

    .. code-block:: python

        # Before inserting the rib variable:
        rib = <<replace me>>  # noqa: E999

        # After inserting the rib variable:
        rib = output.info['vrf']['default']['address_family']['ipv4']['routes']

#. When you finish, save changes to file **task8_labpyats.py** by pressing

    .. code-block:: bash

        Ctrl + O
        File Name to Write: task8_labpyats.py
        Hit [Enter]

#. Execute the test script and check the results section:

    .. code-block:: bash

        python task8_labpyats.py --testbed pyats_testbed.yaml

    .. image:: images/task8_labpyats.png
        :width: 75%
        :align: center

|

.. sectionauthor:: Luis Rueda <lurueda@cisco.com>, Jairo Leon <jaileon@cisco.com>
