Step 1: Explore Lab Structure
#############################

**Value Proposition:** Understand the lab structure and the tools used in it.

#. On the remote desktop, double-click the ``Ubuntu`` shortcut.
#. Ubuntu will run on our RDP Jumphost on top of Windows 10. In addition, the bash Linux shell will appear.

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

#. Change to the directory that contains the lab files:

    .. code-block:: bash

        cd ~/LTRATO-2001

#. Check the lab structure (before running the command shown below, ensure that you have changed to the correct directory: **~/LTRATO-2001**).

    .. code-block:: bash

        ls -l

    Check the list of files and refer to the description of each file depicted in the table below.

    .. TODO::

        - Update at the end of the review for the lab

    .. note ::
        The following files are in the LTRATO-2001 directory and will be used throughout the lab.

    .. csv-table::
        :file: ./reference/pyats-files.csv
        :width: 80%
        :header-rows: 1

.. sectionauthor:: Luis Rueda <lurueda@cisco.com>, Jairo Leon <jaileon@cisco.com>
