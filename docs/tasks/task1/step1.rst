Step 1: Explore Lab Structure
#############################

**Value Proposition:** Develop a comprehensive understanding of the lab's virtual environment architecture, facilitating seamless integration and utilization of Python and pyATS tools, enabling streamlined automation, efficient dependency management, and project isolation for enhanced productivity and consistency across scripting workflows.

#. On the remote desktop, click the ``Terminal`` shortcut on the toolbar, once the terminal opens, on the dropdown icon, select ``ubuntu``.
#. Ubuntu will run on our RDP Jumphost on top of Windows 10. In addition, the bash Linux shell will appear.

    .. note::
        It can take a few seconds while the packages required for the lab are installed.

    .. image:: images/ubuntu-terminal.png
        :width: 75%
        :align: center

    |

    Throughout the lab, you will be working from a virtual environment. 
    The virtual environment provides the following significant advantages over running Python scripts globally:

        - **Project Isolation:** Avoids installing Python packages globally, which could break system tools or other projects.
        - **Dependency Management:** Makes the project self-contained and reproducible by capturing all package dependencies in a requirements file.

    Cisco recommends you run pyATS scripts from the virtual environment.
    Therefore, the keyword (pyats) at the beginning of each line indicates that you are working from a virtual environment.

#. Make sure that you are within the ``/home/cisco/LTRATO-2001`` directory, which contains the necessary lab files, otherwise you can switch to the appropriate directory by executing the following command:

    .. code-block:: bash

        cd ~/LTRATO-2001

#. Check the directory structure.

    .. code-block:: bash

        ls -l

    Check the list of files and refer to the description of each file depicted in the table below.

    .. note ::
        The following files are in the LTRATO-2001 directory and will be used throughout the lab.

    .. csv-table::
        :file: ./reference/pyats-files.csv
        :width: 80%
        :header-rows: 1

.. sectionauthor:: Luis Rueda <lurueda@cisco.com>, Jairo Leon <jaileon@cisco.com>
