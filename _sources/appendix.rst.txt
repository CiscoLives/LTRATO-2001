Appendix: Installing Pre-Requisites
###################################

.. Note ::

   The requirements are already installed in your POD, you ``DON'T`` need to install it.


Install Docker
--------------

As part of requirements Docker is needed, you can install it using the following commands:

.. literalinclude:: reference/install-docker.sh
   :language: bash

Install docker desktop

.. literalinclude:: reference/install-docker-desktop.sh
   :language: bash

Install Git
-----------

Install Git using the following command:

.. code-block:: bash

    sudo yum install git

Install anx
-----------

Install ANX using the following command:

.. code-block:: bash

    docker run --name netconf-exlorer -d -p 9269:8080 userlerueda/anx

Install Postman
---------------

Install Postman using the following scripts:

.. literalinclude:: reference/install-postman.sh
   :language: bash


Add potsman icon to desktop:

.. literalinclude:: reference/add-desktop-icon.sh
   :language: bash


.. sectionauthor:: Luis Rueda <lurueda@cisco.com>, Jairo Leon <jaileon@cisco.com>, Ovesnel Mas Lara <omaslara@cisco.com>
