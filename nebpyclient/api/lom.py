#
# Copyright 2022 Nebulon, Inc.
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

from .graphqlclient import NebMixin, GraphQLParam
from .tokens import TokenResponse

__all__ = [
    "LomCredentialsMixin",
    "UpsertLomCredentialsInput",
    "DeleteLomCredentialsInput",
]


class UpsertLomCredentialsInput:
    """An input to setup new Lights Out Management (LOM) credentials.

    Allows configuration of the Lights Out Management information for a host.
    This is used for controlling server power status and server inventory.
    Sensitive information is stored in encrypted formats on Services
    Processing Units in customers data centers only.
    """

    def __init__(
        self,
        host_uuid: str,
        username: str,
        password: str,
        url: str,
        insecure: bool = False,
    ):
        """ Construct a new LOM credentials input object

        Allows configuration of the Lights Out Management information for a
        host. This is used for controlling server power status and server
        inventory. Sensitive information is stored in encrypted formats on
        Services Processing Units in customers data centers only.

        :param host_uuid: The unique identifier of the host for which to
            configure the LOM credentials. This must be the UUID of a
            host that is already registed with an organization.
        :type host_uuid: str
        :param username: The username that the LOM integration uses for
            interacting with the server. The permissions of the user control
            the available features of the integration.
        :type username: str
        :param password: The password for the specified username
        :type password: str
        :param url: The URL of the host's LOM network interface in the
            format ``https://<fqdn|ip>``.
        :type url: str
        :param insecure: If set to ``True`` allows insecure connections to the
            host's LOM. This is useful when using self-signed or insecure
            certificates on the host's LOM interface.
        :type insecure: bool, optional
        """

        self.__host_uuid = host_uuid
        self.__username = username
        self.__password = password
        self.__url = url
        self.__insecure = insecure

    @property
    def host_uuid(self) -> str:
        """The unique identifier of the host"""
        return self.__host_uuid

    @property
    def username(self) -> str:
        """The username to use for authentication with the LOM"""
        return self.__username

    @property
    def password(self) -> str:
        """The password to use for authentication with the LOM"""
        return self.__password

    @property
    def url(self) -> str:
        """The URL of the host's LOM network interface"""
        return self.__url

    @property
    def insecure(self) -> bool:
        """Allow insecure connections"""
        return self.__insecure

    @property
    def as_dict(self):
        result = dict()
        result["hostUUID"] = self.host_uuid
        result["username"] = self.username
        result["password"] = self.password
        result["url"] = self.url
        result["insecure"] = self.insecure
        return result


class DeleteLomCredentialsInput:
    """An input object to delete Lights Out Management (LOM) credentials"""

    def __init__(
        self,
        host_uuid: str,
    ):
        """Construct a new Delete LOM credentials input object

        Allows removing the Lights Out Management information that is stored
        for the provided host. This will clear any LOM information on SPUs and
        disable any feature integration with the server, including power
        management and inventory.

        :param host_uuid: The unique identifier of the host for which to
            remove the LOM credentials. This must be the UUID of a
            host that has configured LOM credentials.
        :type host_uuid: str
        """
        self.__host_uuid = host_uuid

    @property
    def host_uuid(self) -> str:
        """The unique identifier of the host"""
        return self.__host_uuid

    @property
    def as_dict(self):
        result = dict()
        result["hostUUID"] = self.host_uuid
        return result


class LomCredentialsMixin(NebMixin):
    def upsert_lom_credentials(
        self,
        lom_credentials_input: UpsertLomCredentialsInput,
            ignore_warnings: bool = False,
    ) -> bool:
        """Set LOM credentials for a host

        Allows configuration of the Lights Out Management information for a
        host. Once credentials are configured, the server management features
        are enabled, controlling server power status and server inventory.

        Sensitive information is stored in encrypted formats on Services
        Processing Units in customers data centers only.

        :param lom_credentials_input: An input object describing the
            credentials to configure.
        :type lom_credentials_input: UpsertLomCredentialsInput
        :param ignore_warnings: If specified and set to ``True`` the operation 
            will proceed even if nebulon ON reports warnings. It is
            advised to not ignore warnings. Consequently, the default behavior
            is that the operation will fail when nebulon ON reports
            validation errors or warnings.
        :type ignore_warnings: bool, optional

        :returns bool: If the request was successful.

        :raises GraphQLError: An error with the GraphQL endpoint.
        :raises Exception: An error when delivering a token to the SPU.
        """

        # setup query parameters
        parameters = dict()
        parameters["input"] = GraphQLParam(
            lom_credentials_input,
            "UpsertLomCredentialsInput",
            True,
        )

        # make the request
        mutation_name="upsertLomCredentials"
        response = self._mutation(
            name=mutation_name,
            params=parameters,
            fields=TokenResponse.fields(),
        )

        token_response = TokenResponse(
            response=response,
            ignore_warnings=ignore_warnings,
        )
        delivery_response = token_response.deliver_token()

        # wait for recipe completion
        self._wait_on_recipes(delivery_response, mutation_name)

    def delete_lom_credentials(
        self,
        delete_lom_credentials_input: DeleteLomCredentialsInput,
        ignore_warnings: bool = False,
    ) -> bool:
        """Removes LOM credentials for a host

        Allows removing the Lights Out Management information that is stored
        for the provided host. This will clear any LOM information for the
        provided host on any SPU and disable any feature integration with the
        server, including power management and inventory.

        :param delete_lom_credentials_input: An input object describing the
            credentials to remove.
        :type delete_lom_credentials_input: DeleteLomCredentialsInput
        :param ignore_warnings: If specified and set to ``True`` the operation 
            will proceed even if nebulon ON reports warnings. It is
            advised to not ignore warnings. Consequently, the default behavior
            is that the operation will fail when nebulon ON reports
            validation errors or warnings.
        :type ignore_warnings: bool, optional

        :return bool: If the request was successful.

        :raises GraphQLError: An error with the GraphQL endpoint.
        :raises Exception: An error when delivering a token to the SPU.
        """

        # setup query parameters
        parameters = dict()
        parameters["input"] = GraphQLParam(
            delete_lom_credentials_input,
            "DeleteLomCredentialsInput",
            True,
        )

        # make the request
        mutation_name="deleteLomCredentials"
        response = self._mutation(
            name=mutation_name,
            params=parameters,
            fields=TokenResponse.fields(),
        )

        token_response = TokenResponse(
            response=response,
            ignore_warnings=ignore_warnings,
        )
        delivery_response = token_response.deliver_token()

        # wait for recipe completion
        self._wait_on_recipes(delivery_response, mutation_name)
