Step 3: pyATS Capabilities using the pyATS Shell
################################################

**Value Proposition:** We believe it's always faster to start learning about pyATS in an interactive format where you can try different pyATS functions. It allows you to run commands and see results immediately, instead of making small changes in Python code and re-running it after every minor change. pyATS has an interactive shell for developing tests. It's run from Bash shell in the following way:

.. code-block:: bash

    pyats shell --testbed-file <testbed_file_name>


We will call the pyATS interactive shell **pyATS shell** throughout this guide.


Let's begin with the pyATS shell, using it with ``pyats_testbed.yaml``, which we've seen in the previous task.

The following pyATS methods would be used in this task:

- pyATS connect
- pyATS execute
- pyATS parse
- pyATS learn
- pyATS diff

#. Enter the following command to run the pyATS shell command from the Bash shell and specify the YAML testbed file as the parameter. After about 10 seconds, the interactive shell opens. This is where you can input the Python code.

    .. code-block:: bash

        pyats shell --testbed-file pyats_testbed.yaml

#. The output of the command should contain the following (version of Python might be different):

    .. code-block:: bash

        Welcome to pyATS Interactive Shell
        ==================================
        Python 3.8.7 (default, Mar 30 2021, 10:31:15)
        [GCC 7.4.0]

#. Check the devices included in the lab's testbed.

    .. code-block:: bash

        In [1]: testbed.devices

#. The output of the command should contain the following:

    .. code-block:: bash

        Out[1]: TopologyDict({'asav-1': <Device asav-1 at 0x7f5342e17210>, 'csr1000v-1': <Device csr1000v-1 at 0x7f5342deced0>, 'nx-osv-1': <Device nx-osv-1 at 0x7f5341998890>})

#. Create variables (Python objects) to call devices easily (**nx - 'nx-osv-1'** device, **asa -'asav-1'** device):

    .. code-block:: python

        nx = testbed.devices['nx-osv-1']
        asa = testbed.devices['asav-1']
    
#. Connect and collect raw output from devices.

    - Connect to devices from the pyATS shell:

        .. code-block:: python

            nx.connect()
            asa.connect()

    - Let's prepare ourselves for our first test and collect **show inventory** command output from the devices.

        .. code-block:: python

            nx_output = nx.parse('show inventory')
            asa_output = asa.parse('show inventory')

#. Verify the collected information in the output of each command. Pay attention to the output of both execute methods returned as plain text (string type in Python):

    .. code-block:: bash

        nx-osv-1#
        Out[6]: 'NAME: "Chassis",  DESCR: "Nexus9000 9000v Chassis" \r\nPID: N9K-9000v,  VID: V02 ,  SN: 9OQ8QSK7JX1 \r\n\r\nNAME: "Slot 1",  DESCR: "Nexus 9000v Ethernet Module" \r\nPID: N9K-9000v,  VID: V02 ,  SN: 9OQ8QSK7JX1 \r\n\r\nNAME: "Fan 1",  DESCR: "Nexus9000 9000v Chassis Fan Module"  \r\nPID: N9K-9000v-FAN,  VID: V01 ,  SN: N/A \r\n\r\nNAME: "Fan 2",  DESCR: "Nexus9000 9000v Chassis Fan Module" \r\nPID: N9K-9000v-FAN,  VID: V01 ,  SN: N/A \r\n\r\nNAME: "Fan 3",  DESCR: "Nexus9000 9000v Chassis Fan Module" \r\nPID: N9K-9000v-FAN,  VID: V01 ,  SN: N/A'
        asav-1#
        Out[7]: 'Name: "Chassis", DESCR: "ASAv Adaptive Security Virtual Appliance"\r\nPID: ASAv, VID: V01, SN: 9AWXBH2QJP7'

#. Collect structured data output using parse command.

    - Import **pprint** python module to represent collected output in pretty format.

        .. code-block:: python

            from pprint import pprint

    - Run **parse** command to convert device output into a Python dictionary, which stores the device data as a set of key-value pairs.

        .. code-block:: python

            nx_output = nx.parse('show inventory')

    - Verify collected information using pprint command.

        .. code-block:: python

            pprint(nx_output)

    - The output of the command should contain the following:

        .. code-block:: bash

            {'name': {'Chassis': {'description': 'Nexus9000 9000v Chassis',
                                'pid': 'N9K-9000v',
                                'serial_number': '9EIFZPG7ZAM',
                                'slot': 'None',
                                'vid': 'V02'},
                    'Fan 1': {'description': 'Nexus9000 9000v Chassis Fan Module',
                                'pid': 'N9K-9000v-FAN',
                                'serial_number': 'N/A',
                                'slot': 'None',
                                'vid': 'V01'},
                    'Fan 2': {'description': 'Nexus9000 9000v Chassis Fan Module',
                                'pid': 'N9K-9000v-FAN',
                                'serial_number': 'N/A',
                                'slot': 'None',
                                'vid': 'V01'},
                    'Fan 3': {'description': 'Nexus9000 9000v Chassis Fan Module',
                                'pid': 'N9K-9000v-FAN',
                                'serial_number': 'N/A',
                                'slot': 'None',
                                'vid': 'V01'},
                    'Slot 1': {'description': 'Nexus 9000v Ethernet Module',
                                'pid': 'N9K-9000v',
                                'serial_number': '9EIFZPG7ZAM',
                                'slot': '1',
                                'vid': 'V02'}}}

    - Since information is collected in Python dictionary, we can call any value, using its key. Collect serial number of chassis using its key.

        .. code-block:: python

            nx_serial = nx_output['name']['Chassis']['serial_number']
            pprint(nx_serial)

