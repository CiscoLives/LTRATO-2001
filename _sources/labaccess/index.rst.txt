##########
Lab Access
##########

This lab includes a CML server on which simulation of the lab network will be running. 
All lab tasks will be done from the Jumphost (a Windows 10 machine with WSL installed).

The lab topology is shown as below:

.. image:: images/lab-diagram-01.svg
    :width: 50%
    :align: center

|

IP Addressing and Access Information
====================================

.. csv-table::
   :file: ./reference/devices-info.csv
   :width: 80%
   :header-rows: 1

Component Details
=================

.. csv-table::
   :file: ./reference/componet-details.csv
   :width: 80%
   :header-rows: 1


Get Started
===========

#. Go to `dCloud <https://dcloud.cisco.com>`__ and login with your Cisco (CCO) credentials.
#. Paste Event URL into your browser and click Enter, you will be forwarded into your session page.
#. On the session page click :guilabel:`Info` tab (1) and scroll down (2) for Anyconnect Credentials (3). You will need these credentials to get access to your lab, using Cisco AnyConnect client. 

    .. image:: images/session-details.png
        :width: 75%
        :align: center

#. Cisco AnyConnect client and Host address from previous step.

    .. image:: images/anyconnect-01.png
        :width: 45%
        :align: center

#. When login banner will appear, enter Username/Password from previous step.

    .. image:: images/anyconnect-02.png
        :width: 45%
        :align: center

#. For best performance, connect to the workstation with Cisco AnyConnect VPN `Show Me How <https://dcloud-cms.cisco.com/help/install_anyconnect_pc_mac>`__ and the local RDP client on your laptop `Show Me How <https://dcloud-cms.cisco.com/help/local_rdp_mac_windows>`__ and use the information from the table above to connect to workstation
#. Once inside the remote desktop connection, open Google Chrome browser, startup page https://cml-controller.cml.lab/login would be opened (web interface of Cisco Modeling Labs server).

#. Press ``Login`` button:

    .. image:: images/cml-01.png
        :width: 75%
        :align: center

#. On the opened page ensure the lab LTRATO-2001 is in ``ON`` state:

    .. image:: images/cml-02.png
        :width: 75%
        :align: center

#. Click on the topology and on the opened page ensure status for all devices are ``green``:

    .. image:: images/cml-03.png
        :width: 75%
        :align: center
    
    |

    .. note::
        If the status of any device is not green 10 minutes after CML topology has been started, refer to the lab's proctor for assistance.

#. On the remote desktop, double-click the ``PuTTY`` shortcut icon on the desktop and verify connectivity by launching the **asav-1**, **csr100v-1**, and **nx-osv-1** devices from the remote desktop and logging in. Username/password for all three devices: ``cisco/cisco``.

#. If all devices are reachable and you can log in, close the PuTTY sessions and proceed with **Task 1**.


.. sectionauthor:: Luis Rueda <lurueda@cisco.com>, Jairo Leon <jaileon@cisco.com>
