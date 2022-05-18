Step 2: Verify the Service Contracts Coverage
#############################################

**Value Proposition:** In this test case, we have the list of the devices' serial numbers, covered by the service contracts, and we must verify that all the devices in the testbed are covered by the service contracts. This ensures you will be able to open a TAC case if something goes wrong when the network is in production.

High-level logic of the test will be as follows:
- Connect to each device in the testbed.
- Parse the output of show inventory to find the device's serial number (SN).
- Verify whether the SN is in the list, covered by the service contracts.

#. Let's use the pyATS shell to check our idea.

    .. code-block:: bash

        pyats shell --testbed-file pyats_testbed.yaml

#. Input the following code into pyATS shell:

    .. code-block:: bash

        In [1]: csr = testbed.devices['csr1000v-1']
        asa = testbed.devices['asav-1']
        nx = testbed.devices['nx-osv-1']
        csr.connect()
        asa.connect()
        nx.connect()

#. pyATS uses the **parse** method to collect the output of different show commands and parses it into a structured format (Python dictionary). Let's collect the output of 'show inventory' commands and parse it using the **parse** method.

    .. code-block:: bash

        In [1]: out1 = csr.parse('show inventory')
        out2 = asa.parse('show inventory')
        out3 = nx.parse('show inventory')

#. Now we can observe the structure of parsed outputs. We are starting with the parsed output for **csr1000v-1**. Review it and pay special attention to the highlighted sections.

    .. note::
        The Python library **pprint** will be imported in this task. This is used to break the output (Python dictionary) onto multiple lines, which is easier to check, instead of having it all on one line.

    .. code-block:: python

        import pprint
        pprint.pprint(out1)

#. Observe the output:

    .. code-block:: bash
        :emphasize-lines: 1, 4

        Out [1]: {'main': {'chassis': {'CSR1000V': {'descr': 'Cisco CSR1000V Chassis',
                                   'name': 'Chassis',
                                   'pid': 'CSR1000V',
                                   'sn': '9KZZ4X737UP',
                                   'vid': 'V00'}}},

#. Get the serial number of **csr1000v-1**

    .. code-block:: bash

        In [1]: out1['main']['chassis']['CSR1000V']['sn']

#. The result of the code should contain a serial number collected in the previous step.

    .. code-block:: bash

        Out [1]: '9KZZ4X737UP'

#. Obtain the parsed output for **asav-1**

    .. code-block:: bash

        In [1]: pprint.pprint(out2)

#. Observe the output:

    .. code-block:: bash

        Out [1]: {'Chassis': {'description': 'ASAv Adaptive Security Virtual Appliance',
             'pid': 'ASAv',
             'sn': '9ABUANH9G5F',
             'vid': 'V01'}}

#. Get the serial number of **asav-1**

    .. code-block:: bash

        In [1]: out2['Chassis']['sn']

#. The result of the code should contain a serial number collected in the previous step.

    .. code-block:: bash

        Out [1]: '9ABUANH9G5F'

#. Obtain the parsed output for **nx-osv-1**

    .. code-block:: bash

        In [1]: pprint.pprint(out3)

#. Observe the output:

    .. code-block:: bash

        Out [1]: {'name': {'Chassis': {'description': 'Nexus9000 9000v Chassis',
                      'pid': 'N9K-9000v',
                      'serial_number': '9712TV4C2JF',
                      'slot': 'None',
                      'vid': 'V02'},

#. Get the serial number of **nx-osv-1**

    .. code-block:: bash

        In [1]: out3['name']['Chassis']['serial_number']

#. The result of the code should contain a serial number collected in the previous step.

    .. code-block:: bash

        Out [1]: '9712TV4C2JF'
    
    Now we have all the needed information to write the next test script.

#. Exit the pyATS shell using the **exit** command.

#. Open the file task7_labpyats.py in Nano editor:

    .. code-block:: bash

        nano task7_labpyats.py

#. Review the content of the **Inventory** test case. Note that we use the data structure learned from pyATS shell in the previous step to extract a serial number from the output of **show inventory**:

    .. code-block:: python
        :emphasize-lines: 5

        @aetest.test
        def inventory(self,device):
            if device.os == 'iosxe':
                out1 = device.parse('show inventory')
                chassis_sn = out1['main']['chassis']['CSR1000V']['sn']

    .. note::
        The path to fetch the serial number from the structures has been explored in the previous step with pyATS shell. Variables out2 and out3 are used:

    .. code-block:: python
        :emphasize-lines: 3

        elif device.os == 'nxos':
            out2 = device.parse('show inventory')
            chassis_sn = out2['name']['Chassis']['serial_number']

    The serial number shown below is provided as an example. It would be different on the equipment in a lab.

    .. code-block:: python
        :emphasize-lines: 3

        elif device.os == 'asa':
            out3 = device.parse('show inventory')
            chassis_sn = out3['Chassis']['sn']

#. Exit Nano without saving, pressing:

    .. code-block:: bash

        Ctrl+X

#. Execute the test script and check the **Detailed Results** section.

    .. code-block:: bash

        python task7_labpyats.py --testbed pyats_testbed.yaml

    What are the results of these testcases? All fails? Do you have a clue as to why? Continue for the correct answer.

    .. image:: ./images/task7_labpyats_1.png
        :width: 75%
        :align: center

    |
    
    All the tests have failed since we have serial numbers from a different network in our contract SNs list at the beginning of **task7_labpyats.py** file.

    .. code-block:: python

        contract_sn = ['9AQHSSAS8AU', '9Q3YV06WJ71', '9IFUH4GPSGL']

#. Open the file task7_labpyats.py in Nano editor.

    .. code-block:: bash

        nano task7_labpyats.py

#. Replace the serial numbers in the list **contract_sn** with SNs from our testbed's equipment.

#. When you finish, save changes to file task7_labpyats.py by pressing:

    .. code-block:: bash

        Ctrl + O
        File Name to Write: task7_labpyats.py
        Hit [Enter]

    .. note::
        Correct SNs from testbed can be obtained also from previous script's output:

        2020-01-23T13:20:24: %AETEST-ERROR:Failed reason: 9AQHSSAS8AU is not covered by contract

        <…>

        2020-01-23T13:20:25: %AETEST-ERROR:Failed reason: 9Q3YV06WJ71 is not covered by contract

        <…>
        
        2020-01-23T13:20:26: %AETEST-ERROR:Failed reason: 9IFUH4GPSGL is not covered by contract

#. Еxecute the modified test script once again:

    .. code-block:: bash

        python task7_labpyats.py --testbed pyats_testbed.yaml

    Now all the testcases should succeed:

    .. image:: ./images/task7_labpyats_2.png
        :width: 75%
        :align: center


.. sectionauthor:: Luis Rueda <lurueda@cisco.com>, Jairo Leon <jaileon@cisco.com>
