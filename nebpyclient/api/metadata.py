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

from .common import read_value
from .. import NebMixin


class MetaValue:
    """Metadata information that describes API options"""

    def __init__(
            self,
            response: dict
    ):
        """Constructs a new MetaValue object

        This constructor expects a ``dict`` object from the nebulon ON API. It
        will check the returned data against the currently implemented schema
        of the SDK.

        :param response: The JSON response from the server
        :type response: dict

        :raises ValueError: An error if illegal data is returned from the server
        """
        self.__actual = read_value(
            "actual", response, str, True)
        self.__description = read_value(
            "description", response, str, True)

    @property
    def actual(self) -> str:
        """Actual value"""
        return self.__actual

    @property
    def description(self) -> str:
        """Description of the value"""
        return self.__description

    @staticmethod
    def fields():
        return [
            "actual",
            "description"
        ]


class RBACMetadata:
    """Metadata information for role-based access control"""

    def __init__(
            self,
            response: dict
    ):
        """Constructs a new RBACMetadata list object

        This constructor expects a ``dict`` object from the nebulon ON API. It
        will check the returned data against the currently implemented schema
        of the SDK.

        :param response: The JSON response from the server
        :type response: dict

        :raises ValueError: An error if illegal data is returned from the server
        """

        self.__resource_types = read_value(
            "resourceTypes", response, MetaValue, True)
        self.__permissions = read_value(
            "permissions", response, MetaValue, True)

    @property
    def resource_types(self) -> [MetaValue]:
        """List of possible resource types"""
        return self.__resource_types

    @property
    def permissions(self) -> [MetaValue]:
        """List possible permissions"""
        return self.__permissions

    @staticmethod
    def fields():
        return [
            "resourceTypes{%s}" % ",".join(MetaValue.fields()),
            "permissions{%s}" % ",".join(MetaValue.fields()),
        ]


class Metadata:
    """Metadata information that describes resources in the nebulon ON API"""

    def __init__(
            self,
            response: dict
    ):
        """Constructs a new Metadata object

        This constructor expects a ``dict`` object from the nebulon ON API. It
        will check the returned data against the currently implemented schema
        of the SDK.

        :param response: The JSON response from the server
        :type response: dict

        :raises ValueError: An error if illegal data is returned from the server
        """
        self.__rbac = read_value(
            "rbac", response, RBACMetadata, False)

    @property
    def rbac(self) -> RBACMetadata:
        """Metadata information for role-based access control"""
        return self.__rbac

    @staticmethod
    def fields():
        return [
            "rbac{%s}" % ",".join(RBACMetadata.fields()),
        ]


class MetadataMixin(NebMixin):
    """Mixin to add metadata related methods to the GraphQL client"""

    def get_metadata(self) -> Metadata:
        """Retrieves metadata information describing the nebulon ON API

        :returns Metadata: Metadata information object that describes various
            aspects of the nebulon ON API

        :raises GraphQLError: An error with the GraphQL endpoint.
        """

        # make the request
        response = self._query(
            name="getMetadata",
            fields=Metadata.fields()
        )

        # convert to object
        return Metadata(response)
