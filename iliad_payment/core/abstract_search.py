# -*- coding: utf-8 -*-

from datetime import datetime
import json
from time import time
from typing import Union

from .request import Request
from ..exceptions import InvalidSearchFilter


class AbstractSearch(object):
    """Common search method."""

    @classmethod
    def list(
        cls,
        created: Union[int, datetime] = None,
        limit: int = None,
        start: int = None,
        **kwargs,
    ):
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

        params = {}

        if created is not None:
            if isinstance(created, datetime):
                created = created.timestamp()

            if isinstance(created, float):
                created = int(created)

            if not isinstance(created, int) or created < 0:
                message = 'Created must be a position integer or a DateTime object.'

                raise InvalidSearchFilter(message)

            if created > time():
                raise InvalidSearchFilter('Created must be in the past.')

            params['created'] = created

        if limit is not None:
            if not isinstance(limit, int) or limit < 1 or limit > 100:
                raise InvalidSearchFilter('Limit must be between 1 and 100.')

            params['limit'] = limit

        if start is not None:
            if not isinstance(start, int) or start < 0:
                raise InvalidSearchFilter('Start must be a positive integer.')

            params['start'] = start

        if not params:
            raise InvalidSearchFilter('Invalid search filters.')

        request = Request()
        obj = cls()

        def gen():
            has_more = True

            while has_more:
                response = json.loads(request.get(obj, update=False, **params))

                key = list(response.keys() - ['live_mode', 'range'])[0]

                has_more = response['range']['has_more']
                params['start'] = response['range']['start'] + response['range']['limit']

                for item in response[key]:
                    yield cls().hydrate(**item)

        return gen()
