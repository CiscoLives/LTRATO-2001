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


import logging
from os import path

# To handle errors with connections to devices
from unicon.core import errors  # type: ignore

from pyats.topology.loader import load

format = "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=format)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(level=logging.INFO)


def write_commands_to_file(abs_filename, command_output):
    """Write commands to file."""
    try:
        with open(abs_filename, "a+") as file_output:
            file_output.write(command_output)

    except IOError as e:
        LOGGER.error(
            f"Unable to write output to file: {abs_filename}." f"Due to error: {e}"
        )
        exit(1)


def collect_device_commands(testbed, command_to_gather, filename):
    """Collect device commands."""
    abs_filename = path.join(path.dirname(__file__), filename)
    LOGGER.info(f"filename: {abs_filename}")

    LOGGER.info("Starting command collection...")

    for device_name, device in testbed.devices.items():
        try:
            device.connect(log_stdout=False)
        except errors.ConnectionError:
            LOGGER.error(
                f"Failed to establish a connection to: {device.name}."
                f"Check connectivity and try again."
            )
            continue

        else:
            LOGGER.info(f"Connected ok: {device_name}")
            command_output = device.execute(command_to_gather, log_stdout=True)
            write_commands_to_file(abs_filename, command_output + "\n####\n")


def main():
    """Main function."""
    testbed_filename = "pyats_testbed.yaml"
    testbed = load(testbed_filename)

    output_filename = "task2step1.txt"
    open(output_filename, "w").close()

    collect_device_commands(testbed, "show inventory", output_filename)


if __name__ == "__main__":
    main()