#. Collect features state using **learn** command.

    - Run **learn** command to get the state of the feature (**ospf** in our case) into a Python dictionary, which stores the device data as a set of key-value pairs.
    
            .. code-block:: python
    
                ospf_state_before = nx.learn('ospf')

    - Print collected output to observe structure of Python dictionary.

        .. code-block:: python

            pprint(ospf_state_before.info)

    - Run **parse** command to collect interfaces output when network.

        .. code-block:: python

            int_before = nx.parse('show interface')
    
#. Now impose failure in the topology, shutting down the interface **Ethernet1/1** on device **nx-osv-1**.

    - Open Putty terminal using the shortcut on the desktop.
    - Connect to **nx-osv-1** using password **cisco**

        .. image:: images/putty-01.png
            :width: 35%
            :align: center

    - Disable (input **shutdown** command) interface **Ethernet1/1** on **nx-osv-1**. Input the following commands in the console of nx-osv-1:

        .. code-block:: bash

            configure terminal
            interface Ethernet1/1
            shutdown

    - In pyATS shell run **learn** command to get the state of the feature (**ospf** in our case) into a Python dictionary, which stores the device data as a set of key-value pairs.
    
        .. code-block:: python

            ospf_state_after = nx.learn('ospf')

    - Import PyATS **Diff** package and compare previous (working) and current state (failed) to understand what have changed and further troubleshoot the problem.

        .. code-block:: python

            from genie.utils.diff import Diff
            diff = Diff(ospf_state_before.info, ospf_state_after.info)
            diff.findDiff()
            print(diff)

    - PyATS Diff can compare outputs of structured data collected by parse command.
    - Parse **show interface** to collect interfaces output into a Python dictionary.
    
            .. code-block:: python
    
                int_after = nx.parse('show interface')

    - Compare before and after outputs, using PyATS Diff package.
        
            .. code-block:: python
    
                diff2 = Diff(int_before, int_after)
                diff2.findDiff()
                print(diff2)
  
    - Enable (input **no shutdown** command) interface **Ethernet1/1** on **nx-osv-1**. Input the following commands in the console of nx-osv-1:
    
            .. code-block:: bash
    
                configure terminal
                interface Ethernet1/1
                no shutdown

    - Exit the pyATS shell by using the exit command and proceed to the next step.

#. PyATS parse/learn and diff commands can be run right from Linux Shell, and you can start using PyATS without coding skills.

    - Observe PyATS capabilities from Linux Shell running pyATS parse command from Linux Shell:

        .. code-block:: bash

            pyats parse "show interface" --devices nx-osv-1 --testbed-file pyats_testbed.yaml --output parse-work/
    
    - Run pyATS learn command from Linux Shell for feature OSPF:

        .. code-block:: bash

            pyats learn ospf --devices nx-osv-1 --testbed-file pyats_testbed.yaml --output working/
    
    - Disable (input **shutdown** command) interface **Ethernet1/1** on **nx-osv-1**.

        .. code-block:: bash

            configure terminal
            interface Ethernet1/1
            shutdown

    - Return to Linux Shell and collect outputs after failure running pyATS parse command from Linux Shell:

        .. code-block:: bash

            pyats parse "show interface" --devices nx-osv-1 --testbed-file pyats_testbed.yaml --output parse-failed/

    - Run pyATS learn command from Linux Shell for feature OSPF:
    
        .. code-block:: bash

            pyats learn ospf --devices nx-osv-1 --testbed-file pyats_testbed.yaml --output failed/

    -  Run pyATS diff for parsed commands from Linux Shell:

        .. code-block:: bash

            pyats diff parse-work parse-failed
            cat ./diff_nx-osv-1_show-interface_parsed.txt

    - Run pyATS diff for learned states from Linux Shell:

        .. code-block:: bash

            pyats diff working failed
            cat ./diff_ospf_nxos_nx-osv-1_ops.txt

    - Don't forget to enable (input **no shutdown** command) interface **Ethernet1/1** on **nx-osv-1**:

        .. code-block:: bash

            configure terminal
            interface Ethernet1/1
            no shutdown



.. sectionauthor:: Luis Rueda <lurueda@cisco.com>, Jairo Leon <jaileon@cisco.com>

