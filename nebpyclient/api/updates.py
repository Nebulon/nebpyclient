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
from .common import NebEnum, read_value, PageInput
from .issues import Issues
from .tokens import TokenResponse
from .sorting import SortDirection
from .filters import StringFilter

__all__ = [
    "NebPackagePriority",
    "NebPackageType",
    "PackageInfo",
    "RecommendedPackages",
    "AvailablePackagesSort",
    "AvailablePackagesFilter",
    "PackageInfoList",
    "UpdateStateSpu",
    "UpdateHistory",
    "UpdatesMixin",
    "NPodRecommendedPackage",
]


class NebPackagePriority(NebEnum):
    """Indicates the importance for installing a nebulon package"""

    Normal = "Normal"
    """Indicates a routine installation package"""

    Critical = "Critical"
    """Indicates a critical update"""


class NebPackageType(NebEnum):
    """Indicates the type of software package"""

    Base = "Base"
    """Baseline package that includes major changes to nebOS"""

    Patch = "Patch"
    """A patch package that resolves a specific issue with nebOS"""


class PackageSupportState(NebEnum):
    """Indicates the support state for a nebOS software package"""

    Supported = "Supported"
    """A supported software package"""

    EndOfSupport = "EndOfSupport"
    """A software package that is no longer receives active support"""


class AvailablePackagesSort:
    """A sort object for services processing units (SPU)

    Allows sorting SPUs on common properties. The sort object allows only one
    property to be specified.
    """

    def __init__(
            self,
            package_name: SortDirection = None,
            release_date: SortDirection = None,
    ):
        """Constructs a new sort object for SPUs

        Allows sorting software packages on common properties. The sort object
        allows only one property to be specified.

        :param package_name: Sort direction for the ``package_name`` property
        :type package_name: SortDirection, optional
        :param release_date: Sort direction for the ``release_date`` property
        :type release_date: SortDirection, optional
        """

        self.__package_name = package_name
        self.__release_date = release_date

    @property
    def package_name(self) -> SortDirection:
        """Sort direction for the ``serial`` property"""
        return self.__package_name

    @property
    def release_date(self) -> SortDirection:
        """Sort direction for the ``serial`` property"""
        return self.__release_date

    @property
    def as_dict(self):
        result = dict()
        result["packageName"] = self.package_name
        result["releaseDate"] = self.release_date
        return result


class AvailablePackagesFilter:
    """A filter object to filter software packages

    Allows filtering for specific software packages in nebulon ON. The
    filter allows only one property to be specified. If filtering on multiple
    properties is needed, use the ``and_filter`` and ``or_filter`` options to
    concatenate multiple filters.
    """

    def __init__(
            self,
            package_name: StringFilter = None,
            package_type: NebPackageType = None,
            package_priority: NebPackagePriority = None,
            and_filter=None,
            or_filter=None
    ):
        """Constructs a new filter object

        The filter allows only one property to be specified. If filtering on
        multiple properties is needed, use the ``and_filter`` and ``or_filter``
        options to concatenate multiple filters.

        :param package_name: Filter based on package name
        :type package_name: StringFilter, optional
        :param package_type: Filter by package type
        :type package_type: NebPackageType, optional
        :param package_priority: Filter by package priority
        :type package_priority: NebPackagePriority, optional
        :param and_filter: Concatenate another filter with a logical AND
        :type and_filter: SpuFilter, optional
        :param or_filter: Concatenate another filter with a logical OR
        :type or_filter: SpuFilter, optional
        """

        self.__package_name = package_name
        self.__package_type = package_type
        self.__package_priority = package_priority
        self.__and = and_filter
        self.__or = or_filter

    @property
    def package_name(self) -> StringFilter:
        """Filter based on package name"""
        return self.__package_name

    @property
    def package_type(self) -> NebPackageType:
        """Filter by package type"""
        return self.__package_type

    @property
    def package_priority(self) -> NebPackagePriority:
        """Filter by package priority"""
        return self.__package_priority

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
        result["packageName"] = self.package_name
        result["packageType"] = self.package_type
        result["packagePriority"] = self.package_priority
        result["and"] = self.and_filter
        result["or"] = self.or_filter
        return result


