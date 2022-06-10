Step 1: Collect Show Commands 
#############################

**Value Proposition:** In this task, we will use the knowledge we have gained from the previous task to write a script that collects the **show inventory** command from each device in the testbed. 
The output of this command will be saved in the file *task2step1.txt* created by the script *task2step1.py*.
The output can be used later if you want to compare the future state of the network with the current one.
Since it is required to collect outputs from all the devices in the testbed, in this task, we will work with the **testbed.devices** object and iterate over all the devices contained in this object to collect an output of the required commands from each device.

#. Let's connect to pyATS and check parts of the code before running the final script.

    .. code-block:: bash

        pyats shell --testbed-file pyats_testbed.yaml

    If everything works correctly, you will see an output similar to the following:

    .. code-block:: bash

        Welcome to pyATS Interactive Shell
        ==================================
        Python 3.9.13 (main, May 24 2022, 21:28:31) 
        [Clang 13.1.6 (clang-1316.0.21.2)]

        >>> from pyats.topology.loader import load
        >>> testbed = load('pyats_testbed.yaml')
        -------------------------------------------------------------------------------            
        In [1]: 


#. Now, let's check the structure of the **testbed.devices** object.

    .. code-block:: python

        print(testbed.devices)

#. Check the output

    .. code-block:: bash

        TopologyDict({'asav-1': <Device asav-1 at 0x7f60bef1da90>, 'csr1000v-1': <Device csr1000v-1 at 0x7f60beee73d0>, 'nx-osv-1': <Device nx-osv-1 at 0x7f60bda8d850>})

    .. note::

        As you can see from the output in the previous step, 'Device <device_name>' objects are contained as dictionary values in the object of TopologyDict class. Therefore, the device names are used as dictionary keys.

#. In this task we will apply standard dictionary method: **items()** to get the **keys** (device names) and **values** (respective device objects). We will iterate over the objects using a Python for-loop.

    .. note::
        As seen in the following code, Python uses indentation (the spaces at the beginning of a code line) to specify code blocks. The indentation is crucial because it determines the scope of the code.

    .. code-block:: python

        from unicon.core.erros import EOF, SubCommandFailure

        # device_name - stores hostname of a device
        # device - stores device object
        for device_name, device in testbed.devices.items():
            device.connect(log_stdout=False)
            # device.execute() method - will used to get the output of "show inventory" command
            try:
                device.execute('show inventory')
                print('##########################\n')
            except SubCommandFailure as e:
                if isinstance(e.__cause__, EOF):
                    print('Connection closed, try to reconnect')
                    device.disconnect()
                    device.connect()


#. Paste the following snippet to the pyATS console:

    - Place the following iPython command at the beginning of the code:

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
                        print('Connection closed, try to reconnect')
                        device.disconnect()
                        device.connect()

    - End the code with ``--``

    - On pyATS shell it would look something like this:

    .. code-block:: bash
        
        In [1]: %cpaste
        Pasting code; enter '--' alone on the line to stop or use Ctrl-D.
        :from unicon.core.errors import EOF, SubCommandFailure
        for device_name, device in testbed.devices.ite:ms():
            print('#########################')
            p::rint(f'#####device_name = {device_name}, device = {device}')
            print(f'#####device_name = {device_:name}, device_object_type = {type(device)}')
            d:evice.connect(log_stdout=False)
            print('#####Ou:tput:')
            try:
                out = device.execute('show inventory')
                print(f'{out}')
            except S::ubCommandFailure as e:
                if isinstance(e.__c:ause__, EOF):
                    print('Connection closed:, try to reconnect')
                    device.disconnect:()
                    device.connect():
        :--

    - As a result, each device should return the output of the **show inventory** command.

    |

    .. note::

        If a device connection is closed or terminated unexpectedly after it has already connected to a device, there will be multiple errors generated (for example, the Python EOF exception would be invoked) at the time of executing the command.
        To address this situation, we will add the following code to reconnect to a device:

        .. code-block:: python

            from unicon.core.errors import EOF, SubCommandFailure
            try:
                device.execute('show inventory')
            except SubCommandFailure as e:
                if isinstance(e.__cause__, EOF):
                    print('Connection closed, try reconnect')
                    device.disconnect()
                    device.connect()

