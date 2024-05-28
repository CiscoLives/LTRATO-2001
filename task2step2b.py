#!/usr/bin/env python3
__author__ = "Jairo Leon, Luis Rueda"
__copyright__ = """
Copyright 2022-2024, Cisco Systems, Inc. 
All Rights Reserved. 

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR 
OTHER DEALINGS IN THE SOFTWARE. 
"""


import argparse
import logging

from genie.testbed import load
from unicon.core.errors import ConnectionError, StateMachineError, TimeoutError

from pyats import aetest, topology

# Get your logger for your script
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


class CommonSetup(aetest.CommonSetup):
    """Common Setup Section."""

    @aetest.subsection
    def load_testbed(self, testbed):
        """Load testbed file and assign it to testbed."""
        LOGGER.info(
            "Converting pyATS testbed to Genie Testbed to support pyATS Library features"
        )
        testbed = load(testbed)
        self.parent.parameters.update(testbed=testbed)

    @aetest.subsection
    def connect(self, testbed):
        """Establishes connection to all your testbed devices."""
        # make sure testbed is provided
        assert testbed, "Testbed is not provided!"

        # connect to all testbed devices
        #   By default ANY error in the CommonSetup will fail the entire test run
        #   Here we catch common exceptions if a device is unavailable to allow test to continue
        try:
            testbed.connect(log_stdout=False)
        except (TimeoutError, StateMachineError, ConnectionError):
            LOGGER.error("Unable to connect to all devices")


class interface_errors(aetest.Testcase):
    """interface_errors."""

    # List of counters keys to check for errors
    #   Model details: https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/_models/interface.pdf
    counter_error_keys = ("in_crc_errors", "in_errors", "out_errors")

    @aetest.setup
    def setup(self, testbed):
        """Learn and save the interface details from the testbed devices."""
        self.learnt_interfaces = {}
        for device_name, device in testbed.devices.items():
            # Only attempt to learn details on supported network operation systems
            if device.os in ("ios", "iosxe", "iosxr", "nxos"):
                LOGGER.info(f"{device_name} connected status: {device.connected}")
                LOGGER.info(f"Learning Interfaces for {device_name}")
                self.learnt_interfaces[device_name] = device.learn("interface").info

    @aetest.test
    def test(self, steps):
        """Test section."""
        # Loop over every device with learnt interfaces
        for device_name, interfaces in self.learnt_interfaces.items():
            with steps.start(
                f"Looking for Interface Errors on {device_name}", continue_=True
            ) as device_step:
                # Loop over every interface that was learnt
                for interface_name, interface in interfaces.items():
                    with device_step.start(
                        f"Checking Interface {interface_name}", continue_=True
                    ) as interface_step:
                        # Verify that this interface has "counters" (Loopbacks Lack Counters on some platforms)
                        if "counters" in interface.keys():
                            # Loop over every counter to check, looking for values greater than 0
                            for counter in self.counter_error_keys:
                                # Verify that the counter is available for this device
                                if counter in interface["counters"].keys():
                                    if interface["counters"][counter] > 0:
                                        interface_step.failed(
                                            f'Device {device_name} Interface {interface_name} has a count of {interface["counters"][counter]} for {counter}'
                                        )
                                else:
                                    # if the counter not supported, log that it wasn't checked
                                    LOGGER.info(
                                        f"Device {device_name} Interface {interface_name} missing {counter}"
                                    )
                        else:
                            # If the interface has no counters, mark as skipped
                            interface_step.skipped(
                                f"Device {device_name} Interface {interface_name} missing counters"
                            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="standalone parser")
    parser.add_argument(
        "--testbed",
        dest="testbed",
        help="testbed YAML file",
        type=topology.loader.load,
        default="pyats_testbed.yaml",
    )

    # do the parsing
    args = parser.parse_known_args()[0]

    aetest.main(testbed=args.testbed)
