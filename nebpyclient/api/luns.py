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

from time import sleep
from datetime import datetime
from .graphqlclient import GraphQLParam, NebMixin
from .common import PageInput, read_value
from .filters import UUIDFilter, IntFilter, StringFilter
from .sorting import SortDirection
from .recipe import RecipeState, NPodRecipeFilter
from .npods import _TIMEOUT_SECONDS
from .tokens import TokenResponse

__all__ = [
    "LUN",
    "LUNSort",
    "LUNsMixin",
    "LUNList",
    "LUNFilter",
    "CreateLUNInput",
    "BatchDeleteLUNInput",
]


class LUNSort:
    """A sort object for LUNs

    Allows sorting LUNs on common properties. The sort object allows
    only one property to be specified.
    """

    def __init__(
            self,
            lun_id: SortDirection = None
    ):
        """Constructs a new sort object for LUNs

        :param lun_id: Sort direction for the ``lun_id`` property of a LUN
        :type lun_id: SortDirection, optional
        """

        self.__lun_id = lun_id

    @property
    def lun_id(self) -> SortDirection:
        """Sort direction for the ``lun_id`` property of a LUN"""
        return self.__lun_id

    @property
    def as_dict(self):
        result = dict()
        result["lunID"] = self.lun_id
        return result


class LUNFilter:
    """A filter object to filter LUNs.

    Allows filtering for specific LUNs. The filter allows only one property to
    be specified. If filtering on multiple properties is needed, use the
    ``and_filter`` and ``or_filter`` options to concatenate multiple filters.
    """

    def __init__(
            self,
            uuid: UUIDFilter = None,
            lun_id: IntFilter = None,
            spu_serial: StringFilter = None,
            volume_uuid: UUIDFilter = None,
            npod_uuid: UUIDFilter = None,
            host_uuid: StringFilter = None,
            and_filter=None,
            or_filter=None
    ):
        """Constructs a new filter object

        The filter allows only one property to be specified. If filtering on
        multiple properties is needed, use the ``and_filter`` and ``or_filter``
        options to concatenate multiple filters.

        :param uuid: Filter based on datacenter unique identifiers
        :type uuid: UUIDFilter, optional
        :param lun_id: Filter based on ``lun_id`` property of a LUN
        :type lun_id: IntFilter, optional
        :param spu_serial: Filter based on the SPU serial number on which the
            LUN is active
        :type spu_serial: StringFilter, optional
        :param volume_uuid: Filter based on the unique identifier of the
            volume this LUN relates to
        :type volume_uuid: UUIDFilter, optional
        :param npod_uuid: Filter based on the nPod unique identifier this LUN
            relates to
        :type npod_uuid: UUIDFilter, optional
        :param host_uuid: Filter based on the host unique identifier on which
            the LUN is active
        :type host_uuid: StringFilter, optional
        :param and_filter: Concatenate another filter with a logical AND
        :type and_filter: LUNFilter, optional
        :param or_filter: Concatenate another filter with a logical OR
        :type or_filter: LUNFilter, optional
        """

        self.__uuid = uuid
        self.__lun_id = lun_id
        self.__spu_serial = spu_serial
        self.__volume_uuid = volume_uuid
        self.__npod_uuid = npod_uuid
        self.__host_uuid = host_uuid
        self.__and = and_filter
        self.__or = or_filter

    @property
    def uuid(self) -> UUIDFilter:
        """Filter based on LUN unique identifier"""
        return self.__uuid

    @property
    def lun_id(self) -> IntFilter:
        """Filter based on LUN ID"""
        return self.__lun_id

    @property
    def spu_serial(self) -> StringFilter:
        """Filter based on the SPU serial number on which the LUN is active"""
        return self.__spu_serial

    @property
    def volume_uuid(self) -> UUIDFilter:
        """Filter based on the UUID of the volume this LUN relates to"""
        return self.__volume_uuid

    @property
    def npod_uuid(self) -> UUIDFilter:
        """Filter based on the nPod unique identifier this LUN relates to"""
        return self.__npod_uuid

    @property
    def host_uuid(self) -> StringFilter:
        """Filter based on the host identifier on which the LUN is active"""
        return self.__host_uuid

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
        result["lunID"] = self.lun_id
        result["spuSerial"] = self.spu_serial
        result["volumeUUID"] = self.volume_uuid
        result["nPodUUID"] = self.npod_uuid
        result["hostUUID"] = self.host_uuid
        result["and"] = self.and_filter
        result["or"] = self.or_filter
        return result


