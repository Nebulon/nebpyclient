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

from datetime import datetime
from .graphqlclient import NebMixin, GraphQLParam
from .common import PageInput, read_value
from .filters import UUIDFilter
from .tokens import TokenResponse

__all__ = [
    "VSphereCredentialsMixin",
    "VsphereCredentialsList",
    "VsphereCredentialsFilter",
    "VsphereCredentials",
    "UpsertVsphereCredentialsInput"
]


class VsphereCredentialsFilter:
    """A filter object to filter vSphere credentials.

    Allows filtering for specific vSphere credentials in nebulon ON. The
    filter allows only one property to be specified. If filtering on multiple
    properties is needed, use the ``and_filter`` and ``or_filter`` options to
    concatenate multiple filters.
    """

    def __init__(
            self,
            npod_uuid: UUIDFilter = None,
            and_filter=None,
            or_filter=None,
    ):
        """Constructs a new filter object

        The filter allows only one property to be specified.If filtering on
        multiple properties is needed, use the ``and_filter`` and ``or_filter``
        options to concatenate multiple filters.

        :param npod_uuid: Filter based on nPod unique identifiers
        :type npod_uuid: UUIDFilter
        :param and_filter: Concatenate another filter with a logical AND
        :type and_filter: VsphereCredentialsFilter
        :param or_filter: Concatenate another filter with a logical OR
        :type or_filter: VsphereCredentialsFilter
        """
        self.__npod_uuid = npod_uuid
        self.__and = and_filter
        self.__or = or_filter

    @property
    def npod_uuid(self) -> UUIDFilter:
        """Filter for nPod unique identifier"""
        return self.__npod_uuid

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
        result["nPodUUID"] = self.npod_uuid
        result["and"] = self.and_filter
        result["or"] = self.or_filter
        return result


class UpsertVsphereCredentialsInput:
    """An input object to setup new vSphere credentials.

    Allows specifying login credentials for a vCenter server instance. This
    information is used by a nPod to retrieve diagnostics data from the
    vSphere cluster running on the nPod.
    """

    def __init__(
            self,
            username: str,
            password: str,
            url: str,
            insecure: bool = False,
            enable_vmhost_affinity: bool = False,
    ):
        """Constructs a new vSphere credentials object

        :param username: Username for vCenter login
        :type username: str
        :param password: Password for vCenter login
        :type password: str
        :param url: The URL for the vCenter server API in the form of
            https://<fqdn>:<port>, where ``fqdn`` can be a DNS name or an IP
            address. If the default HTTPS port (443) is used, then the
            port specification is not required.
        :type url: str
        :param insecure: Allow update if certificate is not valid
        :type insecure: bool, optional
        :param enable_vmhost_affinity: If provided and set to ``True`` the
            VMware vSphere integration will configure VM affinity rules to
            ensure that Virtual Machines are running on the host where
            the VM's datastore is local.
        :type enable_vmhost_affinity: bool, optional

        :raises GraphQLError: An error when calling the nebulon ON API
            ValueError: An error when mandatory arguments are not specified
        """

        self.__username = username
        self.__password = password
        self.__url = url
        self.__insecure = insecure
        self.__enable_vmhost_affinity = enable_vmhost_affinity

    @property
    def username(self) -> str:
        """vCenter login username"""
        return self.__username

    @property
    def password(self) -> str:
        """vCenter login password"""
        return self.__password

    @property
    def url(self) -> str:
        """vCenter server API URL"""
        return self.__url

    @property
    def insecure(self) -> bool:
        """Trust Certificate"""
        return self.__insecure

    @property
    def enable_vmhost_affinity(self) -> bool:
        """Enable automatic VM to Host affinity rule creation"""
        return self.__enable_vmhost_affinity

    @property
    def as_dict(self):
        result = dict()
        result["username"] = self.username
        result["password"] = self.password
        result["url"] = self.url
        result["insecure"] = self.insecure
        result["enableVmhostAffinity"] = self.enable_vmhost_affinity
        return result


class VsphereCredentials:
    """A vCenter credentials object

    Represents vCenter login information and status for nPod application
    integration. If defined, a nPod will use this information to collect
    diagnostics information from vCenter for troubleshooting and monitoring.

    """

    def __init__(
            self,
            response: dict
    ):
        """Constructs a new vCenter Credential object

        This constructor expects a ``dict`` object from the nebulon ON API. It
        will check the returned data against the currently implemented schema
        of the SDK.

        :param response: The JSON response from the server
        :type response: dict

        :raises ValueError: An error if illegal data is returned from the server
        """

        self.__npod_uuid = read_value(
            "nPod.uuid", response, str, False)
        self.__username = read_value(
            "username", response, str, True)
        self.__url = read_value(
            "URL", response, str, True)
        self.__polling_period_seconds = read_value(
            "pollingPeriodSec", response, int, True)
        self.__cluster_name = read_value(
            "clusterName", response, str, True)
        self.__last_connected = read_value(
            "lastConnected", response, datetime, False)
        self.__state_updated = read_value(
            "stateUpdated", response, datetime, True)
        self.__status = read_value(
            "status", response, str, True)
        self.__error = read_value(
            "error", response, str, True)
        self.__enable_vmhost_affinity = read_value(
            "enableVmhostAffinity", response, bool, True)

    @property
    def npod_uuid(self) -> str:
        """Unique identifier of the nPod"""
        return self.__npod_uuid

    @property
    def username(self) -> str:
        """vCenter login username"""
        return self.__username

    @property
    def url(self) -> str:
        """vCenter server API URL"""
        return self.__url

    @property
    def polling_period_seconds(self) -> int:
        """Specifies how often the nPod queries vCenter for information"""
        return self.__polling_period_seconds

    @property
    def cluster_name(self) -> str:
        """vCenter cluster name for the nPod"""
        return self.__cluster_name

    @property
    def last_connected(self) -> datetime:
        """Date and time when the nPod last connected to vCenter"""
        return self.__last_connected

    @property
    def state_updated(self) -> bool:
        """Date and time when the nPod last updated vCenter information"""
        return self.__state_updated

    @property
    def status(self) -> str:
        """Current vCenter integration status"""
        return self.__status

    @property
    def error(self) -> str:
        """Error message associated with the vCenter integration"""
        return self.__error

    @property
    def enable_vmhost_affinity(self) -> bool:
        """Automatic VM to Host affinity rule creation"""
        return self.__enable_vmhost_affinity

    @staticmethod
    def fields():
        return [
            "nPod{uuid}",
            "username",
            "URL",
            "pollingPeriodSec",
            "clusterName",
            "lastConnected",
            "stateUpdated",
            "status",
            "error",
            "enableVmhostAffinity",
        ]


