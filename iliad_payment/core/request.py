# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring

# pylint: enable=missing-docstring
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from future import standard_library
standard_library.install_aliases()

from builtins import *  # pylint: disable=unused-wildcard-import, wildcard-import

from ..exceptions import IliadHTTPError
from ..exceptions import IliadValueError
import json
import requests

from ..config import Config


class Request(object):
    """API request manager."""

    def __init__(self, obj):
        self._obj = obj
        self._conf = Config()

    def __getattr__(self, name):
        if name in ['delete', 'get', 'post']:
            mode = self._conf.mode
            username = None

            if self._obj.id is None and (name == 'get' or name == 'delete'):
                message = (
                    'You can not {} an object without an ID.'
                ).format(name)

                raise IliadValueError(message)


            if self._conf.mode == Config.LIVE_MODE:
                mode = 'prod'

            for prefix in ['p', 's']:
                tmp = getattr(self._conf, prefix + mode)

                if tmp is not None:
                    username = tmp

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
