Step 4: Run PING to Verify Reachability
#######################################

**Value Proposition:** In this testcase we must test reachability between devices (**nx-osv-1** and **csr1000v-1**), using the ping command.

High-level logic of the test will be as follows:

- Connect to each device in the testbed.
- Find links between nx-osv-1 and csr1000v-1.
- Collect IP addresses from both ends of these links.
- Run the ping commands from nx-osv-1 for IP addresses, discovered in the previous step.

#. Let's connect to pyATS shell and check our idea:

    .. code-block:: bash

        pyats shell --testbed-file pyats_testbed.yaml

#. Input the following code into pyATS shell:

    .. code-block:: python

        csr = testbed.devices['csr1000v-1']
        nx = testbed.devices['nx-osv-1']

#. pyATS has a **find_links(device_name)** method to find all the links between two devices in the topology. Let’s find the links between **csr1000v-1** and **nx-osv-1**.

    .. code-block:: python

        nx.find_links(csr)

#. Observe the output:

    .. code-block:: bash

        {<Link object 'csr1000v-1-to-nx-osv-1' at 0x7f445194b050>,
        <Link object 'csr1000v-1-to-nx-osv-1#1' at 0x7f445194b150>,
        <Link object 'flat' at 0x7f445194b410>}

#. Exit the pyATS shell using the exit command.

    Before studying the code and running the next script, let's dive into the details on how information about a topology is stored in a testbed object (see the illustration that follows for a graphical representation of the explanation).

    Things to know about the structure of the testbed object (created from the testbed YAML file specified: testbed.yaml):

    - The pyATS **Testbed** object contains the Python dictionary **devices**.
    - Elements of the **devices** dictionary are the **Device** objects.
    - Each object in the **devices** dictionary stores dictionary **interfaces** (contains **interface** objects).
    - Each **interface** object stores the link object.

    |

    .. image:: images/testbed_object_structure.png
        :width: 75%
        :align: center
    
    |

    - The **Testbed** object is the top container object, containing all the testbed devices and all the subsequent information that is generic to the    testbed.
    - **Device** objects represent physical and/or virtual hardware in a testbed topology.
    - **Interface** objects represent a physical/virtual interface that connects to a link of some sort (for example, Ethernet, ATM, Loopback, and so on).
    - **Link** objects represent the connection (wire) between two or more interfaces within a testbed topology.

    |

    .. image:: images/links-representation.png
        :width: 75%
        :align: center
    
    |

    Let's check the structure depicted above using our topology. We will find all the links connected between **nx-osv-1** and **csr1000v-1**.

    .. note::
        We can get the value of an attribute for each object. For example, we can get a link to which an interface object belongs by calling a **link** attribute. We can also reference interfaces which belong to this link, by calling the **interfaces** attribute in step 6 (see code below).

    .. code-block:: bash

        pyats shell --testbed-file pyats_testbed.yaml

#. Paste the following snippet to pyATS console:

    - Place the following iPython command in the beginning of code:

        .. code-block:: bash

            %cpaste

    - Copy and paste the code into the pyATS console:

        .. code-block:: python
            :emphasize-lines: 7

            csr = testbed.devices['csr1000v-1']
            nx = testbed.devices['nx-osv-1']
            links = nx.find_links(csr)
            
            for link in links:
            print(f'#{link}')
            for link_iface in link.interfaces:
                print(f'##{link_iface}')
                print(f'###link_iface.ipv4 = {link_iface.ipv4}, {type(link_iface.ipv4)}')
                print(f'###link_iface.ipv4.ip = {link_iface.ipv4.ip}, {type(link_iface.ipv4.ip)}')

    - End the code with ``--``.

    Refer to the command output:

    - **#Link csr1000v-1-to-nx-osv-1:** represents interfaces of all devices connected to the first link between csr1000v-1 and nx-osv-1.
    - **#Link flat:** represents interfaces of all devices (asav-1, csr1000v-1, nx-osv-1) connected to a management network.
    - **#Link csr1000v-1-to-nx-osv-1#1:** represents interfaces of all devices connected to the second link between csr1000v-1 and nx-osv-1.

    |
    
    .. image:: images/links-output.png
        :width: 75%
        :align: center

#. Open the file task9_labpyats.py in Nano editor:

    .. code-block:: bash

        nano task9_labpyats.py








.. sectionauthor:: Luis Rueda <lurueda@cisco.com>, Jairo Leon <jaileon@cisco.com>
