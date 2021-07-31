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
from .common import ResourceType, read_value
from .filters import StringFilter


class KeyValueFilter:
    """A filter object to filter key value objects.

    Allows filtering for specific key value objects in nebulon ON. The
    filter allows only one property to be specified. If filtering on multiple
    properties is needed, use the ``and_filter`` and ``or_filter`` options to
    concatenate multiple filters.
    """

    def __init__(
            self,
            resource_type: ResourceType,
            npod_uuid: str,
            resource_uuid: str,
            key: StringFilter = None
    ):
        """Constructs a new filter object

        :param resource_type: Filter based on the associated resource type
        :type resource_type: ResourceType
        :param npod_uuid: Filter based on the associated nPod UUID
        :type npod_uuid: str
        :param resource_uuid: Filter based on the associated resource UUID
        :type resource_uuid: str
        :param key: Filter based on the key name
        :type key: StringFilter, optional
        """
        self.__resource_type = resource_type
        self.__npod_uuid = npod_uuid
        self.__resource_uuid = resource_uuid
        self.__key = key

    @property
    def resource_type(self) -> ResourceType:
        """Filter based on the associated resource type"""
        return self.__resource_type

    @property
    def npod_uuid(self) -> str:
        """Filter based on the associated nPod UUID"""
        return self.__npod_uuid

    @property
    def resource_uuid(self) -> str:
        """Filter based on the associated resource UUID"""
        return self.__resource_uuid

    @property
    def key(self) -> StringFilter:
        """Filter based on the key name"""
        return self.__key

    @property
    def as_dict(self):
        result = dict()
        result["resourceType"] = self.resource_type
        result["nPodUUID"] = self.npod_uuid
        result["resourceUUID"] = self.resource_uuid
        result["keyName"] = self.key
        return result


class UpsertKeyValueInput:
    """An input object to create or update a key value entry

    Allows adding metadata to various resources in nebulon ON in the form of
    key value pairs. This metadata can be used by customers to add arbitrary
    text information to resources that are not part of the default resource
    properties.
    """

    def __init__(
            self,
            resource_type: ResourceType,
            npod_uuid: str,
            resource_uuid: str,
            key: str,
            value: str
    ):
        """Constructs a new input object to create or update a key value entry

        :param resource_type: Type of resource for the key value data
        :type resource_type: ResourceType
        :param npod_uuid: nPod identifier.
        :type npod_uuid: str
        :param resource_uuid: Identifier of the resource for the key value entry
        :type resource_uuid: str
        :param key: Metadata key
        :type key: str
        :param value: Metadata value
        :type value: str
        """

        self.__resource_type = resource_type
        self.__npod_uuid = npod_uuid
        self.__resource_uuid = resource_uuid
        self.__key = key
        self.__value = value

    @property
    def resource_type(self) -> ResourceType:
        """Type of resource for the key value data"""
        return self.__resource_type

    @property
    def npod_uuid(self) -> str:
        """nPod identifier"""
        return self.__npod_uuid

    @property
    def resource_uuid(self) -> str:
        """Identifier of the resource for the key value entry"""
        return self.__resource_uuid

    @property
    def key(self) -> str:
        """Metadata key"""
        return self.__key

    @property
    def value(self) -> str:
        """Metadata value"""
        return self.__value

    @property
    def as_dict(self):
        result = dict()
        result["resourceType"] = self.resource_type
        result["nPodUUID"] = self.npod_uuid
        result["resourceUUID"] = self.resource_uuid
        result["key"] = self.key
        result["value"] = self.value
        return result


class DeleteKeyValueInput:
    """An input object to delete a key value entry"""

    def __init__(
            self,
            resource_type: ResourceType,
            npod_uuid: str,
            resource_uuid: str,
            key: str
    ):
        """Constructs a new input object to create or update a key value entry

        :param resource_type: Type of resource for the key value data
        :type resource_type: ResourceType
        :param npod_uuid: nPod identifier
        :type npod_uuid: str
        :param resource_uuid: Identifier of the resource for the key value entry
        :type resource_uuid: str
        :param key: Metadata key
        :type key: str
        """
        self.__resource_type = resource_type
        self.__npod_uuid = npod_uuid
        self.__resource_uuid = resource_uuid
        self.__key = key

    @property
    def resource_type(self) -> ResourceType:
        """Type of resource for the key value data"""
        return self.__resource_type

    @property
    def npod_uuid(self) -> str:
        """nPod identifier"""
        return self.__npod_uuid

    @property
    def resource_uuid(self) -> str:
        """Identifier of the resource for the key value entry"""
        return self.__resource_uuid

    @property
    def key(self) -> str:
        """Metadata key"""
        return self.__key

    @property
    def as_dict(self):
        result = dict()
        result["resourceType"] = self.resource_type
        result["nPodUUID"] = self.npod_uuid
        result["resourceUUID"] = self.resource_uuid
        result["key"] = self.key
        return result


