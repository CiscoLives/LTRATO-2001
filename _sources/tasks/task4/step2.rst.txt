Step 2: Run tests and compare results from XPRESSO dashboard
############################################################

**Value Proposition:** In the last task, we will learn how to use XPRESSO dashboard to run the test job and compare the test results. To simplify the scenario, the basic configuration was already done in XPRESSO. Test Harness, Execution Engine, Testbed, and Job are pre-configured.

.. note::
    Due to security restrictions in dCloud on Jumphost, access to XPRESSO dashboard is provided via RDP session to CentOS VM running XPRESSO.

#. Locate XPRESSO.rdp shortcut on the desktop of Workstation, and double-click to start Remote Desktop Protocol (RDP) session to XPRESSO VM. Login with the following credentials.

    - Username: ``xpresso``
    - Password: ``C1sco12345``

    |

    .. note::
        If you are using AnyConnect VPN and have Microsoft RDP client installed, you can connect directly from your PC via RDP to address XPRESSO VM (use IP address: 198.18.134.50).

    .. image:: images/login-to-xpresso_rdp.png
        :align: center
        :width: 20%

#. Inside RDP session, open Firefox from the desktop or Application menu on top of the screen. You should be automatically logged into XPRESSO dashboard and see Requests page:

    .. image:: images/xpresso-dashboard-page.png
        :align: center
        :width: 75%

    If XPRESSO page is not opened automatically, open it directly on `dCloud <http://xpresso.dcloud-cisco.com>`_ manually and login with credentials:

        - Username: ``xpresso``
        - Password: ``C1sco12345``

#. From the menu icons on the left, locate Jobs item and click on it:

    .. image:: images/xpresso-jobs-filter.png
        :align: left
        :width: 15%

    |
    |
    |

    You will see the pre-configured job **Ping_from_ASA** which executes **task10_runtestsjob.py** script you've used in this Scenario:


    .. image:: images/xpresso-jobs-list.png
        :align: center
        :width: 75%

#. Hover the mouse over the job row and you will see **Execute** icon on the right. Click it:

    .. image:: images/xpresso-jobs-execute.png
        :align: left
        :width: 15%

    |
    |
    |
    |

    You will be presented with a ``You are configuring a new group job request`` page where you can customize job run settings. Leave all settings by default and click Submit button. Once done, job will be submitted for execution.

    On the bottom of the job execution page, you will see the request item, which will go through the different stages: **PREPARING, QUEUING, QUEUED, RUNNING, PASSED, ERRORED or FAILED**:

    .. image:: images/xpresso-jobs-request-status-1.png
        :align: center
        :width: 75%

#. Click on the Request Item while job is running, and you will see how pyATS is executing every tests defined in the job file one by one in real-time:

    .. image:: images/xpresso-jobs-request-status-2.png
        :align: center
        :width: 55%

    .. note::
        If you click on Request item while job is going through **PREPARING, QUEUING, QUEUED** stages, there would be no visible results as job is not running yet. Once job transitions to RUNNING stage, the page will be updated and you will start getting test the execution results,

#. Once job execution is completed, you will see the results, can check raw console output, job history with timestamps, download archive with results or compare test execution with another job run:

    .. image:: images/xpresso-request-details.png
        :align: center
        :width: 75%


#. Let's introduce a network failure by connecting to **csr1000v-1** and shutting down interface **GigabitEthernet2**. From Admin Workstation launch Putty, login to **csr1000v-1** and execute commands:

    .. code-block:: bash

        configure terminal 
        interface gigabitEthernet 2
        shutdown

#. Go back to XPRESSO dashboard and click on Jobs menu item:

    .. image:: images/xpresso-jobs-filter.png
        :align: left
        :width: 15%

    |
    |
    |

#. Run **Ping_from_ASA** job again by repeating Steps 4 - 7. This time you will notice that one of the tests is failing:

    .. image:: images/xpresso-ping-from-asa.png
        :align: center
        :width: 55%

#. Now let's compare job results. On the top of the page click on the **Compare** button and check the last job run that was successful and  has the status **PASSED**:

    .. image:: images/xpresso-jobs-compare-1.png
        :align: center
        :width: 75%

#. You will see the summary of comparison for both job runs and a number of passed and failed tests:

    .. image:: images/xpresso-jobs-compare-2.png
        :align: center
        :width: 75%

    Followed by detailed test to test comparison:

    .. image:: images/xpresso-jobs-compare-3.png
        :align: center
        :width: 75%

#. Hover the mouse over the failing test line **ping[dest_ip=10.0.0.13]**, and click **Testcase Diff** icon on the right to see the test result in diff format:

    .. image:: images/xpresso-jobs-compare-4.png
        :align: center
        :width: 75%

    Section diff page will open and load diff plugin:

    .. image:: images/xpresso-jobs-compare-5.png
        :align: center
        :width: 75%

    .. note::
        Alternatively, you can compare test results by going to the **Requests** page and selecting 2 requests for comparison as described below.

#. Click on Requests menu item:

    .. image:: images/xpresso-jobs-filter.png
        :align: left
        :width: 15%

    |
    |
    |

#. Select 2 requests - PASSED and FAILED, and click the Compare icon on the top right of the page. Compare icon will be visible only if you select exactly 2 items:

    .. image:: images/xpresso-jobs-compare-6.png
        :align: center
        :width: 75%

#. Select 2 results for comparison and click **Compare** icon. This additional step is required as Job can include several requests ran as Job Bundle:

    .. image:: images/xpresso-jobs-compare-7.png
        :align: center
        :width: 75%

#. You will be brought to the results comparison page:

    .. image:: images/xpresso-jobs-compare-8.png
        :align: center
        :width: 75%

|

.. sectionauthor:: Luis Rueda <lurueda@cisco.com>, Jairo Leon <jaileon@cisco.com>
