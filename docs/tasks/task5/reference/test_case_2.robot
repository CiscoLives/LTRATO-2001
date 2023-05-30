*** Test Cases ***

1. CONNECT TO DEVICE UNDER TEST (SSH)
    connect to device "nx-osv-1"

2. VALIDATE VERSION ON THE DUTS AND INITIALIZING LOGGING
    run "show version"

3. COLLECT RUNNING CONFIGURATION FROM ALL DUTS
    initialize logging to "show_version_and_running_configuration.txt"   # initialize logging
    activate report "show_version_and_running_configuration.txt"
    run "show ip route"
    run "show ip route summary"
    disable report logging   #Disabling the show_version_and_running_configuration.txt logging report

4. VERIFY IPV4 IPADDRESS OF LOOPBACK1
    run parsed json "sh interface lo0"
    ${LO0_IP}=  get parsed "eth_ip_addr"      #IPV4 loopback1 ip address
    Set Global Variable  ${LO0_IP}

5. VALIDATE DESTINATION IPV4 ADDRESS REACHABILITY AND VERIFY THE PING COUNT ON DUT1
    run "ping ${LO0_IP} count 10"
    run "ping ${LO0_IP} count 20"
    ${status}=  Run Keyword And Return Status  output contains "20 packets received"
    Run Keyword If  '${status}' == 'False'  FAIL   ++UNSUCCESSFUL++ ${LO0_IP} address not reachable or packets loss
    ...  ELSE  set test message  ++SUCCESSFUL++ ${LO0_IP} is reachable and no packets loss\n  append=True