#. Exit the pyATS shell by using the **exit** command. Now we are ready to go through the final version of the script by gathering the commands specified from all the devices in the testbed and saving them to file on Linux (proceed to the next step).

#. Open the prepared script task1step1.py in Nano editor.

    .. code-block:: bash

        nano task1step1.py

#. Before diving into the details of the code, study the explanation of the code given below. The script **task2step1.py** has the following Python functions:

    .. csv-table::
        :file: ./reference/main-fuctions.csv
        :width: 80%
        :header-rows: 1

    .. note::

        To simplify the script, the name of the testbed is hard-coded into the main() function:
        **testbed_filename = 'pyats_testbed.yaml'**
        In subsequent scripts, the name of the testbed file will be provided as a parameter to the script.

    .. image:: images/code-structure.png
        :width: 75%
        :align: center

    .. note::

        The **log_stdout=False** option in **device.connect** call will disable all logging into a screen to this device for the whole connection session (until disconnection takes place or until log_stdout is set to **True**).
        When multiple commands are being executed, it is preferred to avoid logging the output into the screen by using this method.

#. Exit Nano without saving by pressing :guilabel:`Ctrl + X`
    
#. Now run the script:
    
        .. code-block:: bash
    
            python task2step1.py

#. Check that there is a new file created: collected_task4. Then, check the time in which the file was created.

    .. code-block:: bash

        ls -l ~/LTRATO-2001 | grep task2step1.txt
    
    Sample output in Bash shell:

    .. code-block:: bash

        -rw-r--r-- 1 cisco cisco  6.9K Nov  5 17:12 task2step1.txt

#. Check the content of the **task2step1.txt** file.
    
        .. code-block:: bash
    
            cat ~/LTRATO-2001/task2step1.txt

        The output should look similar to the following:
        
        .. code-block:: text

            Name: "Chassis", DESCR: "ASAv Adaptive Security Virtual Appliance"
            PID: ASAv              , VID: V01     , SN: 9AT6971HDTE
            ####
            NAME: "Chassis", DESCR: "Cisco CSR1000V Chassis"
            PID: CSR1000V          , VID: V00  , SN: 9TZZH2O1ZRC

            NAME: "module R0", DESCR: "Cisco CSR1000V Route Processor"
            PID: CSR1000V          , VID: V00  , SN: JAB1303001C

            NAME: "module F0", DESCR: "Cisco CSR1000V Embedded Services Processor"
            PID: CSR1000V          , VID:      , SN:
            ####
            NAME: "Chassis",  DESCR: "Nexus9000 9000v Chassis"               
            PID: N9K-9000v           ,  VID: V02 ,  SN: 9175PXH6Z4G          

            NAME: "Slot 1",  DESCR: "Nexus 9000v Ethernet Module"           
            PID: N9K-9000v           ,  VID: V02 ,  SN: 9175PXH6Z4G          

            NAME: "Fan 1",  DESCR: "Nexus9000 9000v Chassis Fan Module"    
            PID: N9K-9000v-FAN       ,  VID: V01 ,  SN: N/A                  

            NAME: "Fan 2",  DESCR: "Nexus9000 9000v Chassis Fan Module"    
            PID: N9K-9000v-FAN       ,  VID: V01 ,  SN: N/A                  

            NAME: "Fan 3",  DESCR: "Nexus9000 9000v Chassis Fan Module"    
            PID: N9K-9000v-FAN       ,  VID: V01 ,  SN: N/A
            ####

.. sectionauthor:: Luis Rueda <lurueda@cisco.com>, Jairo Leon <jaileon@cisco.com>
