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
import re

# To filter management networks from ping test cases
from ipaddress import IPv4Network

# To handle errors with connections to devices
import daiquiri
from unicon.core import errors  # type: ignore

from pyats import aetest
from pyats.log.utils import banner
from pyats.topology import loader

# Get your logger for your script
LOGGER = daiquiri.getLogger(__name__)
daiquiri.setup(level=logging.INFO)

# Management network IP range
mgmt_net = IPv4Network("198.18.1.0/24")


class MyCommonSetup(aetest.CommonSetup):
    """
    CommonSetup class to prepare for test cases.
    Establishes connections to all devices in testbed.
    """

    @aetest.subsection
    def establish_connections(self):
        """Establishes connections to all devices in testbed."""
        pyats_testbed = self.parent.parameters.get("pyats_testbed")
        self.parent.parameters["testbed"] = pyats_testbed
        for device in pyats_testbed.devices.values():
            LOGGER.info(banner(f"Connecting to device '{device.name}'..."))
            try:
                device.connect(log_stdout=False)
            except errors.ConnectionError:
                self.failed(f"Failed to establish a connection to '{device.name}'")


class PingTestcase(aetest.Testcase):
    """
    PingTestcase.

    Find links between NX-OS device and CSR1000v
    Extract IP addresses from both ends of each link
    Run ping command for each extracted IP address from NX-OS and CSR1000v
    """

    @aetest.setup
    def setup(self):
        """Extract IP addresses from both ends of each link between NX-OS device and CSR1000v."""
        # list to store all IPs from topology
        dest_ips = []

        nx = self.parent.parameters["testbed"].devices["nx-osv-1"]
        csr = self.parent.parameters["testbed"].devices["csr1000v-1"]

        # Find links between NX-OS device and CSR1000v
        links = nx.find_links(csr)

        for link in links:
            # process each link between devices

            for link_iface in link.interfaces:
                # process each interface (side) of the
                # link and extract IP address from it

                dest_ip = link_iface.ipv4.ip

                # Check that destination IP is not from management IP range
                if dest_ip not in mgmt_net:
                    LOGGER.info(f"{link_iface.name}:{link_iface.ipv4.ip}")
                    dest_ips.append(link_iface.ipv4.ip)
                else:
                    LOGGER.info(
                        f"Skipping link_iface {link_iface.name} "
                        f"from management subnet"
                    )

        LOGGER.info(f"Collected following IP addresses: {dest_ips}")

        # run ping test case for each collected dest_ips

        aetest.loop.mark(self.ping, dest_ip=dest_ips)

    @aetest.test
    def ping(self, dest_ip):
        """
        Run ping command for each IP address (dest_ip) from NX-OS and CSR1000v.
        Parse collected output to generate result of test.

        Sending 5, 56-bytes ICMP Echos to 10.0.0.18
        Timeout is 2 seconds, data pattern is 0xABCD

        64 bytes from 10.0.0.18: icmp_seq=0 ttl=255 time=0.594 ms
        <...>

        --- 10.0.0.18 ping statistics ---
        5 packets transmitted, 5 packets received, 0.00% packet loss
        round-trip min/avg/max = 0.565/0.67/0.837 ms
        """
        nx = self.parent.parameters["testbed"].devices["nx-osv-1"]

        try:
            result = nx.ping(dest_ip)
        except Exception as e:
            self.failed(f"Ping from {nx.name}->{dest_ip} failed: {e}")
        else:
            m = re.search(r"(?P<rate>\d+)\.\d+% packet loss", result)
            loss_rate = m.group("rate")

            if int(loss_rate) < 20:
                self.passed(f"Ping loss rate {loss_rate}%")
            else:
                self.failed(f"Ping loss rate {loss_rate}%")


if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--testbed",
        dest="pyats_testbed",
        type=loader.load,
        default="pyats_testbed.yaml",
    )

    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))