class CreateLUNInput:
    """An input object to create a LUN for a volume

    Allows the creation of a LUN for a volume. A LUN is an instance of a
    volume export that makes a volume accessible to a host.
    """

    def __init__(
            self,
            volume_uuid: str,
            lun_id: int = None,
            host_uuids: [str] = None,
            spu_serials: [str] = None,
            npod_lun: bool = None,
            local: bool = None
    ):
        """Constructs a new input object to create a LUN for a volume

        Allows the creation of a LUN for a volume. A LUN is an instance of a
        volume export that makes a volume accessible to a host.

        Exactly one of the following properties must be specified:
        - ``host_uuids``
        - ``spu_serials``
        - ``npod_lun``

        If ``host_uuids`` is specified, the volume identified by ``volume_uuid``
        will be exported to all hosts in the list of UUIDs. If ``spu_serials``
        is provided the volume will be exported through the specified list of
        SPU serial numbers. If ``npod_lun`` is provided, the volume will be
        exported to all hosts in the nPod through one SPU in the host.

        During export, the ``local`` option allows control over the ALUA
        setting. If set to ``True``, the volume will be exported with ALUA
        turned off. If set to ``False``, ALUA will be turned on for each LUN
        that is created.


        :param volume_uuid: The unique identifier of the volume that shall be
            made available to a host
        :type volume_uuid: str
        :param lun_id: An optional LUN ID to export volumes with a specific ID.
            If the value is not provided, nebulon will automatically determine
            the LUN ID based on available values.
        :type lun_id: int, optional
        :param host_uuids: List of host UUIDs that identify the hosts the
            volume shall be exported to. Only a single LUN will be created for
            each host in the provided list.
        :type host_uuids: [str], optional
        :param spu_serials: List of SPU serials that identify the serials the
            volume shall be exported to. Only a single LUN will be created for
            each SPU in the provided list.
        :type spu_serials: [str], optional
        :param npod_lun: If specified and set to ``True`` a LUN will be created
            for each host in the nPod. If not specified, this parameter defaults
            to ``False`` and either ``host_uuids`` or ``spu_serials`` must be
            specified.
        :type npod_lun: bool, optional
        :param local: If provided and set to ``True`` then the volume will be
            exported with ALUA turned off, otherwise with ALUA turned on.
        :type local: bool, optional
        """

        self.__volume_uuid = volume_uuid
        self.__host_uuids = host_uuids
        self.__spu_serials = spu_serials
        self.__npod_lun = npod_lun
        self.__lun_id = lun_id
        self.__local = local

    @property
    def volume_uuid(self) -> str:
        """The identifier of the volume that shall be exported to a host"""
        return self.__volume_uuid

    @property
    def host_uuids(self) -> [str]:
        """The hosts to which a volume shall be exported to"""
        return self.__host_uuids

    @property
    def spu_serials(self) -> [str]:
        """The SPUs from which a volume shall be exported from"""
        return self.__spu_serials

    @property
    def lun_id(self) -> int:
        """An optional LUN ID to assign to the volume export"""
        return self.__lun_id

    @property
    def npod_lun(self) -> bool:
        """If ``True``, volumes will be exported to all hosts in the nPod"""
        return self.__npod_lun

    @property
    def local(self) -> bool:
        """If ``True``, volumes will be exported with ALUA turned off"""
        return self.__local

    @property
    def as_dict(self):
        result = dict()
        result["volumeUUID"] = self.volume_uuid
        result["hostUUIDs"] = self.host_uuids
        result["spuSerials"] = self.spu_serials
        result["nPodLun"] = self.npod_lun
        result["lunID"] = self.lun_id
        result["local"] = self.local
        return result


class BatchDeleteLUNInput:
    """An input object to delete multiple LUNs at once"""

    def __init__(
            self,
            volume_uuid: str,
            lun_uuids: [str] = None,
            host_uuids: [str] = None
    ):
        """Constructs a new input object to delete multiple LUNs

        Either ``lun_uuids`` or ``host_uuids`` must be specified, but not both.

        :param volume_uuid: The unique identifier of the volume from which the
            LUNs shall be deleted.
        :type volume_uuid: str
        :param lun_uuids: The list of LUN identifiers that shall be deleted. If
            ``host_uuids`` is not specified this parameter is mandatory.
        :type lun_uuids: [str], optional
        :param host_uuids: The list of host identifiers from which the LUNs
            shall be deleted. If ``lun_uuids`` is not specified this parameter
            is mandatory.
        :type host_uuids: [str], optional
        """

        self.__volume_uuid = volume_uuid
        self.__host_uuids = host_uuids
        self.__lun_uuids = lun_uuids

    @property
    def volume_uuid(self) -> str:
        """Identifier of the volume from which LUNs shall be deleted"""
        return self.__volume_uuid

    @property
    def host_uuids(self) -> [str]:
        """List of host identifiers from which LUNs shall be deleted"""
        return self.host_uuids

    @property
    def lun_uuids(self) -> [str]:
        """List of LUN identifiers that shall be deleted"""
        return self.__lun_uuids

    @property
    def as_dict(self):
        result = dict()
        result["lunUUIDs"] = self.lun_uuids
        result["volumeUUID"] = self.volume_uuid
        result["hostUUIDs"] = self.host_uuids
        return result


