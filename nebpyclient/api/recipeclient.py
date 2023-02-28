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
from time import sleep
from datetime import datetime
from typing import Any, Dict, List
from .graphqlclient import NebMixin
from .recipe import NPodRecipeFilter, RecipeState
from .constants import RECIPE_TIMEOUT_SECONDS


class RecipeClient(NebMixin):
    """Used to handle interactions with Nebulon Recipes."""

    def _is_recipe_completed(
        self,
        npod_recipe_filter: NPodRecipeFilter,
        mutation_name: str,
    ) -> bool:
        """
        :param npod_recipe_filter: A filter object to filter recipes
        :type npod_recipe_filter: NPodRecipeFilter
        :param mutation_name: The name of the mutation that was used to initiate the recipe.
        :type mutation_name: str

        :returns bool: True if recipe was completed, False if recipe still pending.

        :raises GraphQLError: An error with the GraphQL endpoint.
        :raises Exception: An Exception if the recipe's status was not completed.
        """

        recipes = self.get_npod_recipes(npod_recipe_filter=npod_recipe_filter)

        # if there is no record in the cloud return false
        # and wait a few more seconds in the callee function.
        # this case should not exist, but is a safety measure for a
        # potential race condition
        if len(recipes.items) == 0:
            return False

        # based on the query there should be exactly one
        recipe = recipes.items[0]

        if recipe.state == RecipeState.Failed:
            raise Exception(f"{mutation_name} failed: {recipe.status}")

        if recipe.state == RecipeState.Timeout:
            raise Exception(f"{mutation_name} timeout: {recipe.status}")

        if recipe.state == RecipeState.Cancelled:
            raise Exception(f"{mutation_name} cancelled: {recipe.status}")

        if recipe.state == RecipeState.Completed:
            return True

        return False

    def _wait_on_single_recipe(
        self,
        npod_recipe_filter: NPodRecipeFilter,
        mutation_name: str,
    ):
        """
        :param npod_recipe_filter: A filter object to filter recipes
        :type npod_recipe_filter: NPodRecipeFilter
        :param mutation_name: The name of the mutation that was used to initiate the recipe.
        :type mutation_name: str

        :raises GraphQLError: An error with the GraphQL endpoint.
        :raises Exception: An Exception if the recipe's status was not completed.
        """
        # set a custom timeout for the update nPod members process
        start = datetime.now()

        while True:
            sleep(5)

            if self._is_recipe_completed(npod_recipe_filter, mutation_name):
                return

            # Wait time remaining until timeout
            total_duration = (datetime.now() - start).total_seconds()
            time_remaining = RECIPE_TIMEOUT_SECONDS - total_duration

            if time_remaining <= 0:
                raise Exception(f"{mutation_name} members timed out")

    def _wait_on_multiple_recipes(
        self,
        delivery_responses: List[Dict[str, str]],
        mutation_name: str
    ):
        """
        :param delivery_responses: A list of token delivery responses from SPUs.
        :type delivery_responses: List
        :param mutation_name: The name of the mutation that was used to initiate the recipes
        :type mutation_name: str

        :raises GraphQLError: An error with the GraphQL endpoint.
        :raises Exception: An Exception if any of the recipe statuses were not completed.
        """
        exception_list = list()
        start = datetime.now()
        while delivery_responses:
            sleep(5)
            for dr in delivery_responses:
                recipe_uuid = dr["recipe_uuid_to_wait_on"]
                npod_uuid = dr["npod_uuid_to_wait_on"]
                npod_recipe_filter = NPodRecipeFilter(
                        npod_uuid=npod_uuid,
                        recipe_uuid=recipe_uuid)
                
                recipe_state = False
                try:
                    recipe_state = self._is_recipe_completed(npod_recipe_filter, mutation_name)

                except Exception as e:
                    # Collect the exceptions in a list to raise an error on all the
                    # failed recipes in the end.
                    exception_list.append(e.args[0])
                    try:
                        delivery_responses.remove(dr)
                    except Exception as e:
                        pass
                
                if recipe_state:
                    try:
                        delivery_responses.remove(dr)
                    except Exception as e:
                        pass

                # Wait time remaining until timeout
                total_duration = (datetime.now() - start).seconds
                time_remaining = RECIPE_TIMEOUT_SECONDS - total_duration

                if time_remaining <= 0:
                    error_msg = f"{mutation_name} for recipe uuid: {recipe_uuid}, npod uuid: {npod_uuid}  timed out"
                    exception_list.append(error_msg)
                    try:
                        delivery_responses.remove(dr)
                    except Exception as e:
                        pass
        
        if exception_list:
            exception_msgs = "\n".join(exception_list)
            raise Exception(exception_msgs)
        
        return
    
    def _wait_on_recipes(
        self,
        delivery_response: Dict[str, Any],
        mutation_name: str,
    ):
        """
        :param delivery_response: A dictionary of different token responses
        :type delivery_response: Dict
        :param mutation_name: The name of the mutation that was used to initiate recipes
        :type mutation_name: str

        :raises GraphQLError: An error with the GraphQL endpoint.
        :raises Exception: An Exception if any of the recipe statuses were not completed.
        """
        recipe_uuid = delivery_response["recipe_uuid_to_wait_on"]
        npod_uuid = delivery_response["npod_uuid_to_wait_on"]
        delivery_responses = delivery_response["individual_recipes"]
        
        # If recipe_uuid and npod_uuid are empty
        # Then this recipe was sent to multiple SPUs
        # So we should wait on completion of delivery_responses
        if recipe_uuid != "" and npod_uuid != "":
            npod_recipe_filter = NPodRecipeFilter(
                    npod_uuid=npod_uuid,
                    recipe_uuid=recipe_uuid
            )
            self._wait_on_single_recipe(npod_recipe_filter, mutation_name)
        
        if delivery_responses:
            self._wait_on_multiple_recipes(delivery_responses, mutation_name)