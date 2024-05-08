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
import daiquiri
from unicon.core import errors

from pyats.topology.loader import load

LOGGER = daiquiri.getLogger(__name__)
daiquiri.setup(level=logging.INFO)


def write_commands_to_file(abs_filename, command_output):
    try:
        with open(abs_filename, "a+") as file_output:
            file_output.write(command_output)

    except IOError as e:
        log.error(
            f"Unable to write output to file: {abs_filename}." f"Due to error: {e}"
        )
        exit(1)


def collect_device_commands(testbed, command_to_gather, filename):
    abs_filename = path.join(path.dirname(__file__), filename)
    log.info(f"filename: {abs_filename}")

    log.info("Starting command collection...")

    for device_name, device in testbed.devices.items():
        try:
            device.connect(log_stdout=False)
        except errors.ConnectionError:
            log.error(
                f"Failed to establish a connection to: {device.name}."
                f"Check connectivity and try again."
            )
            continue

        else:
            log.info(f"Connected ok: {device_name}")
            command_output = device.execute(command_to_gather, log_stdout=True)
            write_commands_to_file(abs_filename, command_output + "\n####\n")


def main():
    global log
    format = "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=format)

    log = logging.getLogger(__name__)

    testbed_filename = "pyats_testbed.yaml"
    testbed = load(testbed_filename)

    output_filename = "task2step1.txt"
    open(output_filename, "w").close()

    collect_device_commands(testbed, "show inventory", output_filename)


if __name__ == "__main__":
    main()