class LUN:
    """A LUN is an export of a volume to a host

    A LUN is an instance of a volume export that makes a volume accessible to
    a host.
    """

    def __init__(
            self,
            response: dict
    ):
        """Constructs a new LUN object

        This constructor expects a ``dict`` object from the nebulon ON API. It
        will check the returned data against the currently implemented schema
        of the SDK.

        :param response: The JSON response from the server
        :type response: dict

        :raises ValueError: An error if illegal data is returned from the server
        """

        self.__uuid = read_value(
            "uuid", response, str, True)
        self.__definition_uuid = read_value(
            "definitionUUID", response, str, True)
        self.__spu_serial = read_value(
            "spu.serial", response, str, True)
        self.__lun_id = read_value(
            "lunID", response, int, True)
        self.__volume_uuid = read_value(
            "volume.uuid", response, str, False)
        self.__host_uuid = read_value(
            "host.uuid", response, str, False)

    @property
    def uuid(self) -> str:
        """The unique identifier of the LUN"""
        return self.__uuid

    @property
    def definition_uuid(self) -> str:
        """The unique identifier of the central LUN definition"""
        return self.__definition_uuid

    @property
    def spu_serial(self) -> str:
        """The SPU serial where the LUN is exported from"""
        return self.__spu_serial

    @property
    def lun_id(self) -> int:
        """The LUN ID of the volume export"""
        return self.__lun_id

    @property
    def volume_uuid(self) -> str:
        """The unique identifier of the volume that is exported"""
        return self.__volume_uuid

    @property
    def host_uuid(self) -> str:
        """The unique identifier of the host the LUN is accessible by"""
        return self.__host_uuid

    @staticmethod
    def fields():
        return [
            "uuid",
            "definitionUUID",
            "spu{serial}",
            "host{uuid}",
            "lunID",
            "volume{uuid}",
        ]


class LUNList:
    """Paginated LUN list object

    Contains a list of LUN objects and information for pagination. By default a
    single page includes a maximum of ``100`` items unless specified otherwise
    in the paginated query.

    Consumers should always check for the property ``more`` as per default
    the server does not return the full list of alerts but only one page.
    """

    def __init__(
            self,
            response: dict
    ):
        """Constructs a new LUN list object

        This constructor expects a ``dict`` object from the nebulon ON API. It
        will check the returned data against the currently implemented schema
        of the SDK.

        :param response: The JSON response from the server
        :type response: dict

        :raises ValueError: An error if illegal data is returned from the server
        """
        self.__more = read_value(
            "more", response, bool, True)
        self.__total_count = read_value(
            "totalCount", response, int, True)
        self.__filtered_count = read_value(
            "filteredCount", response, int, True)
        self.__items = read_value(
            "items", response, LUN, True)

    @property
    def items(self) -> [LUN]:
        """List of LUN objects in the pagination list"""
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
            "items{%s}" % (",".join(LUN.fields())),
            "more",
            "totalCount",
            "filteredCount",
        ]


