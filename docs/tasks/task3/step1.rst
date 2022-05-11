Step 1: Verify Log Messages
###########################

**Value Proposition:** In this test case, we will verify that the logging messages with ERROR or WARN are not present on the devices in the testbed.

The high-level logic of the test case will be as follows:

- Connect to each device in the testbed.
- Collect the output of ``show logging | i ERROR|WARN``.
- If the output contains more than 0 strings, then ERROR messages were found and the test should fail for this device. Otherwise, the test should succeed.

#. Before creating our testcase, connect to ASA. Launch **PuTTY** and connect to **asav-1**.

    .. code-block:: bash
        :emphasize-lines: 3, 5

        User Access Verification

        Password: cisco
        asav-1> enable
        Password: cisco
        asav-1#
        asav-1# clear logging buffer
        asav-1#

#. Let's open the pyATS shell and check it out.

    .. code-block:: bash

        pyats shell --testbed-file pyats_testbed.yaml

#. Input the following code into pyATS shell:

    .. code-block:: bash

        In [1]: csr = testbed.devices['csr1000v-1']
        asa = testbed.devices['asav-1']
        csr.connect()
        asa.connect()

#. Let's verify whether there are any errors or warning messages in the logs:


    .. code-block:: bash

        In [1]: out1 = csr.execute('show logging | i ERROR|WARN')
        out2 = asa.execute('show logging | i ERROR|WARN')

    .. note::

        The output for ASA should be empty.
        If you don’t see any ERROR logs on the csr1000v-1 device, then:

        1. Connect to CSR:
            - Launch PuTTY and connect to **csr1000v-1**. Username: ``cisco``, password: ``cisco``
        2. Generate a test ERROR message:
            - csr1000v-1# **send log 'Test ERROR message for pyATS'**
        3. Repeat step 3 above for CSR in the pyATS shell:
            - **out1 = csr.execute('show logging | i ERROR|WARN')**

#. To check whether there is an empty or non-empty output, we will use the Python **len()** built-in function, which returns the length of the given string. If the collected output is empty, then **len()** of the output will be 0, otherwise, the result will be greater than 0.

    Input into pyATS shell:

        .. code-block:: bash

            In [1]: len(out2)

    The resulting length is 0, means output from ASA is empty:

        .. code-block:: bash

            In [1]: 0

    Input into pyATS shell:

        .. code-block:: bash

            In [1]: len(out1)

    The resulting length is greater than 0, which means the output from CSR is not empty:

        .. code-block:: bash

            In [1]: 664
    
#. Exit pyATS shell using the **exit** command.

#. Open the file task61_labpyats.py in Nano editor:

    .. code-block:: bash

        nano task61_labpyats.py

    This file reuses the establish_connections(self, testbed) method from task5_labpyats.py (used in previous scenarios), which make connections to all devices in the testbed.

    .. note::
        Pay special attention to the following code:
        
    The method self.parent.parameters.update(dev=device_list), located at the end of the establish_connections(self,testbed) method.

    .. code-block:: python
        :emphasize-lines: 20

        @aetest.subsection
        def establish_connections(self, pyats_testbed):
            """
            Establishes connections to all devices in testbed
            :param testbed:
            :return:
            """

            device_list = []
            for device in pyats_testbed.devices.values():
                log.info(banner(
                    f"Connect to device '{device.name}'"))
                try:
                    device.connect(log_stdout=False)
                except errors.ConnectionError:
                    self.failed(f"Failed to establish "
                                f"connection to '{device.name}'")
                device_list.append(device)
            # Pass list of devices to testcases
            self.parent.parameters.update(dev=device_list)


    Where **self.parent.parameters** is an attribute of class **aetest**, and **aetest** is the class from which all the testcase classes and **MyCommonSetup** class are inherited from:

    class MyCommonSetup(aetest.CommonSetup):
    <…>

    class VerifyLogging(aetest.Testcase):
    <…>

    Using **self.parent.parameters** attribute arguments can be passed between different classes.
    As an example, in the class **MyCommonSetup**, we store all the devices from the variable **device_list** in the parameter **parameters['dev']**.
    self.parent.parameters.update(dev=device_list)
    Then we can access all the devices in class VerifyLogging, using the method **self.parent.parameters['dev']**.

