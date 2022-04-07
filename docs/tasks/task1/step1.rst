Step 1: Explore Lab Structure
#############################

**Value Proposition:** Understand the tools used in the lab and the lab's structure.

#. On the remote desktop, double-click the ``Ubuntu`` shortcut on the desktop.
#. Ubuntu will run on our RDP Jumphost on top of Windows 10. The bash Linux shell appears.

    .. image:: images/ubuntu-terminal.png
        :width: 75%
        :align: center

    |

    Throughout the lab, you will be working from a virtual environment. The virtual environment provides the following major advantages over running Python scripts globally:

        - **Project Isolation:** Avoids installing Python packages globally which could break system tools or other projects.
        - **Dependency Management:** Makes the project self-contained and reproducible by capturing all package dependencies in a requirements file.

    Cisco recommends that you run pyATS scripts from the virtual environment. The keyword (pyats) at the beginning of each line indicates that you are working from a virtual environment.

#. Change to the directory that contains the lab files:

    .. code-block:: bash

        cd ~/labpyats

#. Check the lab’s structure (before running the command shown below, ensure that you have changed to the correct directory: **~/labpyats**).

    .. code-block:: bash

        ls -l

    Check the list of files and refer to the description of each file depicted in the table below.

    .. note ::
        The following files are in the labpyats directory and will be used throughout the lab.

    .. csv-table::
        :file: ./reference/pyats-files.csv
        :width: 80%
        :header-rows: 1

.. sectionauthor:: Luis Rueda <lurueda@cisco.com>, Jairo Leon <jaileon@cisco.com>
