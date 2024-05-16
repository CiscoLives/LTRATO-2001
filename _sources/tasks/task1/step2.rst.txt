Step 2: Verify pyATS Testbed File
#################################

**Value Proposition:** Ensure accurate network infrastructure mapping for seamless test automation and proactive issue mitigation.

For pyATS to work with network topology, it must know the following basic information: management interfaces, IP addresses, connection protocol, and connections between network devices.

This information is stored in the pyATS testbed file (`YAML format <https://pubhub.devnetcloud.com/media/pyats/docs/topology/schema.html>`_).

The testbed YAML file for pyATS has been pre-created for this lab, and it is named ``pyats_testbed.yaml``.

#. Change to the directory that contains the lab files:

    .. code-block:: bash

        cd ~/LTRATO-2001


#. Open the pre-created ``pyats_testbed.yaml`` file in the Nano editor by entering the following command:

    .. code-block:: bash

        nano pyats_testbed.yaml

#. The output of the command should contain the following:

    .. literalinclude:: ./reference/pyats_testbed.yaml
        :language: yaml
    
    Now we have all the required information to start our tests with pyATS.

    .. note::
        Note that username and passwords to access devices are not stored in the YAML file:

        .. code-block:: bash

            credentials:
            default:
            username: "%ENV{PYATS_USERNAME}"
            password: "%ENV{PYATS_PASSWORD}"
            enable:
            password: "%ENV{PYATS_AUTH_PASS}"
            line:
            password: "%ENV{PYATS_AUTH_PASS}"

        We recommend you store credentials separately as environment variables.


#. Exit Nano without saving by pressing :guilabel:`Ctrl + X`

#. In the lab environment, variables for PYATS with credentials to access all devices are preconfigured. Check these environment variables from a Bash shell:

    .. code-block:: bash
    
        echo $PYATS_USERNAME
        echo $PYATS_PASSWORD
        echo $PYATS_AUTH_PASS

#. The output of the command should contain the following:

    .. code-block:: bash

        cisco
        cisco
        cisco


.. sectionauthor:: Luis Rueda <lurueda@cisco.com>, Jairo Leon <jaileon@cisco.com>
