Step 3: Configure the script and execute
########################################

**Value Proposition:** In this step, we will create a script and execute it, to run the desired tests against the device under test.


#. Expand the left-hand navigational panel and scroll down to :guilabel:`Test Cases` and click on the :guilabel:`Test Cases` sub-section.

    .. image:: images/cxtm-test-cases.png
        :width: 75%
        :align: center

#. Let's now add a new test case by clicking on the :guilabel:`+` button.

    .. image:: images/cxtm-test-case-add.png
        :width: 75%
        :align: center

    |

    A pop-up will appear, enter the information for the test case as detailed in the following image. Click on the :guilabel:`SUBMIT` button when you are done.

    .. image:: images/cxtm-test-case-add-details.png
        :width: 55%
        :align: center


#. Click on the :guilabel:`Open` link to display the test case details.

    .. image:: images/cxtm-open-test-case.png
        :width: 75%
        :align: center

    |

    A pop-up will appear, click on the :guilabel:`Configure Automation` button.

    .. image:: images/cxtm-test-case-configure-automation.png
        :width: 75%
        :align: center

#. The New Job File will be displayed, this screen contains an editor for ROBOT framework code execution. By default, this editor is populated with the basic ROBOT automation testing job-file. This default job-file that is loaded can be customized to your testing needs in the left-hand navigational panel.

    .. image:: images/cxtm-test-case-configure-automation-editor.png
        :width: 75%
        :align: center

#. Replace the ``*** Test Cases ***`` section with the following contents:

    .. literalinclude:: ./reference/test_case_1.robot
        :language: robotframework


    .. note:: 
        ROBOT is readable by everyone! i.e.   run "show inventory"

        The above statement in plain English from the Robot Framework test case is called a ROBOT keyword. These are generic and reusable terms. Our automation developers define and implement Robot Framework keywords in Python behind the scenes, allowing customers and engineers to focus on the breakdown of test steps for readability and usability using ROBOT. Our developers & testers work together to create more keywords that express different test automation scenarios. Customers can also add their keywords if needed. As keyword count increases, test automation velocity increases as less time is spent re-writing the same automation (how many times have you seen the same interface flap code repeated!?)

#. We now have a full ROBOT test. Select the latest “Runtime Image Version” container that has all these keyword libraries. Select ``cxta:23.8``. Select :guilabel:`Save` to save this job file.

    .. image:: images/cxtm-test-case-configure-automation-save.png
        :width: 75%
        :align: center

    |

    .. tip::
        In case you see a warning message about **Autocomplete may not work** when you select the Runtime Image Version, please ignore it and continue.

#. We are now ready to run our first ROBOT test case! Click on the :guilabel:`Run` button in the execution section to begin the test.

    .. image:: images/cxtm-test-case-configure-automation-run.png
        :width: 75%
        :align: center

#. The test will now show `STARTED`.

    .. note:: 
        You can click on the Task Id link to watch the job execution in real time. This test is executed very quickly. After a minute, if your screen does not load (stays black), click the job-file name 'Verify routing information' in the link at the top of the page to get back to the testing summary page.


#. The execution status will show `COMPLETED` for successful execution. If the execution status is anything other than `COMPLETED`, please reach out to your session speakers.

    .. image:: images/cxtm-test-case-configure-automation-completed.png
        :width: 55%
        :align: center

#. Refresh the page to see the execution details and move to the `Run History` section.

#. The Run History section will show all previous runs of this test case. Each test case run has a time stamp and the job result. Click the job time stamp to review the test results when the ROBOT test case is finished executing.

    .. image:: images/cxtm-test-case-configure-automation-run-history.png
        :width: 75%
        :align: center

#. Click on the ``log.html``  in the artifact section to view the full audit trail of the script events and the logs associated with the execution.

    .. image:: images/cxtm-test-case-configure-automation-run-history-log-html.png
        :width: 75%
        :align: center

#. Click on :guilabel:`+` to expand this keyword section.  Notice that by expanding the various keywords, you can see more detail at each step. The steps here show that the first keyword `load testbed` loaded the topology file you created earlier in this exercise. The next step connects to device "nx-osv-1" using the connection information provided to connect to the device.

    .. image:: images/cxtm-test-case-configure-automation-run-history-log-html-expand.png
        :width: 75%
        :align: center

#. Expand Step #4 and Step #6 to view the output execution for "show ip route summary" of existing route count on the device before and after clearing routes on Step #5 to make sure they are back in a good operating state.

    .. image:: images/cxtm-test-case-configure-automation-run-history-log-html-expand-2.png
        :width: 75%
        :align: center

.. note::
    Within this step, you have created a test case, configured the test case to run a ROBOT test, and executed the test case. You have also reviewed the results of the test case execution where you verified the routing information on the device. You can now move on to the next step to learn how to verify connectivity.

.. sectionauthor:: Nandakumar Arunachalam <narunach@cisco.com>, Jinrui Wang <jinrwang@cisco.com>, Luis Rueda <lurueda@cisco.com>, Jairo Leon <jaileon@cisco.com>
