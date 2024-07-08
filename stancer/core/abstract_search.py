# -*- coding: utf-8 -*-

import json

from abc import ABC
from abc import abstractmethod
from datetime import datetime
from time import time

from ..exceptions import InvalidSearchFilter
from ..exceptions import InvalidSearchResponse
from ..exceptions import NotFoundError
from .request import Request

# This code is a Hack to let us use Self from typing if available, else we use TypeVar
try:
    # Self is available in Python 3.11
    from typing import Self  # type: ignore
except ImportError:
    from typing import TypeVar

    Self = TypeVar('Self', bound='AbstractSearch')  # type: ignore


class AbstractSearch(ABC):
    """Common search method."""

    @classmethod
    def filter_list_params(cls, **kwargs) -> dict:  # pylint: disable=unused-argument
        """
        Filter for list method.

        This method should be overrided in child object.

        Args:
            kwargs: Arbitrary keyword argument to filter.

        Returns:
            Filtered arguments.
        """
        return {}

    @classmethod
    def validate_order_id_params(cls,order_id: any, max_length: int, base_message: str) -> str:
        """
        Filter Order ids.
        as it is a common params we add it to not reimplement it on all class

        Args:
            order_id: A string representing order_id

        Returns:
            The validated order_id

        Raises:
            InvalidSearchFilter if the order_id isn't a valid order_id
        """
        if not isinstance(order_id, str):
            raise InvalidSearchFilter('Order ID must be a string.')

        length = len(order_id)

        if length > max_length or not length:
            raise InvalidSearchFilter(base_message.format('order ID', 1, max_length))
        return order_id

    @classmethod
    def validate_order_params(cls,order:any) -> str:
        """
        Filter Order parameter.

        Args:
            order: A string defining the order of our list

        Returns:
            The order of our list (validated)

        Raises:
            InvalidSearchFilter if the order isn't either asc or desc
        """
        if not ( isinstance(order, str) and order in ('asc', 'desc' )):
            raise InvalidSearchFilter("Order must be 'desc' or 'asc'.")

        return order


    @abstractmethod
    def hydrate(self: Self, **params) -> Self:
        """
        Hydrate current object.

        Args:
            **params: Elements used to hydrate the object.
                Every key matching an object property will be used.

        Returns:
            Current instance.
        """

    @classmethod
    def get_param(
        cls,
        created: int | float | datetime | None = None,
        limit: int | None = None,
        start: int | None = None,
        **kwargs,
    ) -> dict:
        """
        Create the parameters for the listing,

        Args:
            created: must be an unix timestamp or a datetime object which will
                filter payments equal to or greater than this value.
            limit: must be an integer between 1 and 100 and will limit the number of
                objects to be returned.
            start: must be an integer, will be used as a pagination cursor,
                starts at 0.
            kwargs: Arbitrary keyword argument.
        Returns:
            dict.

        """
        params = cls.filter_list_params(**kwargs)
        if created is not None:
            if isinstance(created, datetime):
                created = created.timestamp()

            if isinstance(created, float):
                created = int(created)

            if not isinstance(created, int) or created < 0:
                message = "Created must be a position integer or a DateTime object."

                raise InvalidSearchFilter(message)

            if created > time():
                raise InvalidSearchFilter("Created must be in the past.")

            params["created"] = created

        if limit is not None:
            if not isinstance(limit, int) or limit < 1 or limit > 100:
                raise InvalidSearchFilter("Limit must be between 1 and 100.")

            params["limit"] = limit

        if start is not None:
            if not isinstance(start, int) or start < 0:
                raise InvalidSearchFilter("Start must be a positive integer.")

            params["start"] = start
        return params

    @staticmethod
    def _create_generator(obj, searched_class, **kwargs) -> Callable[[],Generator]:
        """
        Create a generator that will iterate on all the object on a given route.

        args:
            obj: An Instance of our classes.
            searched_class: The class that will be listed.

        returns:
            A generator
        """
        request = Request()

        def gen():
            has_more = True

            while has_more:
                try:
                    response = json.loads(request.get(obj, update=False, **kwargs))

                    keys = list(response.keys() - ["live_mode", "range"])

                    if len(keys) != 1:
                        raise InvalidSearchResponse("Results not found.")

                    key = keys[0]
                    has_more = response["range"]["has_more"]
                    kwargs["start"] = (
                        response["range"]["start"] + response["range"]["limit"]
                    )

                    for item in response[key]:
                        yield searched_class().hydrate(**item)

                except NotFoundError:
                    has_more = False

                except json.JSONDecodeError as err:
                    has_more = False

                    raise InvalidSearchResponse("Invalid results.") from err

        return gen()

    @classmethod
    def list(
        cls,
        created: int | datetime = None,
        limit: int = None,
        start: int = None,
        **kwargs,
    ) -> Callable[[],Generator] :
        """
        List elements.

        Args:
            created: must be an unix timestamp or a datetime object which will
                filter payments equal to or greater than this value.
            limit: must be an integer between 1 and 100 and will limit the number of
                objects to be returned.
            start: must be an integer, will be used as a pagination cursor,
                starts at 0.
            kwargs: Arbitrary keyword argument.

        Returns:
            Generator.
        """

        params = cls.get_param(created, limit, start, **kwargs)

        if not params:
            raise InvalidSearchFilter("Invalid search filters.")

        return cls._create_generator(cls(), cls, **params)
