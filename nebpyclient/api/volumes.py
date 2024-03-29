#
# Copyright 2021 Nebulon, Inc.
# All Rights Reserved.
#
# DISCLAIMER: THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO
# EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
# OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#

from .graphqlclient import GraphQLParam, NebMixin
from datetime import datetime
from .common import NebEnum, PageInput, read_value
from .filters import StringFilter, UUIDFilter, IntFilter
from .sorting import SortDirection
from .tokens import TokenResponse

__all__ = [
    "VolumeSyncState",
    "VolumeSort",
    "VolumeFilter",
    "CreateVolumeInput",
    "DeleteVolumeInput",
    "UpdateVolumeInput",
    "CreateCloneInput",
    "Volume",
    "VolumeList",
    "VolumeMixin"
]


class VolumeSyncState(NebEnum):
    """Represents volume sync status for mirrored volumes"""

    NotMirrored = "NotMirrored"
    """The volume is not mirrored"""

    InSync = "InSync"
    """The volume is healthy and all data is in-sync"""

    Syncing = "Syncing"
    """The volume is unhealthy and data is currently synchronizing"""

    Unsynced = "Unsynced"
    """The volume is unhealthy and data is currently not synchronizing"""

    Unknown = "Unknown"
    """The volume sync status is unavailable"""


class VolumeSort:
    """A sort object for volumes

    Allows sorting volumes on common properties. The sort object allows
    only one property to be specified.
    """

    def __init__(
            self,
            name: SortDirection = None,
            wwn: SortDirection = None,
            size_bytes: SortDirection = None,
            creation_time: SortDirection = None,
            expiration_time: SortDirection = None
    ):
        """Constructs a new sort object for volumes

        Allows sorting volumes on common properties. The sort object allows
        only one property to be specified.

        :param name: Sort direction for the ``name`` property
        :type name: SortDirection, optional
        :param wwn: Sort direction for the ``wwn`` property
        :type wwn: SortDirection, optional
        :param size_bytes: Sort direction for the ``size_bytes`` property
        :type size_bytes: SortDirection, optional
        :param creation_time: Sort direction for the ``creation_time`` property
        :type creation_time: SortDirection, optional
        :param expiration_time: Sort direction for the ``expiration_time``
            property
        :type expiration_time: SortDirection, optional
        """

        self.__name = name
        self.__wwn = wwn
        self.__size_bytes = size_bytes
        self.__creation_time = creation_time
        self.__expiration_time = expiration_time

    @property
    def name(self) -> SortDirection:
        """Sort direction for the ``name`` property"""
        return self.__name

    @property
    def wwn(self) -> SortDirection:
        """Sort direction for the ``wwn`` property"""
        return self.__wwn

    @property
    def size_bytes(self) -> SortDirection:
        """Sort direction for the ``size_bytes`` property"""
        return self.__size_bytes

    @property
    def creation_time(self) -> SortDirection:
        """Sort direction for the ``creation_time`` property"""
        return self.__creation_time

    @property
    def expiration_time(self) -> SortDirection:
        """Sort direction for the ``expiration_time`` property"""
        return self.__expiration_time

    @property
    def as_dict(self):
        result = dict()
        result["name"] = self.name
        result["wwn"] = self.wwn
        result["sizeBytes"] = self.size_bytes
        result["creationTime"] = self.creation_time
        result["expirationTime"] = self.expiration_time
        return result