class LUNsMixin(NebMixin):
    """Mixin to add LUN related methods to the GraphQL client"""

    def get_luns(
            self,
            page: PageInput = None,
            lun_filter: LUNFilter = None,
            sort: LUNSort = None
    ) -> LUNList:
        """Retrieves a list of LUN objects

        :param page: The requested page from the server. This is an optional
            argument and if omitted the server will default to returning the
            first page with a maximum of ``100`` items.
        :type page: PageInput, optional
        :param lun_filter: A filter object to filter the LUNs on the
            server. If omitted, the server will return all objects as a
            paginated response.
        :type lun_filter: LUNFilter, optional
        :param sort: A sort definition object to sort the LUN objects
            on supported properties. If omitted objects are returned in the
            order as they were created in.
        :type sort: LUNSort, optional

        :returns LUNList: A paginated list of LUNs.

        :raises GraphQLError: An error with the GraphQL endpoint.
        """

        # setup query parameters
        parameters = dict()
        parameters["page"] = GraphQLParam(
            page, "PageInput", False)
        parameters["filter"] = GraphQLParam(
            lun_filter, "LUNFilter", False)
        parameters["sort"] = GraphQLParam(
            sort, "LUNSort", False)

        # make the request
        response = self._query(
            name="getLUNs",
            params=parameters,
            fields=LUNList.fields()
        )

        # convert to object
        return LUNList(response)

    def create_lun(
            self,
            lun_input: CreateLUNInput
    ) -> LUN:
        """Allows creation of a new LUN

        Allows the creation of a LUN for a volume. A LUN is an instance of a
        volume export that makes a volume accessible to a host.

        :param lun_input: The parameters that describe the LUN or LUNs to create
        :type lun_input: CreateLUNInput

        :returns LUN: the created LUN.

        :raises GraphQLError: An error with the GraphQL endpoint.
        """

        # setup query parameters
        parameters = dict()
        parameters["input"] = GraphQLParam(
            lun_input,
            "CreateLUNInput",
            True
        )

        # make the request
        response = self._mutation(
            name="createLUNV2",
            params=parameters,
            fields=TokenResponse.fields()
        )

        # convert to object and deliver token
        token_response = TokenResponse(response)
        delivery_response = token_response.deliver_token()

        # wait for recipe completion
        # TODO: Nebulon ON now returns a different response
        recipe_uuid = delivery_response["recipe_uuid_to_wait_on"]
        npod_uuid = delivery_response["npod_uuid_to_wait_on"]
        npod_recipe_filter = NPodRecipeFilter(
                npod_uuid=npod_uuid,
                recipe_uuid=recipe_uuid)

        # set a custom timeout for the create lun process
        start = datetime.now()

        while True:
            sleep(5)

            recipes = self.get_npod_recipes(npod_recipe_filter=npod_recipe_filter)

            # if there is no record in the cloud wait a few more seconds
            # this case should not exist, but is a safety measure for a
            # potential race condition
            if len(recipes.items) != 0:

                # based on the query there should be exactly one
                recipe = recipes.items[0]

                if recipe.state == RecipeState.Failed:
                    raise Exception(f"create lun failed: {recipe.status}")

                if recipe.state == RecipeState.Timeout:
                    raise Exception(f"create lun timeout: {recipe.status}")

                if recipe.state == RecipeState.Cancelled:
                    raise Exception(f"create lun cancelled: {recipe.status}")

                if recipe.state == RecipeState.Completed:
                    lun_list = self.get_luns(
                        lun_filter=LUNFilter(
                            npod_uuid=UUIDFilter(
                                equals=npod_uuid
                            ),
                            and_filter=LUNFilter(
                                volume_uuid=UUIDFilter(
                                    equals=lun_input.volume_uuid
                                ),
                                and_filter=LUNFilter(
                                    lun_id=IntFilter(
                                        equals=lun_input.lun_id
                                    )
                                )
                            )
                        )
                    )

                    if lun_list.filtered_count == 0:
                        break

                    return lun_list.items[0]

            # Wait time remaining until timeout
            total_duration = (datetime.now() - start).total_seconds()
            time_remaining = _TIMEOUT_SECONDS - total_duration

            if time_remaining <= 0:
                raise Exception("create lun timed out")

    def delete_lun(
            self,
            lun_uuid: str
    ):
        """Allows deletion of a LUN

        :param lun_uuid: The unique identifier of the LUN to delete
        :type lun_uuid: str

        :raises GraphQLError: An error with the GraphQL endpoint.
        """

        # setup query parameters
        parameters = dict()
        parameters["uuid"] = GraphQLParam(lun_uuid, "UUID", True)

        # make the request
        response = self._mutation(
            name="deleteLUN",
            params=parameters,
            fields=TokenResponse.fields()
        )

        # convert to object and deliver token
        token_response = TokenResponse(response)
        token_response.deliver_token()

    def delete_luns(
            self,
            batch_delete_lun_input: BatchDeleteLUNInput
    ):
        """Allows deletion of multiple LUNs simultaneously

        :param batch_delete_lun_input: An input parameter describing the
            selection criteria for the LUNs to delete.
        :type batch_delete_lun_input: BatchDeleteLUNInput


        :raises GraphQLError: An error with the GraphQL endpoint.
        """

        # setup query parameters
        parameters = dict()
        parameters["input"] = GraphQLParam(
            batch_delete_lun_input,
            "BatchDeleteLUNInput",
            True
        )

        # make the request
        response = self._mutation(
            name="batchDeleteLUN",
            params=parameters,
            fields=TokenResponse.fields()
        )

        # convert to object and deliver token
        token_response = TokenResponse(response)
        token_response.deliver_token()
