Appendix: A
###########

Links
=====

- `GitHub repository <https://github.com/CiscoLives/LTRATO-2001>`_
- `pyATS Page <https://developer.cisco.com/pyats/>`_
- `Models supported by pyATS genie learn method <https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/models>`_
- `Platforms supported by pyATS genie unicon <https://pubhub.devnetcloud.com/media/unicon/docs/user_guide/supported_platforms.html>`_
- `Available parsers that are supported by pyATS genie <https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/parsers>`_
- `pyATS Useful Libraries <https://pubhub.devnetcloud.com/media/genie-docs/docs/userguide/utils/index.html>`_


Examples
========

Configuration Compliance
------------------------

Steps:

#. Install jsonschema python library

    .. code-block:: bash

        pip install jsonschema


#. Connect to pyATS shell

    .. code-block:: bash

        pyats shell --testbed-file pyats_testbed.yaml 


#. Import jsonschema python library

    .. code-block:: python

        from jsonschema import validate 


#. Define a schema for the configuration compliance test.

    .. code-block:: python

        schema = {
            "type": "object",
            "properties": {"description": {"type": "string"}},
            "required": ["description"],
        }

#. Define, connect, and parse the **show interfaces** command.

    .. code-block:: python

        csr = testbed.devices['csr1000v-1']
        csr.connect()
        csr_interfaces = csr.parse("show interfaces")

#. Validate the parsed output against the schema.

    .. code-block:: python

        validate(instance=csr_interfaces["Loopback1"], schema=schema)

#. If the validation fails, an execption will be raised.

    .. code-block:: bash

        ---------------------------------------------------------------------------
        ValidationError                           Traceback (most recent call last)
        Input In [10], in <cell line: 1>()
        ----> 1 validate(instance=csr_interfaces["Loopback1"], schema=schema)

        File ~/code/github.com/jaileon/LTRATO-2001/.venv/lib/python3.9/site-packages/jsonschema/validators.py:1058, in validate(instance, schema, cls, *args, **kwargs)
        1056 error = exceptions.best_match(validator.iter_errors(instance))
        1057 if error is not None:
        -> 1058     raise error

        ValidationError: 'description' is a required property

        Failed validating 'required' in schema:
            {'properties': {'description': {'type': 'string'}},
            'required': ['description'],
            'type': 'object'}

        On instance:
            {'bandwidth': 8000000,
            'counters': {'in_abort': 0,
                        'in_broadcast_pkts': 0,
                        'in_crc_errors': 0,
                        'in_errors': 0,
                        'in_frame': 0,
                        'in_giants': 0,
                        'in_ignored': 0,
                        'in_multicast_pkts': 0,
                        'in_no_buffer': 0,
                        'in_octets': 0,
                        'in_overrun': 0,
                        'in_pkts': 0,
                        'in_runts': 0,
                        'in_throttles': 0,
                        'last_clear': 'never',
                        'out_buffer_failure': 0,
                        'out_buffers_swapped': 0,
                        'out_collision': 0,
                        'out_errors': 0,
                        'out_interface_resets': 0,
                        'out_octets': 0,
                        'out_pkts': 0,
                        'out_underruns': 0,
                        'out_unknown_protocl_drops': 0,
                        'rate': {'in_rate': 0,
                                'in_rate_pkts': 0,
                                'load_interval': 300,
                                'out_rate': 0,
                                'out_rate_pkts': 0}},
            'delay': 5000,
            'enabled': True,
            'encapsulations': {'encapsulation': 'loopback'},
            'ipv4': {'10.10.10.10/32': {'ip': '10.10.10.10',
                                        'prefix_length': '32'}},
            'keepalive': 10,
            'last_input': 'never',
            'last_output': 'never',
            'line_protocol': 'up',
            'mtu': 1514,
            'oper_status': 'up',
            'output_hang': 'never',
            'port_channel': {'port_channel_member': False},
            'queues': {'input_queue_drops': 0,
                        'input_queue_flushes': 0,
                        'input_queue_max': 75,
                        'input_queue_size': 0,
                        'output_queue_max': 0,
                        'output_queue_size': 0,
                        'queue_strategy': 'fifo',
                        'total_output_drop': 0},
            'reliability': '255/255',
            'rxload': '1/255',
            'txload': '1/255',
            'type': 'Loopback'}


#. If the validation succeeds, no exceptions will be raised.

.. sectionauthor:: Luis Rueda <lurueda@cisco.com>, Jairo Leon <jaileon@cisco.com>
