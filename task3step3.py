#!/usr/bin/env python3
__author__ = "Jairo Leon, Luis Rueda"
__copyright__ = """
Copyright 2022-2025, Cisco Systems, Inc. 
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

# To handle erorrs in connections
from unicon.core import errors  # type: ignore

from pyats import aetest
from pyats.log.utils import banner
from pyats.topology import loader

# Get your logger for your script
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

golden_routes = ["192.168.0.3/32", "192.168.0.1/32"]


class MyCommonSetup(aetest.CommonSetup):
    """
    CommonSetup class to prepare for test cases
    Establishes connections to all devices in testbed.
    """

    @aetest.subsection
    def establish_connections(self, testbed):
        """
        Establishes connections to all devices in testbed.

        Args:
            testbed: The testbed containing the devices to connect to.
        """
        device_list = []
        for device in testbed.devices.values():
            LOGGER.info(banner(f"Connecting to device '{device.name}'..."))
            try:
                device.connect(log_stdout=False)
            except errors.ConnectionError:
                self.failed(f"Failed to establish a connection to '{device.name}'")
            device_list.append(device)
        # Pass list of devices to test cases
        self.parent.parameters.update(dev=device_list)


class Routing(aetest.Testcase):
    """
    Routing test case.

    Extract routing information from devices
    Verify that all device have golden_routes installed in the RIB.
    """

    @aetest.setup
    def setup(self):
        """Get list of all devices in testbed and run routes test case for each device."""
        devices = self.parent.parameters["dev"]
        aetest.loop.mark(self.routes, device=devices)

    @aetest.test
    def routes(self, device):
        """Verify that all device have golden_routes installed in the RIB."""
        if (device.os == "iosxe") or (device.os == "nxos"):
            output = device.learn("routing")
            rib = output.info["vrf"]["default"]["address_family"]["ipv4"]["routes"]
            for route in golden_routes:
                if route not in rib:
                    self.failed(f"{route} is not found")
                else:
                    pass

        elif device.os == "asa":
            output = device.parse("show route")
            rib = output["vrf"]["default"]["address_family"]["ipv4"]["routes"]

            for route in golden_routes:
                if route not in rib:
                    self.failed(f"{route} is not found")
                else:
                    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--testbed-file",
        dest="testbed",
        type=loader.load,
        default="pyats_testbed.yaml",
    )

    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))  # type: ignore