class VolumeFilter:
    """A filter object to filter volumes

    Allows filtering for specific volumes registered in nebulon ON. The
    filter allows only one property to be specified. If filtering on multiple
    properties is needed, use the ``and_filter`` and ``or_filter`` options to
    concatenate multiple filters.
    """

    def __init__(
            self,
            uuid: UUIDFilter = None,
            name: StringFilter = None,
            wwn: StringFilter = None,
            size_bytes: IntFilter = None,
            npod_uuid: UUIDFilter = None,
            snapshots_only: bool = None,
            base_only: bool = None,
            creation_time: IntFilter = None,
            expiration_time: IntFilter = None,
            parent_uuid: UUIDFilter = None,
            parent_name: StringFilter = None,
            natural_owner_spu_serial: StringFilter = None,
            natural_backup_spu_serial: StringFilter = None,
            sync_state: VolumeSyncState = None,
            and_filter=None,
            or_filter=None
    ):
        """Constructs a new filter object

        Allows filtering for specific volumes registered in nebulon ON. The
        filter allows only one property to be specified. If filtering on
        multiple properties is needed, use the ``and_filter`` and ``or_filter``
        options to concatenate multiple filters.

        :param uuid: Filter based on volume unique identifier
        :type uuid: StringFilter, optional
        :param name: Filter based on volume name
        :type name: StringFilter, optional
        :param wwn: Filter based on volume WWN
        :type wwn: StringFilter, optional
        :param size_bytes: Filter based on volume size
        :type size_bytes: IntFilter, optional
        :param npod_uuid: Filter based on nPod unique identifier
        :type npod_uuid: UUIDFilter, optional
        :param snapshots_only: Filter for only snapshots
        :type snapshots_only: bool, optional
        :param base_only: Filter for only base volumes
        :type base_only: bool, optional
        :param creation_time: Filter based on creation time
        :type creation_time: IntFilter, optional
        :param expiration_time: Filter based on snapshot expiration time
        :type expiration_time: IntFilter, optional
        :param parent_uuid: Filter based on volume parent uuid
        :type parent_uuid: UUIDFilter, optional
        :param parent_name: Filter based on volume parent name
        :type parent_name: StringFilter, optional
        :param natural_owner_spu_serial: Filter based on volume's natural
            owner SPU serial number
        :type natural_owner_spu_serial: StringFilter, optional
        :param natural_backup_spu_serial: Filter based on volume's natural
            backup SPU serial number
        :type natural_backup_spu_serial: StringFilter, optional
        :param sync_state: Filter based on volume's sync state
        :type sync_state: VolumeSyncState, optional
        :param and_filter: Concatenate another filter with a logical AND
        :type and_filter: VolumeFilter, optional
        :param or_filter: Concatenate another filter with a logical OR
        :type or_filter: VolumeFilter, optional
        """

        self.__uuid = uuid
        self.__name = name
        self.__wwn = wwn
        self.__size_bytes = size_bytes
        self.__npod_uuid = npod_uuid
        self.__snapshots_only = snapshots_only
        self.__base_only = base_only
        self.__creation_time = creation_time
        self.__expiration_time = expiration_time
        self.__parent_uuid = parent_uuid
        self.__parent_name = parent_name
        self.__natural_owner_spu_serial = natural_owner_spu_serial
        self.__natural_backup_spu_serial = natural_backup_spu_serial
        self.__sync_state = sync_state
        self.__and = and_filter
        self.__or = or_filter

    @property
    def uuid(self) -> UUIDFilter:
        """Filter based on volume unique identifier"""
        return self.__uuid

    @property
    def name(self) -> StringFilter:
        """Filter based on volume name"""
        return self.__name

    @property
    def wwn(self) -> StringFilter:
        """Filter based on volume WWN"""
        return self.__wwn

    @property
    def size_bytes(self) -> IntFilter:
        """Filter based on volume size"""
        return self.__size_bytes

    @property
    def npod_uuid(self) -> UUIDFilter:
        """Filter based on nPod unique identifier"""
        return self.__npod_uuid

    @property
    def snapshots_only(self) -> bool:
        """Filter for only snapshots"""
        return self.__snapshots_only

    @property
    def base_only(self) -> bool:
        """Filter for only base volumes"""
        return self.__base_only

    @property
    def creation_time(self) -> IntFilter:
        """Filter based on creation time"""
        return self.__creation_time

    @property
    def expiration_time(self) -> IntFilter:
        """Filter based on snapshot expiration time"""
        return self.__expiration_time

    @property
    def parent_uuid(self) -> UUIDFilter:
        """Filter based on volume parent uuid"""
        return self.__parent_uuid

    @property
    def parent_name(self) -> StringFilter:
        """Filter based on volume parent name"""
        return self.__parent_name

    @property
    def natural_owner_spu_serial(self) -> StringFilter:
        """Filter based on volume natural owner SPU serial number"""
        return self.__natural_owner_spu_serial

    @property
    def natural_backup_spu_serial(self) -> StringFilter:
        """Filter based on volume natural backup SPU serial number"""
        return self.__natural_backup_spu_serial

    @property
    def sync_state(self) -> VolumeSyncState:
        """Filter based on volume synchronization status"""
        return self.__sync_state

    @property
    def and_filter(self):
        """Allows concatenation of multiple filters via logical AND"""
        return self.__and

    @property
    def or_filter(self):
        """Allows concatenation of multiple filters via logical OR"""
        return self.__or

    @property
    def as_dict(self):
        result = dict()
        result["uuid"] = self.uuid
        result["name"] = self.name
        result["wwn"] = self.wwn
        result["sizeBytes"] = self.size_bytes
        result["nPodUUID"] = self.npod_uuid
        result["snapshotsOnly"] = self.snapshots_only
        result["baseOnly"] = self.base_only
        result["creationTime"] = self.creation_time
        result["expirationTime"] = self.expiration_time
        result["parentUUID"] = self.parent_uuid
        result["parentName"] = self.parent_name
        result["naturalOwnerSPUSerial"] = self.natural_owner_spu_serial
        result["naturalBackupSPUSerial"] = self.natural_backup_spu_serial
        result["syncState"] = self.sync_state
        result["and"] = self.and_filter
        result["or"] = self.or_filter
        return result