#. Pay special attention to the code in class **VerifyLogging**, which is used to implement the approach that has been tested using the pyATS shell: if length of output is greater than zero, it means that output contains ERROR or WARN message. Testcase should be marked as Failed in this case.

    - The **device.connect(log_stdout=False)** is used in this example (see **def establish_connections**).
    - This code (log_stdout=False) - disables all logging to a screen for the whole connection session. To make the execution of the command on a device visible **(show logging | i ERROR|WARN)** in the output of the test, the following code is used: **any_device.log_user(enable=True)**

    |

    .. code-block:: python
        :emphasize-lines: 1

        class VerifyLogging(aetest.Testcase):
            <..>
            @aetest.test
            def error_logs(self):
                any_device = self.parent.parameters['dev'][0]
                any_device.log_user(enable=True)
                output = any_device.execute('show logging | i ERROR|WARN')

                if len(output) > 0:
                    self.failed('Found ERROR in log, review logs first')
                else:
                    pass

#. Note that the Setup section of the test case is not used, therefore **pass** is written in this function. We will use the Setup section of the test case later when we execute the **show logging | i ERROR|WARN** command on multiple devices.

    .. code-block:: python
        :emphasize-lines: 3

        @aetest.setup
        def setup(self):
            pass

#. Exit Nano without saving, pressing:

    .. code-block:: bash

        Ctrl+X

#. Execute the test script **task61_labpyats.py** and check the results section.

    The Testcase **error_log** will run only for one device. Scroll above the results section and you will see to which device is related to this output.

    .. image:: images/error-log.png
        :width: 75%
        :align: center
    
    We have learned how to run a testcase for only one device, now we need to get familiar with the **aetest.loop** method, which will let us repeat an elementary test case (written for one device) for every device in the testbed.

#. Open the file task62_labpyats.py once again.

    .. code-block:: bash

        nano task62_labpyats.py
    
    .. note::
        In this task we will learn dynamic loops, which will create loops based on information that is only available during a script run.

        This approach is helpful if we don't want to hardcode device names inside our testcase, but want to dynamically load devices from testbed file and run testcases across them.

#. Pay special attention to the code in **error_logs** method. It receives **device** object as an argument on input and collects the command from this **device**.

    .. code-block:: python
        :emphasize-lines: 2-3

        @aetest.test
        def error_logs(self, device):
            output = device.execute('show logging | i ERROR|WARN')

            if len(output) > 0:
                self.failed('Found ERROR in log, review logs first')
            else:
                pass

#. Next, check the **setup(self)** method of class **VerifyLogging**. Method **setup(self)** is used to load all the devices from the testbed and to run the **error_logs** method for each device.

    .. code-block:: python
        :emphasize-lines: 4

        @aetest.setup
        def setup(self):
            devices = self.parent.parameters['dev']
            aetest.loop.mark(self.error_logs, device=devices)

    .. note::
        **aetest.loop.mark()** instructs method **self.error_logs** to take an argument for input variable 'device', one-by-one from the devices list and run a testcase for each device separately.

#. Exit Nano without saving, pressing:

    .. code-block:: bash
            
            Ctrl+X

#. Execute the test script; testcase **error_logs** will run for all the devices in the testbed:

    .. code-block:: bash

        python task62_labpyats.py --testbed pyats_testbed.yaml

#. Check the **VerifyLogging** results section. The test for **asav-1** should pass, whereas for **csr1000v-1** and **nx-osv-1** should fail, because these devices have error messages in the logs.

    .. image:: images/error-log-results.png
        :width: 75%
        :align: center


.. sectionauthor:: Luis Rueda <lurueda@cisco.com>, Jairo Leon <jaileon@cisco.com>