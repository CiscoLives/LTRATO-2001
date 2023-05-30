*** Test Cases ***

1. CONNECT TO DEVICE UNDER TEST (SSH)
    connect to device "nx-osv-1"

2. VALIDATE VERSION ON THE DUTS AND INITIALIZING LOGGING
    run "show version"
    run "show inventory"

3. COLLECT RUNNING CONFIGURATION FROM ALL DUTS
    initialize logging to "show_version_and_running_configuration.txt"   # initialize logging
    activate report "show_version_and_running_configuration.txt"
    run "show ip route"
    run "show ip route summary"
    disable report logging   #Disabling the show_version_and_running_configuration.txt logging report

4. VERIFY IPV4 ROUTE BEFORE CLEAR COMMAND ON DUT1
    run parsed json "sh ip route summary"
    ${ROUTE_COUNT_BEFORE}=  get parsed "routes"      #IPV4 route count before clear ipv4 routes
    Set Global Variable  ${ROUTE_COUNT_BEFORE}

5. CLEAR IPV4 ROUTES ON DUT1
    run "clear ip route *"
    ${status}=  Run Keyword And Return Status  output contains "Clearing ALL routes"
    Run Keyword If  '${status}' == 'False'  Fatal Error  ++UNSUCCESSFUL++ ${DUT1} IPv4 routes not successfully cleared
    ...  ELSE  set test message  ++SUCCESSFUL++ IPV4 routes cleared successfully \n  append=True

6. VALIDATE IPV4 ROUTES AFTER CLEAR COMMAND ON DUT1
    sleep  30  #For learning routes
    run parsed json "sh ip route summary"
    ${ROUTE_COUNT_AFTER}=  get parsed "routes"      #IPV4 route count after clear ipv4 routes
    Run Keyword If  '${ROUTE_COUNT_AFTER}' != '${ROUTE_COUNT_BEFORE}'  FAIL  ++UNSUCCESSFUL++ ${DUT1} - Either few or all IPv4 routes are not learnt after 'clear ipv4 route' command
    ...  ELSE  set test message  ++SUCCESSFUL++ All IPV4 routes are learnt successfully after 'clear ipv4 route' command\n  append=True
