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


# To get a logger for the script
import argparse
import logging

# To handle errors with connections to devices
from unicon.core import errors  # type: ignore

from pyats import aetest
from pyats.log.utils import banner
from pyats.topology import loader

# Get your logger for your script
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


class MyCommonSetup(aetest.CommonSetup):
    """
    CommonSetup class to prepare for test cases.
    Establishes connections to all devices in testbed.
    """

    @aetest.subsection
    def establish_connections(self, pyats_testbed):
        """Establishes connections to all devices in testbed."""
        device_list = []
        # Load all devices from testbed file and try to connect to them
        for device in pyats_testbed.devices.values():
            LOGGER.info(banner(f"Connecting to device '{device.name}'..."))
            try:
                device.connect(log_stdout=False)
            except errors.ConnectionError:
                self.failed(f"Failed to establish a connection to '{device.name}'")
            device_list.append(device)
        # Pass list of devices to test cases
        self.parent.parameters.update(dev=device_list)


class VerifyLogging(aetest.Testcase):
    """
    VerifyLogging Testcase.

    Collect show logging information from devices.
    Verify that all devices do not have 'ERROR|WARN' messages in logs
    """

    @aetest.setup
    def setup(self):
        """Testcase Setup section."""
        pass

    @aetest.test
    def error_logs(self):
        """Testcase section to check for ERROR|WARN messages in logs."""
        any_device = self.parent.parameters["dev"][0]
        any_device.log_user(enable=True)
        output = any_device.execute("show logging | include ERROR|WARN")

        if len(output) > 0:
            self.failed(
                "Found messages in log that are either ERROR or WARN, review logs first"
            )
        else:
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--testbed",
        dest="pyats_testbed",
        type=loader.load,
        default="pyats_testbed.yaml",
    )

    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))
