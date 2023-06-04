#!/usr/bin/env python3

# To get a logger for the script
import logging

from pyats import aetest
from pyats.log.utils import banner

# To handle errors with connections to devices
from unicon.core import errors

import argparse
from pyats.topology import loader

# Get your logger for your script
LOGGER = logging.getLogger(__name__)
LOGGER.level = logging.INFO

# SNs that has to be changed to the actual:
contract_sn = ["9AQHSSAS8AU", "9Q3YV06WJ71", "9IFUH4GPSGL"]


class MyCommonSetup(aetest.CommonSetup):
    """
    CommonSetup class to prepare for test cases
    Establishes connections to all devices in testbed
    """

    @aetest.subsection
    def establish_connections(self, pyats_testbed):
        """
        Establishes connections to all devices in testbed
        :param testbed:
        :return:
        """

        device_list = []
        for device in pyats_testbed.devices.values():
            LOGGER.info(banner(f"Connecting to device '{device.name}'..."))
            try:
                device.connect(log_stdout=False)
            except errors.ConnectionError:
                self.failed(
                    f"Failed to establish a connection to '{device.name}'")
            device_list.append(device)
        # Pass list of devices to test cases
        self.parent.parameters.update(dev=device_list)


class Inventory(aetest.Testcase):
    """
    Inventory test case - extract Serial numbers information from devices
    Verify that all SNs are covered by service contract (exist in contract_sn)
    """

    @aetest.setup
    def setup(self):
        """
        Get list of all devices in testbed and
        run inventory test case for each device
        :return:
        """

        devices = self.parent.parameters["dev"]
        aetest.loop.mark(self.inventory, device=devices)

    @aetest.test
    def inventory(self, device):
        """
        Verify that all SNs are covered by
        service contract (exist in contract_sn)
        :return:
        """

        if device.os == "iosxe":

            csr_output = device.parse('show inventory')
            chassis_sn = csr_output["main"]["chassis"]["CSR1000V"]["sn"]

            if chassis_sn not in contract_sn:
                self.failed(f"{chassis_sn} is not covered by contract")
            else:
                pass

        elif device.os == "nxos":

            nx_output = device.parse('show inventory')
            chassis_sn = nx_output["name"]["Chassis"]["serial_number"]

            if chassis_sn not in contract_sn:
                self.failed(f"{chassis_sn} is not covered by contract")
            else:
                pass

        elif device.os == "asa":

            asa_output = device.parse('show inventory')
            chassis_sn = asa_output["Chassis"]["sn"]

            if chassis_sn not in contract_sn:
                self.failed(f"{chassis_sn} is not covered by contract")
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
