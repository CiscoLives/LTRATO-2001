Step 5: pyATS APIs
##################

**Value Proposition:** By leveraging its APIs, you can streamline the process of interacting with network devices, executing commands, and parsing the output in a consistent and structured manner. 
The pyATS APIs offer a powerful abstraction layer that simplifies the complexity of working with different network operating systems and device types. 
With its modular design and extensive library of supported platforms, pyATS empowers network engineers and developers to write scalable and maintainable automation scripts, enabling efficient network validation, troubleshooting, and configuration management.


To use the **pyATS APIs**, you need to follow the steps below:

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
        csr_routes = csr.api.get_routes(protocol_codes="O")

    .. tip:: 
        
        The protocol_codes corresponds to what we see in the output of the `show ip route` command.
        In this case, we are looking for OSPF routes.

#. Explore csr_routes by typing ``csr_routes`` and try to find the routes for **OSPF**.

    .. code-block:: python

        ['10.0.0.4/30', '10.0.0.8/30', '192.168.0.1/32', '192.168.100.1/32']

.. note::
    
    It's much simpler to use the **APIs** to get the specific output when they are available.
    
    Compare the output to the output of the last step in Step 4.
    The output is the same, but the method to get the output is different.

    To look at the list of available APIs, refer to the appendix section of the documentation.


.. sectionauthor:: Luis Rueda <lurueda@cisco.com>, Jairo Leon <jaileon@cisco.com>