class PackageInfo:
    """A nebulon update package

    Represents a software bundle for nebulon services processing units
    and all related metadata. This information is used for updating
    nebulon services processing units to a specific nebOS version.
    """

    def __init__(
            self,
            response: dict
    ):
        """Constructs a new package information object

        This constructor expects a ``dict`` object from the nebulon ON API. It
        will check the returned data against the currently implemented schema
        of the SDK.

        :param response: The JSON response from the server
        :type response: dict

        :raises ValueError: An error if illegal data is returned from the server
        """
        self.__package_name = read_value(
            "packageName", response, str, True)
        self.__package_size_bytes = read_value(
            "packageSizeBytes", response, int, True)
        self.__release_notes_url = read_value(
            "releaseNotesURL", response, str, True)
        self.__prerequisites = read_value(
            "prerequisites", response, str, True)
        self.__package_description = read_value(
            "packageDescription", response, str, True)
        self.__package_type = read_value(
            "packageType", response, NebPackageType, True)
        self.__package_priority = read_value(
            "packagePriority", response, NebPackagePriority, True)
        self.__release_date = read_value(
            "releaseDate", response, datetime, True)
        self.__version_number = read_value(
            "versionNumber", response, str, True)
        self.__patch_number = read_value(
            "patchNumber", response, str, False)
        self.__support_state = read_value(
            "supportState", response, PackageSupportState, True)
        self.__lts_version = read_value(
            "longTermSupportVersion", response, bool, True)
        self.__offline = read_value(
            "offlineCheck", response, str, True)
        self.__eligible_npod_uuids = read_value(
            "eligibleNPods.uuid", response, str, False)

    @property
    def package_name(self) -> str:
        """The name of the nebulon update package"""
        return self.__package_name

    @property
    def package_size_bytes(self) -> int:
        """The size of the update package in bytes"""
        return self.__package_size_bytes

    @property
    def release_notes_url(self) -> str:
        """A URL to the release notes of the package"""
        return self.__release_notes_url

    @property
    def prerequisites(self) -> str:
        """Describes the prerequisites for the package"""
        return self.__prerequisites

    @property
    def package_description(self) -> str:
        """Description for the package"""
        return self.__package_description

    @property
    def package_type(self) -> NebPackageType:
        """Type of the nebOS installation package"""
        return self.__package_type

    @property
    def package_priority(self) -> NebPackagePriority:
        """Indicates the importance for installing a nebulon package"""
        return self.__package_priority

    @property
    def support_state(self) -> PackageSupportState:
        """Indicates the package's support state"""
        return self.__support_state

    @property
    def release_date(self) -> datetime:
        """The release date"""
        return self.__release_date

    @property
    def eligible_npod_uuids(self) -> [str]:
        """List of nPod unique identifiers that can install this package"""
        return self.__eligible_npod_uuids

    @property
    def version_number(self) -> str:
        """The version number if it is a nebOS package"""
        return self.__version_number

    @property
    def patch_number(self) -> str:
        """The patch number if it is a patch"""
        return self.__patch_number

    @property
    def lts_version(self) -> bool:
        """Indicates if the software package is under long-term support"""
        return self.__lts_version

    @property
    def offline(self) -> bool:
        """Indicates if the update is done offline"""
        return self.__offline

    @staticmethod
    def fields():
        return [
            "packageName",
            "packageSizeBytes",
            "releaseNotesURL",
            "prerequisites",
            "packageDescription",
            "packageType",
            "packagePriority",
            "releaseDate",
            "supportState",
            "longTermSupportVersion",
            "eligibleNPods{uuid}",
            "offlineCheck",
            "versionNumber",
            "patchNumber",
        ]


class NPodRecommendedPackage:
    """A nebulon update recommendation

    This information is used to indicate package installation recommendations
    for nPods.
    """

    def __init__(
            self,
            response: dict
    ):
        """Constructs a new nPod recommended package object

        This constructor expects a ``dict`` object from the nebulon ON API. It
        will check the returned data against the currently implemented schema
        of the SDK.

        :param response: The JSON response from the server
        :type response: dict

        :raises ValueError: An error if illegal data is returned from the
            server.
        """
        self.__package_name = read_value(
            "packageName", response, str, True)
        self.__priority = read_value(
            "priority", response, NebPackagePriority, True)
        self.__offline = read_value(
            "offline", response, bool, True)

    @property
    def package_name(self) -> str:
        """The name of the nebulon update package"""
        return self.__package_name

    @property
    def priority(self) -> NebPackagePriority:
        """The importance for installing the recommended package"""
        return self.__priority

    @property
    def offline(self) -> bool:
        """Indicates if the installation requires stopping I/O"""
        return self.__offline

    @staticmethod
    def fields():
        return [
            "packageName",
            "priority",
            "offline",
        ]


