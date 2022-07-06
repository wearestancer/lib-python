# -*- coding: utf-8 -*-

from typing import TypeVar, Union

import requests

from ..config import Config
from ..exceptions import StancerHTTPError
from ..exceptions import StancerValueError


CurrentInstance = TypeVar('CurrentInstance', bound='Request')
AbstractObject = TypeVar('AbstractObject', bound='AbstractObject')


class Request(object):
    """API request manager."""

    def __init__(self):
        """Initialize"""
        self._conf = Config()

    def delete(self, obj: AbstractObject) -> CurrentInstance:
        """
        Send a DELETE HTTP request.

        Args:
            obj: Target object.

        Returns:
            Current instance of Request.
        """
        return self._request('delete', obj)

    def get(
        self,
        obj: AbstractObject,
        update: bool = True,
        **kwargs,
    ) -> Union[CurrentInstance, str]:
        """
        Send a GET HTTP request.

        Args:
            obj: Target object.
            update: Do we update the object ?
            kwargs: Query parameters.

        Returns:
            Current instance of Request.
        """
        return self._request('get', obj, update, **kwargs)

    def patch(self, obj: AbstractObject) -> CurrentInstance:
        """
        Send a POST HTTP request.

        Args:
            obj: Target object.

        Returns:
            Current instance of Request.
        """
        return self._request('patch', obj)

    def post(self, obj: AbstractObject) -> CurrentInstance:
        """
        Send a POST HTTP request.

        Args:
            obj: Target object.

        Returns:
            Current instance of Request.
        """
        return self._request('post', obj)

    def _request(
        self,
        method: str,
        obj: AbstractObject,
        update: bool = True,
        **kwargs,
    ) -> CurrentInstance:
        """Handle "delete", "get", "patch" and "post" method."""

        if method not in ['delete', 'get', 'patch', 'post']:
            raise StancerValueError('Invalid HTTP method.')

        username = self._conf.secret_key

        if username is None:
            raise AttributeError('No API key found.')

        body = None

        if method not in ('get', 'delete'):
            body = obj.to_json()

        response = requests.request(
            method,
            obj.uri,
            auth=(username, ''),
            data=body,
            params=kwargs,
            timeout=self._conf.timeout,
            headers={
                'Content-Type': 'application/json',
            },
        )

        if not response.ok:
            raise StancerHTTPError(response)

        if response.ok and method == 'delete':
            del obj.id

        if not update:
            return response.text

        if response.text:
            # pylint: disable=protected-access
            obj._bypass = True
            obj.hydrate(**response.json())
            obj._bypass = False

        return self
