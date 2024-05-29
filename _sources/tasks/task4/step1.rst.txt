Step 1: Show the Results of Tests in a Browser
##############################################

**Value Proposition:** Effectively communicating test results is crucial for business decision-making and collaboration. In this task, we will learn how to present test results in a visually appealing and easily accessible manner using a web browser. By leveraging the power of the pyats run job command, you can streamline the testing process, enhance team collaboration, and make informed decisions based on comprehensive test data.

When a test is executed using the **pyats run job** it adds the following advantages:

- Logs of test runs are saved into the archive
- Makes a graphical representation of test results in a browser
- Has the ability to run tests in different Python scripts

To use **pyats run job**, a special file “job file” (written in Python) should be created.

A job file looks like the following example:

**<test_name1>** - specifies the path in the system to the Python file with the first list of tests (for example **task3step3.py**).
**<test_name2>** - specifies the path to the Python file with the second list of tests (for example **task3step4.py**).


The method **run** from the imported library **pyats.easypy** instructs the system to run tests in sequence.

.. code-block:: python
    :emphasize-lines: 6-7, 10-11

    import os
    from pyats.easypy import run

    def main():
        # Find the location of the script concerning the job file
        <test_name1> = os.path.join('<file_with_tests1.py>')
        <test_name2> = os.path.join('<file_with_tests2.py>')
        
        # Execute the testscript
        run(testscript=<test_name1>)
        run(testscript=<test_name2>)

To call **pyats run job**, use the following command in a Bash shell:

.. code-block:: bash

    pyats run job <job-file> --testbed <testbed-file>

Schematically, the process of a **pyats run job** can be shown as follows:

.. image:: images/run-job-process.svg
    :width: 65%
    :align: center

Let's use a **pyats job run** to execute tests from task 3 step 4. PyATS job file **task4step1.py** has been pre-configured for this.

#. Open **runtestsjob.py** file in Nano and check it (the structure must be in accordance with the one shown above).

    .. code-block:: bash

        nano task4step1.py

#. Exit Nano without saving by pressing :guilabel:`Ctrl + X`

#. Execute the pyATS job file with the **pyats run job** command:

    .. code-block:: bash

        pyats run job task4step1.py  --testbed pyats_testbed.yaml

#. After the completion of the job, check the results:

    .. code-block:: bash

        pyats logs view

#. Google Chrome will be launched to show the last jobs run. Minimize the Linux shell window.

    .. note::

        Don't close the Linux shell; otherwise, it will stop the local pyATS web server.

    Click the upper line in a list to open the results of the last job run:

    .. image:: images/viewer-list-of-jobs-run.png
        :width: 75%
        :align: center

#. Detailed results of the tests comprising the last run job will be shown.

    .. note::

        Pay special attention to the result of each test, which is shown along with the start time and run time of each one.

    .. image:: images/pyats-log-viewer-results-page.png
        :width: 75%
        :align: center
    
    |

#. Click on the test **ping[dest_ip=10.0.0.17]** (see “1” in the next figure). A detailed log from the execution of this test will be shown on the right side of the window (see “2”).

#. Click on the **PASSED** button for the test **ping[dest_ip=10.0.0.17]** (see “3” in the next figure). Ensure that the test passed message is shown (see “4”).

    |

    .. image:: images/pyats-log-viewer-ping-test-results.png
        :width: 75%
        :align: center
    
    |

    You can open detailed results of the last job without opening the list of previous jobs, using the following command in the shell:

    .. code-block:: bash

        pyats logs view --latest

    To test this option, follow the next steps.

#. Maximize the Linux shell, minimized in step 5. Stop the running pyATS web server by pressing :guilabel:`Ctrl + C`
    
    Open the web page with the detailed results of the last job:

    .. code-block:: bash

        pyats logs view --latest

    Ensure detailed results of the tests comprising the last run job are shown right away.

#. Open the Linux shell again, and stop the running pyATS web server by pressing :guilabel:`Ctrl + C`
    
.. tip::

    pyATS run is a very handy tool and it is recommended that you use it to run your pyATS tests.

    You might also check the official documentation for the details found on this `site <https://pubhub.devnetcloud.com/media/pyats/docs/cli/pyats_run.html#pyats-run-job>`_.

.. sectionauthor:: Luis Rueda <lurueda@cisco.com>, Jairo Leon <jaileon@cisco.com>