class RecommendedPackages:
    """Recommended packages for customers

    Recommended packages indicate the currently recommended packages for
    customers given their current version and hardware.
    """

    def __init__(
            self,
            response: dict
    ):
        """Constructs a new recommended packages object

        This constructor expects a ``dict`` object from the nebulon ON API. It
        will check the returned data against the currently implemented schema
        of the SDK.

        :param response: The JSON response from the server
        :type response: dict

        :raises ValueError: An error if illegal data is returned from the
            server.
        """
        self.__spu_type = read_value(
            "spuType", response, str, True)
        self.__base_version = read_value(
            "baseVersion", response, str, True)
        self.__package_name = read_value(
            "packageName", response, str, True)
        self.__package_info = read_value(
            "packageInfo", response, PackageInfo, False)

    @property
    def spu_type(self) -> str:
        """Indicates the type of SPU for which the package is recommended"""
        return self.__spu_type

    @property
    def base_version(self) -> str:
        """Indicates the base version for the recommended package"""
        return self.__base_version

    @property
    def package_name(self) -> str:
        """The name of the package that is recommended"""
        return self.__package_name

    @property
    def package_info(self) -> PackageInfo:
        """Information concerning the update package"""
        return self.__package_info

    @staticmethod
    def fields():
        return [
            "spuType",
            "baseVersion",
            "packageName",
            "packageInfo{%s}" % ",".join(PackageInfo.fields()),
        ]


class PackageInfoList:
    """Paginated software packages list

    Contains a list of software package objects and information for
    pagination. By default a single page includes a maximum of ``100`` items
    unless specified otherwise in the paginated query.

    Consumers should always check for the property ``more`` as per default
    the server does not return the full list of alerts but only one page.
    """
    def __init__(
            self,
            response: dict
    ):
        """Constructs a new update package list object

        This constructor expects a ``dict`` object from the nebulon ON API. It
        will check the returned data against the currently implemented schema
        of the SDK.

        :param response: The JSON response from the server
        :type response: dict

        :raises ValueError: An error if illegal data is returned from the
            server.
        """
        self.__items = read_value(
            "items", response, PackageInfo, True)
        self.__more = read_value(
            "more", response, bool, True)
        self.__total_count = read_value(
            "totalCount", response, int, True)
        self.__filtered_count = read_value(
            "filteredCount", response, int, True)

    @property
    def items(self) -> [PackageInfo]:
        """List of software packages in the pagination list"""
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
            "items{%s}" % ",".join(PackageInfo.fields()),
            "more",
            "totalCount",
            "filteredCount",
        ]


class UpdateStateSpu:
    """An object describing the current state of an update installation"""

    def __init__(
            self,
            response: dict
    ):
        """Constructs a new update status object

        This constructor expects a ``dict`` object from the nebulon ON API. It
        will check the returned data against the currently implemented schema
        of the SDK.

        :param response: The JSON response from the server
        :type response: dict

        :raises ValueError: An error if illegal data is returned from the
            server.
        """
        self.__update_id = read_value(
            "updateID", response, str, True)
        self.__spu_serial = read_value(
            "SPUSerial", response, str, True)
        self.__package_name = read_value(
            "packageName", response, str, True)
        self.__download_progress_pct = read_value(
            "downloadProgressPct", response, int, True)
        self.__waiting_for_spu_serial = read_value(
            "waitingForSPUSerial", response, str, True)
        self.__waiting_for_scheduled = read_value(
            "waitingForScheduled", response, datetime, False)
        self.__started_install = read_value(
            "startedInstall", response, bool, True)
        self.__restarting = read_value(
            "restarting", response, bool, True)
        self.__restart_complete = read_value(
            "restartComplete", response, bool, True)
        self.__failure_log = read_value(
            "failureLog", response, str, False)
        self.__last_changed = read_value(
            "lastChanged", response, datetime, True)

    @property
    def update_id(self) -> str:
        """The identifier of the update"""
        return self.__update_id

    @property
    def spu_serial(self) -> str:
        """The serial number for the SPU on which the update is installed"""
        return self.__spu_serial

    @property
    def package_name(self) -> str:
        """The name of the package that is installed"""
        return self.__package_name

    @property
    def download_progress_pct(self) -> int:
        """Download progress in percent"""
        return self.__download_progress_pct

    @property
    def waiting_for_spu_serial(self) -> str:
        """Indicates if the SPU is waiting for a SPU to complete its update"""
        return self.__waiting_for_spu_serial

    @property
    def waiting_for_scheduled(self) -> datetime:
        """Indicates that the SPU is waiting for a scheduled update"""
        return self.__waiting_for_scheduled

    @property
    def started_install(self) -> bool:
        """Indicates if the SPU has started installing the SPU"""
        return self.__started_install

    @property
    def restarting(self) -> bool:
        """Indicates if nebOS is restarting"""
        return self.__restarting

    @property
    def restart_complete(self) -> bool:
        """Indicates if nebOS has completed the restart"""
        return self.__restart_complete

    @property
    def failure_log(self) -> str:
        """Contains information about update errors"""
        return self.__failure_log

    @property
    def last_changed(self) -> datetime:
        """Date and time when the SPU last reported update status"""
        return self.__last_changed

    @staticmethod
    def fields():
        return [
            "updateID",
            "SPUSerial",
            "packageName",
            "downloadProgressPct",
            "waitingForSPUSerial",
            "waitingForScheduled",
            "startedInstall",
            "restarting",
            "restartComplete",
            "failureLog",
            "lastChanged",
        ]


