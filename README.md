# Python API for Nebulon

This is an API client for Nebulon ON for Python 3 and allows working with
Nebulon nPods just like with the Nebulon ON web user interface but in a
scriptable form.

## Installation

The Nebulon Python SDK client is available through the Python Package Index
with the name nebpyclient, but can also be installed from source.

**IMPORTANT**: Please review the changelog to transition from version 1.x of the
nebpyclient to version 2.x.

### Python Package Index

```bash
pip install nebpyclient
```

Or

```bash
python3 -m pip install nebpyclient
```

### Installation from Source Code

```bash
mkdir nebulon
cd nebulon
git clone https://github.com/nebulon/nebpyclient.git
cd nebpyclient
python3 setup.py install
```

To build the HTML documentation from source:

```bash
cd docs/
make html
```

## Using the API

To use this API, instantiate a `NebPyClient` object with username and password.
You can then use its methods to query state, and if a nPod is reachable from
where the script is being run modify the system. A simple script to display
the names of all of the pods in your organization along with a count of
the volumes in them would be:

```python
from nebpyclient import NebPyClient

client = NebPyClient("username", "password")

npod_list = client.get_npods()
for npod in npod_list.items:
    print(f"nPod {npod.name} has {npod.volume_count} volumes")
```

An example to create a 2 TiB volume called `volume name` on an existing nPod
with the name `NPod Name` would be:

```python
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
```

Full documentation on the API is available in the `docs` directory.
Some functions have comments that describe functions and methods and are
visible in modern Python IDEs.

Please review the
[current version of the documentation](https://nebulon.github.io/nebpyclient/index.html)
for more details.
