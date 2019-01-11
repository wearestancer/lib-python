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

from datetime import datetime
import json


class AbstractObject(object):
    """Manage common code between API object."""

    _filtered_attributes = [
        'id',
        'created',
    ]

    def __init__(self, uid=None):
        """
        Create or get an API object.

        You can optionaly pass an id uppon instanciation, it will be used to
        get current object data on the API.

        If you did not provide an id, the current object will be a new API
        object.
        """
        self._id = uid
        self._created = None
        self._data = {}

    @property
    def __dict__(self):
        """Return a dictionary representing the current object."""
        representation = {}

        if self.id is not None:
            representation['id'] = self.id

        if self.created is not None:
            representation['created'] = str(self.created)

        for key, value in self._data.items():
            if hasattr(value, '__dict__'):
                representation[key] = value.__dict__
            else:
                representation[key] = value

        return representation

    @property
    def id(self):  # pylint: disable=C0103
        """Return current object ID."""
        return self._id

    @property
    def created(self):
        """
        Return the creation date and time of the current object.

        The creation date is provided by the API during server side creation.
        This method returns a datetime instance.
        """
        return self._created

    def _get_filtered_attributes(self):
        filtered = self._filtered_attributes

        if hasattr(super(), '_get_filtered_attributes'):
            filtered += super()._get_filtered_attributes()

        return filtered

    def hydrate(self, params):
        """
        Hydrate current object.

        `params` supposed to be a dictionary within each key will be
        an object property.
        """

        for key, value in list(params.items()):
            if hasattr(self, key):
                tmp = getattr(self, key)

                if hasattr(tmp, 'hydrate'):
                    val = {'id': value} if isinstance(value, str) else value
                    value = tmp.hydrate(val)

            if key == 'id':
                self._id = value
            elif key == 'created':
                self._created = datetime.fromtimestamp(value)
            else:
                self._data[key] = value

        return self

    def to_json(self):
        """Return a JSON representation of the current object."""
        representation = {}

        if self.id is not None:
            representation['id'] = self.id
        else:
            items = {
                k: v
                for k, v in self._data.items()
                if k not in self._filtered_attributes
            }

            for key, value in items.items():
                if hasattr(value, '__dict__'):
                    child = value.__dict__

                    if 'id' in child and child['id'] is not None:
                        representation[key] = {'id': child['id']}
                    else:
                        representation[key] = {
                            k: v
                            for k, v in child.items()
                            if k not in value._get_filtered_attributes()
                        }
                else:
                    representation[key] = value

        return json.dumps(representation, separators=(',', ':'))
