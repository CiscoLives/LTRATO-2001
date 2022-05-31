Step 2: Writing Test Script
############################

**Value Proposition:** We will write our first test script on Python using the pyATS library.
Our test script will connect to all the devices in the testbed and print the results of the connection.
If the connections to all the devices are successful, the test will pass; otherwise, it will fail.
Using this simple test script, we will learn the structure of the pyATS test script file.

The pyATS test script is a file in Python code that uses the pyATS library.
The structure of the pyATS test script is modular and straightforward.
Each test script is written in a Python file and split into three major sections (Python classes) – see the illustration below for a graphical representation:

- **Common Setup:** The first section of the test script runnned at the beginning. It performs all the "common" setups required for the script.
- **Testcase(s):** A self-contained individual unit of testing. Each testcase is independent of the other testcases.
- **Common Cleanup:** The last section in the test script. It performs all the "common" cleanups at the end of execution.

Each of these sections is further broken down into smaller subsections (Python methods of the class).

.. note::
    There can be only one Common Setup and only one Common in a script, whereas there might be multiple test cases in one test script.

.. image:: images/test-script-structure.png
    :width: 75%
    :align: center

#. Let's verify our first test script. Open the file **task2step2.py** and observe its structure:

    .. code-block:: bash

        nano task2step2.py

#. Pay special attention to the following part of the code. Whereas it's not only related to this task, it will help you understand the logging capabilities of pyATS that will be used in other tasks during this lab:

    .. code-block:: python

        # To get a logger for the script
        import logging

        # Get your logger for your script
        LOGGER = logging.getLogger(__name__)
        LOGGER.setLevel(logging.INFO)

#. When the pyATS banner is used, the following message will be displayed in the test output.

    .. code-block:: bash

        Connecting to device 'csr1000v-1'...

    .. image:: images/pyats-logger-banner.png
        :width: 75%
        :align: center

    |

    .. note::

        The pyATS logging banner itself does not perform logging; it only formats input messages.
        Hence, the **log.info(banner("logging message"))** construction is used in the code for logging.
        Since the banner is logged with INFO logging level, it's required to set the logging level up to INFO (default is WARNING):
        **log.setLevel(logging.INFO)**

#. Let's look at the main contents of this example. Python class **common_setup**, which inherits from **aetest.CommonSetup** represents the major section, “Common Setup” (see the following illustration).  The Python class **common_setup** is where initializations happen. This initialization is required before executing any tests. For this reason, the code in class **common_setup** is always executed first. The following snippet of code is taken from the task2step2.py file:

    .. code-block:: python

        class common_setup(aetest.CommonSetup):
        """Common Setup section"""

        @aetest.subsection
        def establish_connections(self, pyats_testbed):
            device_list = []
            # Load all devices from testbed file and try to connect to them
            for device in pyats_testbed.devices.values():
                LOGGER.info(banner(f"Connecting to device '{device.name}'..."))
                try:
                    device.connect(log_stdout=False)
                except errors.ConnectionError:
                    self.failed(f"Failed to establish a connection to '{device.name}'")
                device_list.append(device)
            # Pass list of devices to testcases
            self.parent.parameters.update(dev=device_list)

    The following code is used to load a testbed file from the filename specified in the command-line option (**--testbed** is a command line key, **dest** – specifies the name of the object that would represent the testbed file in code):

    .. code-block:: python

        if __name__ == "__main__":
            parser = argparse.ArgumentParser()
            parser.add_argument(
                "--testbed",
                dest="pyats_testbed",
                type=loader.load,
                default="pyats_testbed.yaml",
            )

            args, unknown = parser.parse_known_args()

            aetest.main(**vars(args))

#. Exit Nano without saving, pressing:
    
        .. code-block:: bash
    
            Ctrl + X

#. Let's run our first test script. This test script will try to connect to all the devices in the testbed and print the results of these attempts:

    .. code-block:: bash

        python task2step2.py --testbed pyats_testbed.yaml

#. Upon finishing the test script, pyATS generates a report of Success/Failed testcases. The **common_setup** section is also treated as the testcase with subsection **establish_connections**. Since all the devices are reachable, the testcases should be successful (PASSED). Refer to the following diagram.

    .. image:: images/step7-output.png
        :width: 75%
        :align: center


.. sectionauthor:: Luis Rueda <lurueda@cisco.com>, Jairo Leon <jaileon@cisco.com>