class DeleteVolumeInput:
    """An input object to delete a volume"""

    def __init__(
            self,
            cascade: bool = None
    ):
        """Constructs a new input object to delete a new volume.

        :param cascade: If specified and set to ``True`` all snapshots
            that are associated with the volume will be deleted with
            the deletion of this volume. Otherwise, only the volume
            will be deleted
        :type cascade: bool, optional
        """

        self.__cascade = cascade

    @property
    def cascade(self) -> bool:
        """Forces the creation of the volume and ignores any warnings"""
        return self.__cascade

    @property
    def as_dict(self):
        result = dict()
        result["cascade"] = self.cascade
        return result


class CreateCloneInput:
    """An input object to create a volume clone

    Allows the creation of a volume clone from a base volume or snapshot.
    Clones are read and writeable copies of another volume. Clones can be used
    to quickly instantiate copies of data and data for recovery purposes when
    applications require read/write access for copy operations.
    """

    def __init__(
            self,
            name: str,
            volume_uuid: str
    ):
        """Constructs a new input object to create a volume clone

        Allows the creation of a volume clone from a base volume or snapshot.
        Clones are read and writeable copies of another volume. Clones can be
        used to quickly instantiate copies of data and data for recovery
        purposes when applications require read/write access for copy
        operations.

        :param name: The human readable name for the volume clone
        :type name: str
        :param volume_uuid: The unique identifier for the volume or snapshot
            from which to create the clone
        :type volume_uuid: str
        """
        self.__name = name
        self.__volume_uuid = volume_uuid

    @property
    def clone_volume_name(self) -> str:
        """Name for the volume clone"""
        return self.__name

    @property
    def origin_volume_uuid(self) -> str:
        """Unique identifier of the volume or snapshot to clone"""
        return self.__volume_uuid

    @property
    def as_dict(self):
        result = dict()
        result["cloneVolumeName"] = self.clone_volume_name
        result["originVolumeUUID"] = self.origin_volume_uuid
        return result


