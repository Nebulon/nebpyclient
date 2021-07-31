Quick Start Guide
=================

This guide is intended to give #nebNerds a starting point and provide them
with the basic information to get started using the Nebulon Python SDK by
use of examples.

Before you start
----------------

The guide assumes that you have already installed the Nebulon Python SDK
including all of its dependencies. Review the ``requirements.txt`` file
at the root of the repository for the full list of dependencies.

For installation instructions see :doc:`installation`.

Connecting to Nebulon ON
------------------------

To use the SDK, instantiate a NebPyClient object with username and password.
You can then use its methods to query state, and if a nPod is reachable from
where the script is being run modify the system.

.. code-block:: python

    from nebpyclient import NebPyClient

    client = NebPyClient("username", "password")


If this command succeeds without a ``GraphQLError``, you are ready to query
the Nebulon ON API with the client. Queries (read access) can be done from any
client. A simple script to display the names of all of the pods in your
organization along with a count of the volumes in them would be:

.. code-block:: python

    from nebpyclient import NebPyClient

    client = NebPyClient("username", "password")

    npod_list = client.get_npods()
    for npod in npod_list.items:
        print(f"nPod {npod.name} has {npod.volume_count} volumes")


However, mutations (write access) that make changes to your on-premises
infrastructure require a successful completion of the security triangle and
requires the client to run on a device that has direct network access to the
affected nPod or SPUs. An example that requires the security triangle is the
creation of a ``2 TiB`` volume called ``volume name`` on an existing nPod with the
name ``NPod Name`` would be:

.. code-block:: python

    from nebpyclient import NebPyClient
    from nebpyclient import NPodFilter, StringFilter

    client = NebPyClient("username", "password")

    # find the nPod by name
    npod_list = client.get_npods(
        npod_filter=NPodFilter(
            name=StringFilter(
                equals="NPod Name"
            )
        )
    )

    if npod_list.filtered_count == 0:
        # nPod with the name "NPod Name" not found
        exit(-1)

    npod_uuid = npod_list.items[0].uuid
    volume_name="volume name"
    volume_size_bytes = 2 * 1024 * 1024 * 1024 * 1024 # 2 TiB

    # create the volume
    client.create_volume(
        name=volume_name,
        size_bytes=volume_size_bytes,
        npod_uuid=npod_uuid
    )

The full documentation and available queries and mutations is available in
:doc:`api`. Most functions have docstring comments that describe functions,
methods and their parameters that modern Python IDEs can display.
