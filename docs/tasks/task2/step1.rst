Step 1: Collect Show Commands 
#############################

**Value Proposition:** In this task, we will use the knowledge we have gained from the previous task to write a script that collects **show inventory** command from each device in the testbed. The output of this command will be saved in the file created by the script collected_task4. These outputs can be used later if you want to compare the future state of the network with the current one. Since it's required to collect outputs from all the devices in the testbed, in this task we will work with the **testbed.devices** object, and iterate over all the devices contained in this object to collect an output of the required commands from each device.

#. Let's connect to pyATS and check parts of the code before running the final script. In the beginning, we will check the structure of **testbed.devices** object.

    .. code-block:: python

        pyats shell --testbed-file pyats_testbed.yaml
        print(testbed.devices)

#. Check the output

    .. code-block:: bash

        TopologyDict({'asav-1': <Device asav-1 at 0x7f60bef1da90>, 'csr1000v-1': <Device csr1000v-1 at 0x7f60beee73d0>, 'nx-osv-1': <Device nx-osv-1 at 0x7f60bda8d850>})

    .. note::

        As you can see from the output in the previous step, 'Device <device_name>' objects are contained as dictionary values in the object of TopologyDict class. The device names are used as dictionary keys.

#. In this task we will apply standard dictionary method: **items()** to get **keys** (device names) and **values** (respective device objects). To iterate, the for loop will be used:

    .. code-block:: python

        # device_name - stores hostname of a device
        # device - stores device object
        for device_name, device in testbed.devices.items():
            device.connect()
        
            # device.execute() method - will used to get the output of "show inventory" command
            try:
                device.execute('show inventory')
                print('##########################\n')

    .. note::
        Python uses Indentation (the spaces at the beginning of a code line) to specify code blocks. The indentation is important because it determines the scope of the code.

    .. image:: images/indentation-example.png
        :width: 75%
        :align: center

#. Paste the following snippet to pyATS console:

    - Place the following iPython command in the beginning of code:

        .. code-block:: python

            %cpaste
    
    - Copy and paste the code into the pyATS console:

        .. code-block:: python

            from unicon.core.errors import EOF, SubCommandFailure
            for device_name, device in testbed.devices.items():
                print('#########################')
                print(f'#####device_name = {device_name}, device = {device}')
                print(f'#####device_name = {device_name}, device_object_type = {type(device)}')
                device.connect(log_stdout=False)
                print('#####Output:')
                try:
                    out = device.execute('show inventory')
                    print(f'{out}')
                except SubCommandFailure as e:
                    if isinstance(e.__cause__, EOF):
                        print('Connection closed, try reconnect')
                        device.disconnect()
                        device.connect()

    - End the code with ``--``

#. Check the result of this code. Now each device should return the output of **show inventory** command.

    .. note::

        If a device connection is closed or terminated unexpectedly after it has already connected to a device, there will be multiple errors generated (for example, the Python EOF exception would be invoked) at the time of executing the commmand.
        To handle this situation, it's required to add the following code to reconnect to a device in case that a broken connection to a device is detected:

        .. code-block:: python

            from unicon.core.errors import EOF, SubCommandFailure
            try:
                device.execute('show inventory')
            except SubCommandFailure as e:
                if isinstance(e.__cause__, EOF):
                    print('Connection closed, try reconnect')
                    device.disconnect()
                    device.connect()

#. Exit the pyATS shell by using the **exit** command. Now we are ready to go through the final version of the script by gathering commands specified from all the devices in the testbed and saving them to file on Linux (proceed to the next step).

#. Open the prepared script task4_labpyats.py in Nano editor.

    .. code-block:: bash

        nano task4_labpyats.py

#. Before diving into the details of the code, study the explanation of the code given below. The script **task4_labpyats.py** has the following Python functions:

    .. csv-table::
        :file: ./reference/main-fuctions.csv
        :width: 80%
        :header-rows: 1

    .. note::

        To simplify the script, the name of the testbed is hard-coded into the main():
        **testbed_filename = '/home/cisco/labpyats/pyats_testbed.yaml'**
        In further scripts, the name of a testbed file will be inputed as a parameter of the script.

    .. image:: images/code-structure.png
        :width: 75%
        :align: center

    .. note::

        **log_stdout=False** option in **device.connect** call:
        **device.connect(log_stdout=False)**
        This will disable all logging into a screen to this device for the whole connection session (until disconnection takes place or until log_stdout is set to **True**).
        For the script to collect many commands, it would be preferred to prune the output of the commands to the console using this method.

#. Exit Nano without saving, pressing:
    
        .. code-block:: bash
    
            Ctrl + X
    
#. Now run the script:
    
        .. code-block:: bash
    
            python task4_labpyats.py

#. Check that there is a new file created: collected_task4. Check the time in which it was created.

    .. code-block:: bash

        ls -l ~/labpyats | grep collected_task4
    
    Sample output in Bash shell:

    .. code-block:: bash

        -rw-r--r-- 1 cisco cisco  6.9K Nov  5 17:12 collected_task4

#. Check content of collected_task4 file.
    
        .. code-block:: bash
    
            cat ~/labpyats/collected_task4


.. sectionauthor:: Luis Rueda <lurueda@cisco.com>, Jairo Leon <jaileon@cisco.com>