class CreateVolumeInput:
    """An input object to create a new volume"""

    def __init__(
        self,
        name: str,
        size_bytes: int,
        npod_uuid: str,
        mirrored: bool = None,
        owner_spu_serial: str = None,
        backup_spu_serial: str = None,
        force: bool = None,
        download_contents_url: str = None,
        replace_lun: str = None,
        boot: bool = None,
    ):
        """Constructs a new input object to create a new volume.

        If ``owner_spu_serial`` or ``backup_spu_serial`` are not provided,
        nebulon ON will automatically determine where the volume will be
        provisioned.

        :param name: The name for the volume
        :type name: str
        :param size_bytes: The size of the volume in bytes
        :type size_bytes: int
        :param npod_uuid: The uuid of the nPod in which to create the volume
        :type npod_uuid: str
        :param mirrored: Indicates if the volume shall be created with high
            availability. By default the volume will be created without
            mirroring
        :type mirrored: bool, optional
        :param owner_spu_serial: Create the volume on the SPU indicated with
            this serial number
        :type owner_spu_serial: str, optional
        :param backup_spu_serial: If the volume is mirrored, create the
            backup mirror on the specified SPU
        :type backup_spu_serial: str, optional
        :param force: Forces the creation of the volume even if there is no
            available capacity available. By default the volume creation will
            fail if there is not enough capacity available
        :type force: bool, optional
        :param download_contents_url: If specified, the contents of the given
            URL will be downloaded to the newly created volume.
        :type download_contents_url: str, optional
        :param replace_lun: If specified, the given lun will be replaced after
            the download completes and the host reboots.  Lun 0 of the owner
            SPU will be used if the UUID is 00000000-0000-0000-0000-000000000000.
        :type replace_lun: str, optional
        :param boot: indicates if the volume is a boot volume
        :type boot: bool, optional
        """

        self.__name = name
        self.__npod_uuid = npod_uuid
        self.__size_bytes = size_bytes
        self.__mirrored = mirrored
        self.__owner_spu_serial = owner_spu_serial
        self.__backup_spu_serial = backup_spu_serial
        self.__force = force
        self.__download_contents_url = download_contents_url
        self.__replace_lun = replace_lun
        self.__boot = boot

    @property
    def name(self) -> str:
        """The name for the volume"""
        return self.__name

    @property
    def npod_uuid(self) -> str:
        """The uuid of the nPod in which to create the volume"""
        return self.__npod_uuid

    @property
    def size_bytes(self) -> int:
        """The size of the volume in bytes"""
        return self.__size_bytes

    @property
    def mirrored(self) -> bool:
        """Indicates if the volume shall be created with high availability"""
        return self.__mirrored

    @property
    def owner_spu_serial(self) -> str:
        """Create the volume on the SPU indicated with this serial number"""
        return self.__owner_spu_serial

    @property
    def backup_spu_serial(self) -> str:
        """If the volume is mirrored, create a mirror on the specified SPU"""
        return self.__backup_spu_serial

    @property
    def force(self) -> bool:
        """Forces the creation of the volume and ignores any warnings"""
        return self.__force

    @property
    def download_contents_url(self) -> str:
        """Contents of the given URL will be downloaded to the newly created volume"""
        return self.__download_contents_url

    @property
    def replace_lun(self) -> str:
        """Given lun will be replaced after the download completes and the host reboots.
            Lun 0 of the owner SPU will be used if the UUID is 00000000-0000-0000-0000-000000000000"""
        return self.__replace_lun

    @property
    def boot(self) -> bool:
        """Indicates if the volume is a boot volume"""
        return self.__boot

    @property
    def as_dict(self):
        result = dict()
        result["name"] = self.name
        result["nPodUUID"] = self.npod_uuid
        result["sizeBytes"] = self.size_bytes
        result["mirrored"] = self.mirrored
        result["ownerSPUSerial"] = self.owner_spu_serial
        result["backupSPUSerial"] = self.backup_spu_serial
        result["force"] = self.force
        result["downloadContentsURL"] = self.__download_contents_url
        result["replaceLun"] = self.__replace_lun
        result["boot"] = self.__boot
        return result


class UpdateVolumeInput:
    """An input object to update an existing volume"""

    def __init__(
            self,
            name: str = None,
    ):
        """Constructs a new input object to update an existing volume.

        :param name: The new name for the volume
        :type name: str
        """

        self.__name = name

    @property
    def name(self) -> str:
        """The new name for the volume"""
        return self.__name

    @property
    def as_dict(self):
        result = dict()
        result["name"] = self.name
        return result


