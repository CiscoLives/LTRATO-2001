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

*** Settings ***
Library             ats.robot.pyATSRobot
Library             genie.libs.robot.GenieRobot
Library             genie.libs.robot.GenieRobotApis

# Load topology/testbed yaml file
Suite Setup         Run Keywords
...                     use testbed "%{TESTBED}"    AND
...                     connect to all devices
# Disconnect sessions from all devices
Suite Teardown      Run Keywords
...                     disconnect from all devices


*** Test Cases ***
Connect to All Devices and Setup Testbed
    run testcase "ltrato_2001.task4step1.MyCommonSetup"

Verify Logs For All Devices
    run testcase "ltrato_2001.task4step1.VerifyLogging"