class UpdateHistory:
    """An object describing past updates"""

    def __init__(
            self,
            response: dict
    ):
        """Constructs a new update history object

        This constructor expects a ``dict`` object from the nebulon ON API. It
        will check the returned data against the currently implemented schema
        of the SDK.

        :param response: The JSON response from the server
        :type response: dict

        :raises ValueError: An error if illegal data is returned from the
            server.
        """
        self.__update_id = read_value(
            "updateID", response, str, True)
        self.__package_name = read_value(
            "packageName", response, str, True)
        self.__start = read_value(
            "start", response, datetime, True)
        self.__finish = read_value(
            "finish", response, datetime, False)
        self.__success = read_value(
            "success", response, bool, True)

    @property
    def update_id(self) -> str:
        """The identifier of the update"""
        return self.__update_id

    @property
    def package_name(self) -> str:
        """The name of the package that is installed"""
        return self.__package_name

    @property
    def start(self) -> datetime:
        """Date and time when the update started"""
        return self.__start

    @property
    def finish(self) -> datetime:
        """Date and time when the update completed"""
        return self.__finish

    @property
    def success(self) -> bool:
        """Indicates if the update completed successfully"""
        return self.__success

    @staticmethod
    def fields():
        return [
            "updateID",
            "packageName",
            "start",
            "finish",
            "success",
        ]