class Volume:
    """A volume"""

    def __init__(
            self,
            response: dict
    ):
        """Constructs a volume object

        This constructor expects a ``dict`` object from the nebulon ON API. It
        will check the returned data against the currently implemented schema
        of the SDK.

        :param response: The JSON response from the server
        :type response: dict

        :raises ValueError: An error if illegal data is returned from the server
        """

        self.__uuid = read_value(
            "uuid", response, str, True)
        self.__npod_uuid = read_value(
            "nPod.uuid", response, str, False)
        self.__wwn = read_value(
            "wwn", response, str, True)
        self.__name = read_value(
            "name", response, str, True)
        self.__size_bytes = read_value(
            "sizeBytes", response, int, True)
        self.__creation_time = read_value(
            "creationTime", response, datetime, True)
        self.__expiration_time = read_value(
            "expirationTime", response, datetime, False)
        self.__read_only_snapshot = read_value(
            "readOnlySnapshot", response, bool, True)
        self.__snapshot_parent_uuid = read_value(
            "snapshotParent.uuid", response, str, False)
        self.__natural_owner_host_uuid = read_value(
            "naturalOwnerHost.uuid", response, str, False)
        self.__natural_backup_host_uuid = read_value(
            "naturalBackupHost.uuid", response, str, False)
        self.__current_owner_host_uuid = read_value(
            "currentOwnerHost.uuid", response, str, False)
        self.__natural_owner_spu_serial = read_value(
            "naturalOwnerSPU.serial", response, str, False)
        self.__natural_backup_spu_serial = read_value(
            "naturalBackupSPU.serial", response, str, False)
        self.__accessible_by_host_uuids = read_value(
            "accessibleByHosts.uuid", response, str, False)
        self.__sync_state = read_value(
            "syncState", response, VolumeSyncState, False)
        self.__boot = read_value(
            "boot", response, bool, True)

    @property
    def uuid(self) -> str:
        """The unique identifier of the volume"""
        return self.__uuid

    @property
    def npod_uuid(self) -> str:
        """The unique identifier of the nPod for this volume"""
        return self.__npod_uuid

    @property
    def wwn(self) -> str:
        """The world wide name of the volume"""
        return self.__wwn

    @property
    def name(self) -> str:
        """The name of the volume"""
        return self.__name

    @property
    def size_bytes(self) -> int:
        """The size of the volume in bytes"""
        return self.__size_bytes

    @property
    def creation_time(self) -> datetime:
        """Date and time when the volume was created"""
        return self.__creation_time

    @property
    def expiration_time(self) -> datetime:
        """Date and time when the snapshot is automatically deleted"""
        return self.__expiration_time

    @property
    def read_only_snapshot(self) -> bool:
        """Indicates if the volume is a read-only snapshot"""
        return self.__read_only_snapshot

    @property
    def snapshot_parent_uuid(self) -> str:
        """Indicates the parent volume of a snapshot"""
        return self.__snapshot_parent_uuid

    @property
    def natural_owner_host_uuid(self) -> str:
        """The uuid of the host / server that is the natural owner"""
        return self.__natural_owner_host_uuid

    @property
    def natural_backup_host_uuid(self) -> str:
        """The uuid of the host / server that is the natural backup"""
        return self.__natural_backup_host_uuid

    @property
    def natural_owner_spu_serial(self) -> str:
        """The serial number of the SPU that is the natural owner"""
        return self.__natural_owner_spu_serial

    @property
    def natural_backup_spu_serial(self) -> str:
        """The serial number of the SPU that is the natural backup"""
        return self.__natural_backup_spu_serial

    @property
    def current_owner_host_uuid(self) -> str:
        """The uuid of the current host / server owner of a volume"""
        return self.__current_owner_host_uuid

    @property
    def accessible_by_host_uuids(self) -> [str]:
        """List of host / server uuids that have access to the volume"""
        return self.__accessible_by_host_uuids

    @property
    def sync_state(self) -> VolumeSyncState:
        """Indicates the health and sync state of the volume"""
        return self.__sync_state

    @property
    def boot(self) -> str:
        """Indicates if the volume is a boot volume"""
        return self.__boot

    @staticmethod
    def fields():
        return [
            "uuid",
            "nPod{uuid}",
            "wwn",
            "name",
            "sizeBytes",
            "creationTime",
            "expirationTime",
            "readOnlySnapshot",
            "snapshotParent{uuid}",
            "naturalOwnerHost{uuid}",
            "naturalBackupHost{uuid}",
            "currentOwnerHost{uuid}",
            "naturalOwnerSPU{serial}",
            "naturalBackupSPU{serial}",
            "accessibleByHosts{uuid}",
            "syncState",
            "boot",
        ]


class VolumeList:
    """Paginated list of volumes

    Contains a list of volume objects and information for
    pagination. By default a single page includes a maximum of ``100`` items
    unless specified otherwise in the paginated query.

    Consumers should always check for the property ``more`` as per default
    the server does not return the full list of alerts but only one page.
    """

    def __init__(
            self,
            response: dict
    ):
        """Constructs a new volume list object

        This constructor expects a ``dict`` object from the nebulon ON API. It
        will check the returned data against the currently implemented schema
        of the SDK.

        :param response: The JSON response from the server
        :type response: dict

        :raises ValueError: An error if illegal data is returned from the server
        """

        self.__items = read_value(
            "items", response, Volume, True)
        self.__more = read_value(
            "more", response, bool, True)
        self.__total_count = read_value(
            "totalCount", response, int, True)
        self.__filtered_count = read_value(
            "filteredCount", response, int, True)

    @property
    def items(self) -> [Volume]:
        """List of volume in the pagination list"""
        return self.__items

    @property
    def more(self) -> bool:
        """Indicates if there are more items on the server"""
        return self.__more

    @property
    def total_count(self) -> int:
        """The total number of items on the server"""
        return self.__total_count

    @property
    def filtered_count(self) -> int:
        """The number of items on the server matching the provided filter"""
        return self.__filtered_count

    @staticmethod
    def fields():
        return [
            "items{%s}" % ",".join(Volume.fields()),
            "more",
            "totalCount",
            "filteredCount",
        ]


