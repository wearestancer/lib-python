# -*- coding: utf-8 -*-

from ..exceptions import IliadHTTPError
from ..exceptions import IliadValueError
import json
import requests

from ..config import Config


class Request(object):
    """API request manager."""

    def __init__(self, obj):
        """Initialize"""
        self._obj = obj
        self._conf = Config()

    def __getattr__(self, name):
        """Handle automaticaly "get", "post" and "delete" method."""
        if name in ['delete', 'get', 'post']:
            if self._obj.id is None and (name == 'get' or name == 'delete'):
                message = (
                    'You can not {} an object without an ID.'
                ).format(name)

                raise IliadValueError(message)

            username = self._conf.secret_key

            if username is None:
                raise AttributeError('No API key found.')

            if name == 'post' and self._obj.id is not None:
                name = 'patch'

            method = getattr(requests, name)

            body = None

            if name != 'get' and name != 'delete':
                body = self._obj.to_json()

            response = method(
                self._obj.uri,
                auth=(username, ''),
                data=body,
                timeout=self._conf.timeout,
                headers={
                    'Content-Type': 'application/json',
                },
            )

            if not response.ok:
                raise IliadHTTPError.factory(response)

            if response.ok and name == 'delete':
                self._obj.hydrate({'id': None})

            if response.text is not None:
                try:
                    self._obj.hydrate(response.json())
                except ValueError:
                    # Bypass in case of decoding error
                    #  (if the body is HTML or whatever)
                    pass

        return self
