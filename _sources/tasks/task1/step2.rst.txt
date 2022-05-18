Step 2: Verify pyATS Testbed File
#################################

**Value Proposition:** Explore pyATS testbed file used in the lab.

For pyATS to be able to work with network topology, it must know the following basic information: management interfaces, IP addresses, connection protocol and connections between network devices.

This information is stored in the pyATS testbed file (in YAML format).

Can this information be gathered automatically, and can pyATS testbed file be prepared for us?

Sure. Since the lab is running in Cisco Modeling Labs (CML) `cmlutils <https://github.com/CiscoDevNet/virlutils>`__ , tool can be used to prepare pyATS testbed file from CML topology.

.. note ::
    Testbed file was already prepared and you do not need to call cmlutils now. However, if you are curious about how can you prepare pyATS testbed file from CML topology, then the needed commands are:

    .. code-block:: bash

        source /var/lib/virlutils/venv/bin/activate

        cml ls (get id from ID column)
        cml use --id XXX

        cml generate pyats

        source ~/pyats/bin/activate

The testbed YAML file for pyATS has been pre-created for this lab, and it is named pyats_testbed.yaml.

#. Change to the directory that contains the lab files:

    .. code-block:: bash

        cd ~/labpyats


#. Open the pre-created ``pyats_testbed.yaml`` file in the Nano editor by entering the following command:

    .. code-block:: bash

        nano pyats_testbed.yaml

#. 3.	The output of the command should contain the following:

    .. literalinclude:: ./reference/pyats_testbed.yaml
        :language: yaml
    
    Now we have all the required information to start our tests with pyATS.

    .. note ::
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

        We recommend you store credentials separately, at least as environmental variables.


#. Exit Nano without saving, pressing:

    .. code-block:: bash

        Ctrl + X

#. In the lab environment, variables for PYATS with credentials to access all devices are preconfigured. Check these environment variables from a Bash shell:

    .. code-block:: bash
    
        echo $PYATS_USERNAME $PYATS_PASSWORD $PYATS_AUTH_PASS

#. The output of the command should contain the following:

    .. code-block:: bash

        cisco cisco cisco


.. sectionauthor:: Luis Rueda <lurueda@cisco.com>, Jairo Leon <jaileon@cisco.com>
