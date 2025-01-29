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