class VolumeMixin(NebMixin):
    """Mixin to add volume related methods to the GraphQL client"""

    def get_volumes(
            self,
            page: PageInput = None,
            volume_filter: VolumeFilter = None,
            sort: VolumeSort = None
    ) -> VolumeList:
        """Retrieves a list of volumes

        :param page: The requested page from the server. This is an optional
            argument and if omitted the server will default to returning the
            first page with a maximum of ``100`` items.
        :type page: PageInput, optional
        :param volume_filter: A filter object to filter the volumes on the
            server. If omitted, the server will return all objects as a
            paginated response.
        :type volume_filter: VolumeFilter, optional
        :param sort: A sort definition object to sort the volume objects on
            supported properties. If omitted objects are returned in the order
            as they were created in.
        :type sort: VolumeSort, optional

        :returns VolumeList: A paginated list of volumes

        :raises GraphQLError: An error with the GraphQL endpoint.
        """

        # setup query parameters
        parameters = dict()
        parameters["page"] = GraphQLParam(
            page, "PageInput", False)
        parameters["filter"] = GraphQLParam(
            volume_filter, "VolumeFilter", False)
        parameters["sort"] = GraphQLParam(
            sort, "VolumeSort", False)

        # make the request
        response = self._query(
            name="getVolumes",
            params=parameters,
            fields=VolumeList.fields()
        )

        # convert to object
        return VolumeList(response)

    def create_volume(
            self,
            create_volume_input: CreateVolumeInput,
            ignore_warnings: bool = False,
    ) -> Volume:
        """Allows creation of a new volume


        :param create_volume_input: An input object that describes the
            volume to be created
        :type create_volume_input: CreateVolumeInput
        :param ignore_warnings: If specified and set to ``True`` the operation 
            will proceed even if nebulon ON reports warnings. It is
            advised to not ignore warnings. Consequently, the default behavior
            is that the operation will fail when nebulon ON reports
            validation errors or warnings.
        :type ignore_warnings: bool, optional

        :returns Volume: The created volume

        :raises GraphQLError: An error with the GraphQL endpoint.
        :raises Exception: An error when delivering a token to the SPU
        """

        # setup query parameters
        parameters = dict()
        parameters["input"] = GraphQLParam(
            create_volume_input,
            "CreateVolumeInputV2",
            True
        )

        # make the request
        mutation_name = "createVolumeV3"
        response = self._mutation(
            name=mutation_name,
            params=parameters,
            fields=TokenResponse.fields()
        )

        # convert to object and deliver token
        token_response = TokenResponse(
            response=response,
            ignore_warnings=ignore_warnings,
        )
        delivery_response = token_response.deliver_token()

        # wait for recipe completion
        self._wait_on_recipes(delivery_response, mutation_name)

        npod_uuid = delivery_response["npod_uuid_to_wait_on"]
        volume_list = self.get_volumes(
            volume_filter=VolumeFilter(
                npod_uuid=UUIDFilter(
                    equals=npod_uuid
                ),
                and_filter=VolumeFilter(
                    name=StringFilter(
                        equals=create_volume_input.name
                    )
                )
            )
        )

        if volume_list.filtered_count != 0:
            return volume_list.items[0]
        
        return None

    def delete_volume(
            self,
            uuid: str,
            cascade: bool = False,
            ignore_warnings: bool = False,
    ):
        """Allows deletion of a volume

        :param uuid: The unique identifier of the volume or snapshot to delete
        :type uuid: str
        :param cascade: If set to True all associated snapshots will be deleted
            with the parent volume. If set to False, only this volume is
            deleted
        :type cascade: bool, optional
        :param ignore_warnings: If specified and set to ``True`` the operation 
            will proceed even if nebulon ON reports warnings. It is
            advised to not ignore warnings. Consequently, the default behavior
            is that the operation will fail when nebulon ON reports
            validation errors or warnings.
        :type ignore_warnings: bool, optional

        :raises GraphQLError: An error with the GraphQL endpoint.
        :raises Exception: An error when delivering a token to the SPU
        """

        # setup query parameters
        parameters = dict()
        parameters["uuid"] = GraphQLParam(
            uuid,
            "UUID",
            True
        )
        parameters["input"] = GraphQLParam(
            DeleteVolumeInput(
                cascade=cascade
            ),
            "DeleteVolumeInput",
            True
        )

        # make the request
        response = self._mutation(
            name="deleteVolumeV3",
            params=parameters,
            fields=TokenResponse.fields()
        )

        # convert to object and deliver token
        token_response = TokenResponse(
            response=response,
            ignore_warnings=ignore_warnings,
        )
        token_response.deliver_token()

    def update_volume(
            self,
            uuid: str,
            update_volume_input: UpdateVolumeInput,
            ignore_warnings: bool = False,
    ):
        """Allows deletion of a volume

        :param uuid: The unique identifier of the volume or snapshot to delete
        :type uuid: str
        :param update_volume_input: An input object that describes the changes
            to apply to the volume
        :type update_volume_input: UpdateVolumeInput
        :param ignore_warnings: If specified and set to ``True`` the operation 
            will proceed even if nebulon ON reports warnings. It is
            advised to not ignore warnings. Consequently, the default behavior
            is that the operation will fail when nebulon ON reports
            validation errors or warnings.
        :type ignore_warnings: bool, optional

        :raises GraphQLError: An error with the GraphQL endpoint.
        :raises Exception: An error when delivering a token to the SPU
        """

        # setup query parameters
        parameters = dict()
        parameters["uuid"] = GraphQLParam(
            uuid,
            "UUID",
            True
        )
        parameters["input"] = GraphQLParam(
            update_volume_input,
            "UpdateVolumeInput",
            True
        )

        # make the request
        response = self._mutation(
            name="updateVolume",
            params=parameters,
            fields=TokenResponse.fields()
        )

        # convert to object and deliver token
        token_response = TokenResponse(
            response=response,
            ignore_warnings=ignore_warnings,
        )
        token_response.deliver_token()

    def create_clone(
        self,
        create_clone_input: CreateCloneInput,
        ignore_warnings: bool = False,
    ) -> Volume:
        """Create a clone of a volume

        Clones are exact copies of volumes or snapshots. In contrast to
        immutable snapshots, clones are mutable copies and can be written to by
        hosts.

        :param create_clone_input: An input object that describes the clone
        :type create_clone_input: CreateCloneInput
        :param ignore_warnings: If specified and set to ``True`` the operation 
            will proceed even if nebulon ON reports warnings. It is
            advised to not ignore warnings. Consequently, the default behavior
            is that the operation will fail when nebulon ON reports
            validation errors or warnings.
        :type ignore_warnings: bool, optional

        :returns Volume: The created volume

        :raises GraphQLError: An error with the GraphQL endpoint.
        :raises Exception: An error when delivering a token to the SPU
        """

        # setup query parameters
        parameters = dict()
        parameters["input"] = GraphQLParam(
            create_clone_input,
            "CreateCloneInput",
            True
        )

        # make the request
        mutation_name = "createCloneV2"
        response = self._mutation(
            name=mutation_name,
            params=parameters,
            fields=TokenResponse.fields()
        )

        # convert to object and deliver token
        token_response = TokenResponse(
            response=response,
            ignore_warnings=ignore_warnings,
        )
        delivery_response = token_response.deliver_token()

        # wait for recipe completion
        self._wait_on_recipes(delivery_response, mutation_name)

        npod_uuid = delivery_response["npod_uuid_to_wait_on"]
        volume_list = self.get_volumes(
            volume_filter=VolumeFilter(
                npod_uuid=UUIDFilter(
                    equals=npod_uuid
                ),
                and_filter=VolumeFilter(
                    name=StringFilter(
                        equals=create_clone_input.clone_volume_name
                    )
                )
            )
        )

        if volume_list.filtered_count != 0:
            return volume_list.items[0]
        
        return None
