Installation Guide
==================

The Nebulon Python SDK client is available through the Python Package Index
with the name ``nebpyclient``.

The source code is available on github.com and can be installed from source.


Python Package Index Installation
---------------------------------

.. code-block:: bash

    pip install nebpyclient

Or

.. code-block:: bash

    python3 -m pip install nebpyclient


Source Code Installation
------------------------

.. code-block:: bash

    mkdir nebulon
    cd nebulon
    git clone https://github.com/nebulon/nebpyclient.git
    cd nebpyclient
    python3 setup.py install

To build the HTML documentation from source:

.. code-block:: bash

    cd docs/
    make html