class KeyValue:
    """Key value pair

    Represents metadata assigned to various resources in nebulon ON in the form
    of key value pairs. This metadata can be used by customers to add arbitrary
    text information to resources that are not part of the default resource
    properties
    """

    def __init__(
            self,
            response: dict
    ):
        """Constructs a new key value object

        This constructor expects a ``dict`` object from the nebulon ON API. It
        will check the returned data against the currently implemented schema
        of the SDK.

        :param response: The JSON response from the server
        :type response: dict

        :raises ValueError: An error if illegal data is returned from the server
        """

        self.__key = read_value(
            "key", response, str, True)
        self.__value = read_value(
            "value", response, str, True)

    @property
    def key(self) -> str:
        """Metadata key"""
        return self.__key

    @property
    def value(self) -> str:
        """Metadata value"""
        return self.__value

    @staticmethod
    def fields():
        return [
            "key",
            "value",
        ]


class KeyValueList:
    """List of key value pairs"""

    def __init__(
            self,
            response: dict
    ):
        """Constructs a new key value list object

        This constructor expects a ``dict`` object from the nebulon ON API. It
        will check the returned data against the currently implemented schema
        of the SDK.

        :param response: The JSON response from the server
        :type response: dict

        :raises ValueError: An error if illegal data is returned from the server
        """

        self.__total_count = read_value(
            "totalCount", response, int, True)
        self.__filtered_count = read_value(
            "filteredCount", response, int, True)
        self.__items = read_value(
            "items", response, KeyValue, True)

    @property
    def items(self) -> [KeyValue]:
        """List of key-value objects in the list"""
        return self.__items

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
            "items{%s}" % (",".join(KeyValue.fields())),
            "totalCount",
            "filteredCount",
        ]


class KeyValueMixin(NebMixin):
    """Mixin to add key value related methods to the GraphQL client"""

    def get_key_values(
            self,
            key_value_filter: KeyValueFilter
    ) -> KeyValueList:
        """Retrieves a list of key value objects

        :param key_value_filter: A filter object to filter key value objects on
            the server.
        :type key_value_filter: KeyValueFilter

        :returns KeyValueList: A list of key value objects.

        :raises GraphQLError: An error with the GraphQL endpoint.
        """

        # setup query parameters
        parameters = dict()
        parameters["filter"] = GraphQLParam(
            key_value_filter,
            "KeyValueFilter",
            True
        )

        # make the request
        response = self._query(
            name="getKeyValues",
            params=parameters,
            fields=KeyValueList.fields()
        )

        # convert to object
        return KeyValueList(response)

    def set_key_value(
            self,
            upsert_key_value_input: UpsertKeyValueInput
    ) -> bool:
        """Set a key value entry for a resource

        Allows adding metadata to various resources in nebulon ON in the form of
        key value pairs. This metadata can be used by customers to add arbitrary
        text information to resources that are not part of the default resource
        properties.

        :param upsert_key_value_input: Input parameters to create a new
            key/value pair of update an existing one.
        :type upsert_key_value_input: UpsertKeyValueInput

        :returns bool: Indicator if the query was successful.

        :raises GraphQLError: An error with the GraphQL endpoint.
        """

        # setup query parameters
        parameters = dict()
        parameters["input"] = GraphQLParam(
            upsert_key_value_input,
            "UpsertKeyValueInput",
            True
        )

        # make the request
        response = self._mutation(
            name="upsertKeyValue",
            params=parameters,
            fields=None
        )

        # response is a bool
        return response

    def delete_key_value(
            self,
            delete_key_value_input: DeleteKeyValueInput
    ) -> bool:
        """Remove a key value entry from a resource

        :param delete_key_value_input: Input parameter that identifies which
            key/value pair to delete
        :type delete_key_value_input: DeleteKeyValueInput

        :returns bool: Indicator if the query was successful.

        :raises GraphQLError: An error with the GraphQL endpoint.
        """

        # setup query parameters
        parameters = dict()
        parameters["input"] = GraphQLParam(
            delete_key_value_input,
            "DeleteKeyValueInput",
            True
        )

        # make the request
        response = self._mutation(
            name="deleteKeyValue",
            params=parameters,
            fields=None
        )

        # response is a bool
        return response