class VsphereCredentialsList:
    """Paginated vCenter Credential information objects

    Contains a list of vCenter Credential objects and information for
    pagination. By default a single page includes a maximum of ``100`` items
    unless specified otherwise in the paginated query.
    """

    def __init__(
            self,
            response: dict
    ):
        """Constructs a new vCenter Credential list object

        This constructor expects a ``dict`` object from the nebulon ON API. It
        will check the returned data against the currently implemented schema
        of the SDK.

        Consumers should always check for the property ``more`` as per default
        the server only populates ``100`` items.

        :param response: The JSON response from the server
        :type response: dict

        :raises ValueError: An error if illegal data is returned from the server
        """
        self.__items = read_value(
            "items", response, VsphereCredentials, True)
        self.__more = read_value(
            "more", response, bool, True)
        self.__total_count = read_value(
            "totalCount", response, int, True)
        self.__filtered_count = read_value(
            "filteredCount", response, int, True)

    @property
    def items(self) -> [VsphereCredentials]:
        """List of vCenter credential information"""
        return self.__items

    @property
    def more(self) -> bool:
        """Indicates if there are more pages on the server"""
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
            "items{%s}" % ",".join(VsphereCredentials.fields()),
            "more",
            "totalCount",
            "filteredCount",
        ]


class VSphereCredentialsMixin(NebMixin):

    def get_vsphere_credentials(
            self,
            page: PageInput = None,
            credential_filter: VsphereCredentialsFilter = None
    ) -> VsphereCredentialsList:
        """Retrieves a list of vCenter credentials

        :param page: The requested page from the server. This is an optional
            argument and if omitted the server will default to returning the
            first page with a maximum of ``100`` items.
        :type page: PageInput, optional
        :param credential_filter: A filter object to filter the vSphere
            credentials on the server. If omitted, the server will return
            all objects as a paginated response.
        :type credential_filter: VsphereCredentialsFilter, optional

        :returns SpuList: A paginated list of vCenter credential entries.
            For security reasons, the passwords are not stored in nebulon
            ON and therefore not retrievable via the API even though they
            are set.

        Raises:
            GraphQLError: An error with the GraphQL endpoint.
        """

        # setup query parameters
        parameters = dict()
        parameters["page"] = GraphQLParam(
            page,
            "PageInput",
            False
        )
        parameters["filter"] = GraphQLParam(
            credential_filter,
            "VsphereCredsFilter",
            False
        )

        # make the request
        response = self._query(
            name="getVsphereCreds",
            params=parameters,
            fields=VsphereCredentialsList.fields()
        )

        # convert to object
        return VsphereCredentialsList(response)

    def set_vsphere_credentials(
            self,
            npod_uuid: str,
            credentials_input: UpsertVsphereCredentialsInput
    ) -> bool:
        """Sets vCenter credentials for the provided nPod

        :param npod_uuid: Unique identifier of the nPod
        :type npod_uuid: str
        :param credentials_input: An input object describing the
            credentials to configure for the provided nPod
        :type credentials_input: UpsertVsphereCredentialsInput

        :returns bool: If the request was successful

        :raises GraphQLError: An error with the GraphQL endpoint.
        :raises Exception: An error when delivering a token to the SPU
        """

        # setup query parameters
        parameters = dict()
        parameters["nPodUUID"] = GraphQLParam(
            npod_uuid,
            "UUID",
            True
        )
        parameters["input"] = GraphQLParam(
            credentials_input,
            "UpsertVsphereCredsInput",
            True
        )

        # make the request
        response = self._mutation(
            name="upsertVsphereCredsV2",
            params=parameters,
            fields=TokenResponse.fields()
        )

        token_response = TokenResponse(response)
        return token_response.deliver_token()

    def delete_vsphere_credentials(
            self,
            npod_uuid: str
    ) -> bool:
        """Removes the vCenter credentials from the provided nPod

        :param npod_uuid: Unique identifier of the nPod
        :type npod_uuid: str

        Returns:
            A boolean that indicates if the request was successfully sent
            to the services processing unit.

        :returns bool: If the request was successful

        :raises GraphQLError: An error with the GraphQL endpoint.
        :raises Exception: An error when delivering a token to the SPU
        """

        # setup query parameters
        parameters = dict()
        parameters["nPodUUID"] = GraphQLParam(
            npod_uuid,
            "UUID",
            True
        )

        # make the request
        response = self._mutation(
            name="deleteVsphereCredsV2",
            params=parameters,
            fields=TokenResponse.fields()
        )

        token_response = TokenResponse(response)
        return token_response.deliver_token()
