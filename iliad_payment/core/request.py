# -*- coding: utf-8 -*-

from typing import TypeVar

import requests

from ..config import Config
from ..exceptions import IliadHTTPError
from ..exceptions import IliadValueError


CurrentInstance = TypeVar('CurrentInstance', bound='Request')


class Request(object):
    """API request manager."""

    def __init__(self, obj):
        """Initialize"""
        self._obj = obj
        self._conf = Config()

    def __getattr__(self, method: str) -> CurrentInstance:
        """Handle automaticaly "get", "post" and "delete" method."""

        if method in ['delete', 'get', 'post']:
            if self._obj.id is None and method in ('get', 'delete'):
                message = (
                    'You can not {} an object without an ID.'
                ).format(method)

                raise IliadValueError(message)

            username = self._conf.secret_key

            if username is None:
                raise AttributeError('No API key found.')

            if method == 'post' and self._obj.id is not None:
                method = 'patch'

            body = None

            if method not in ('get', 'delete'):
                body = self._obj.to_json()

            response = requests.request(
                method,
                self._obj.uri,
                auth=(username, ''),
                data=body,
                timeout=self._conf.timeout,
                headers={
                    'Content-Type': 'application/json',
                },
            )

            if not response.ok:
                raise IliadHTTPError(response)

            if response.ok and method == 'delete':
                del self._obj.id

            if response.text is not None:
                try:
                    self._obj.hydrate(**response.json())
                except ValueError:
                    # Bypass in case of decoding error
                    #  (if the body is HTML or whatever)
                    pass

        return self