class UpdatesMixin(NebMixin):
    """Mixin to add update related methods to the GraphQL client"""

    def get_available_packages(
            self,
            page: PageInput = None,
            available_packages_filter: AvailablePackagesFilter = None,
            sort: AvailablePackagesSort = None
    ) -> PackageInfoList:
        """Retrieves a list of update packages

        :param page: The requested page from the server. This is an optional
            argument and if omitted the server will default to returning the
            first page with a maximum of ``100`` items.
        :type page: PageInput, optional
        :param available_packages_filter: A filter object to filter the
            software packages on the server. If omitted, the server will
            return all objects as a paginated response.
        :type available_packages_filter: AvailablePackagesFilter, optional
        :param sort: A sort definition object to sort the software package
            objects on supported properties. If omitted objects are
            returned in the order as they were created in.
        :type sort: AvailablePackagesSort, optional

        :returns PackageInfoList: A paginated list of software packages

        :raises GraphQLError: An error with the GraphQL endpoint
        """

        # setup query parameters
        parameters = dict()
        parameters["page"] = GraphQLParam(
            page, "PageInput", False)
        parameters["filter"] = GraphQLParam(
            available_packages_filter, "AvailablePackagesFilter", False)
        parameters["sort"] = GraphQLParam(
            sort, "AvailablePackagesSort", False)

        # make the request
        response = self._query(
            name="getAvailablePackages",
            params=parameters,
            fields=PackageInfoList.fields()
        )

        # convert to object
        return PackageInfoList(response)

    def __run_update_precheck(
            self,
            npod_uuid: str,
            package_name: str
    ) -> Issues:
        """Runs diagnostics before an update is installed

        Ensures that an nPod is in a healthy state and that there are no issues
        preventing a successful update

        :param npod_uuid: The unique identifier of the nPod for which the
            update pre-check is performed
        :type npod_uuid: str
        :param package_name: The package name to be installed
        :type package_name: str

        :returns Issues: A list of warnings and errors discovered during the
            pre-check

        :raises GraphQLError: An error with the GraphQL endpoint.
        """

        # setup query parameters
        parameters = dict()
        parameters["podUID"] = GraphQLParam(
            npod_uuid, "String", True)
        parameters["packageName"] = GraphQLParam(
            package_name, "String", True)

        # make the request
        response = self._query(
            name="updatePrecheck",
            params=parameters,
            fields=Issues.fields()
        )

        # convert to object
        return Issues(response)

    def update_npod_firmware(
            self,
            npod_uuid: str,
            package_name: str,
            schedule_at: datetime = None,
            ignore_warnings: bool = False
    ):
        """Update nPod firmware to specified package

        :param npod_uuid: The unique identifier of the nPod to update
        :type npod_uuid: str
        :param package_name: The name of the package to install
        :type package_name: str
        :param schedule_at: Allows scheduling the installation of a package
            at the specified date and time. If omitted, the package will be
            installed immediately
        :type schedule_at: datetime, optional
        :param ignore_warnings: If specified warnings that are discovered
            during the update pre-check are ignored (not recommended). If 
            omitted or set to ``False`` will cause the update to stop.
        :type ignore_warnings: bool, optional

        :raises GraphQLError: An error with the GraphQL endpoint
        :raises Exception: If token delivery fails
        """

        # first run an update pre-check
        issues = self.__run_update_precheck(
            npod_uuid=npod_uuid,
            package_name=package_name
        )
        issues.assert_no_issues(ignore_warnings=ignore_warnings)

        # setup query parameters
        parameters = dict()
        parameters["podUID"] = GraphQLParam(
            npod_uuid, "String", True)
        parameters["packageName"] = GraphQLParam(
            package_name, "String", True)
        parameters["scheduled"] = GraphQLParam(
            schedule_at, "Time", False)

        # make the request
        response = self._mutation(
            name="updatePodFirmware",
            params=parameters,
            fields=TokenResponse.fields()
        )

        # convert to object and deliver token
        token_response = TokenResponse(response)
        token_response.deliver_token()

    def get_update_state(
            self,
            npod_uuid: str = None,
            update_uuid: str = None
    ) -> [UpdateStateSpu]:
        """Retrieves a list of active updates

        Allows querying for currently ongoing updates and their status
        information.

        :param npod_uuid: Filter active updates for a specific nPod by
            providing its unique identifier
        :type npod_uuid: str
        :param update_uuid: The unique identifier of an ongoing update
        :type update_uuid: str

        :returns [UpdateStateSpu]: A list of ongoing updates

        :raises GraphQLError: An error with the GraphQL endpoint.
        """

        # setup query parameters
        parameters = dict()
        parameters["podUID"] = GraphQLParam(
            npod_uuid, "String", False)
        parameters["updateID"] = GraphQLParam(
            update_uuid, "String", False)

        # make the request
        response = self._query(
            name="updateState",
            params=parameters,
            fields=UpdateStateSpu.fields()
        )

        # convert to object
        return [UpdateStateSpu(i) for i in response]

    def update_spu_firmware(
            self,
            spu_serial: str,
            package_name: str,
            force: bool = False
    ):
        """Update nebOS of a SPU to a specific package

        This method is executed asynchronously and does not wait for the
        update to complete.

        :param spu_serial: The serial number of the SPU to update
        :type spu_serial: str
        :param package_name: The name of the update package to install
        :type package_name: str
        :param force: If set to ``True`` the update will bypass any safeguards
        :type force: bool

        :raises GraphQLError: An error with the GraphQL endpoint.
        :raises Exception: If token delivery failed
        """

        # setup query parameters
        parameters = dict()
        parameters["serial"] = GraphQLParam(
            spu_serial, "String", True)
        parameters["packageName"] = GraphQLParam(
            package_name, "String", True)
        parameters["force"] = GraphQLParam(
            force, "Boolean", False)

        # make the request
        response = self._mutation(
            name="updateSPUFirmware",
            params=parameters,
            fields=TokenResponse.fields()
        )

        # convert to object
        token_response = TokenResponse(response)
        token_response.deliver_token()

    def abort_update_spu_firmware(
            self,
            spu_serial: str = None,
            npod_uuid: str = None
    ):
        """Abort an ongoing firmware update

        Either ``spu_serial`` or ``npod_uuid`` must be specified.

        :param spu_serial: The serial number of the SPU
        :type spu_serial: str, optional
        :param npod_uuid: The unique identifier of the nPod
        :type npod_uuid: str, optional

        :raises GraphQLError: An error with the GraphQL endpoint.
        :raises Exception: If token delivery failed
        """

        # setup query parameters
        parameters = dict()
        parameters["serial"] = GraphQLParam(
            spu_serial, "String", False)
        parameters["podUID"] = GraphQLParam(
            npod_uuid, "String", False)

        # make the request
        response = self._mutation(
            name="abortUpdateSPUFirmware",
            params=parameters,
            fields=TokenResponse.fields()
        )

        # convert to object
        token_response = TokenResponse(response)
        token_response.deliver_token()
