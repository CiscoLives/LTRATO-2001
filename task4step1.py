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

import os

import daiquiri
from ats.easypy import run

from pyats.topology.loader import load

LOGGER = daiquiri.getLogger(__name__)
daiquiri.setup(level=logging.INFO)


def main():
    # Find the location of the script in relation to the job file
    ping_tests = os.path.join("task3step4.py")
    testbed = load("pyats_testbed.yaml")

    # Execute the testscript
    run(testscript=ping_tests, pyats_testbed=testbed)
