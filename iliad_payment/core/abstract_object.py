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
import requests

from ..config import Config
from .request import Request


class AbstractObject(object):
    """Manage common code between API object."""

    _ENDPOINT = None

    def __init__(self, uid=None):
        """
        Create or get an API object.

        You can optionaly pass an id uppon instanciation, it will be used to
        get current object data on the API.

        If you did not provide an id, the current object will be a new API
        object.

        Args:
            uid (str): Object identifier.

        Returns:
            self: An instance of the current object.
        """
        self._id = uid
        self._created = None
        self._data = {}
        self._modified = False
        self._populated = False

    @property
    def __dict__(self):
        """
        Dictionary for instance variables.

        Returns:
            dict: A simple representation of the current object.
        """
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
        """
        Return current object ID.

        Returns:
            str: Current ID.
        """
        return self._id

    @property
    def created(self):
        """
        Return the creation date and time of the current object.

        Returns:
            datetime: Creation date and time (into the API)
                during server side creation.
        """
        return self._created

    def delete(self):
        """
        Delete the current object.

        Returns:
            self: Current instance.
        """
        Request(self).delete

        self._modified = True

        return self

    @classmethod
    def _get_allowed_attributes(cls):
        allowed = []

        if hasattr(cls, '_allowed_attributes'):
            allowed = cls._allowed_attributes

        for parent in cls.mro():
            if parent != cls and hasattr(parent, '_allowed_attributes'):
                allowed += parent._allowed_attributes

        return allowed

    def hydrate(self, params):
        """
        Hydrate current object.

        Args:
            params (dict): Elements used to hydrate the object.
                Every key matching an object property will be used.

        Returns:
            self: Current instance.
        """

        for key, value in list(params.items()):
            if hasattr(self, key):
                tmp = getattr(self, key)
                init_method = '_init_' + key

                if tmp is None and hasattr(self, init_method):
                    tmp = getattr(self, init_method)

                if hasattr(tmp, 'hydrate'):
                    val = {'id': value} if isinstance(value, str) else value
                    tmp._populated = True
                    value = tmp.hydrate(val)
                    value._populated = self._populated

            if key == 'id':
                self._id = value
            elif key == 'created':
                self._created = datetime.fromtimestamp(value)
            else:
                self._data[key] = value

        return self

    @property
    def is_modified(self):
        """
        Indicate if the object was modified.

        Returns
            bool: Was it modified ?
        """
        return self._modified

    @property
    def is_not_modified(self):
        """
        Indicate if the object was not modified.

        Returns
            bool: Was it not modified ?
        """
        return not self.is_modified

    @property
    def is_not_populated(self):
        """
        Indicate if the object was not populated.

        Returns
            bool: Was it not populated ?
        """
        return not self.is_populated

    @property
    def is_populated(self):
        """
        Indicate if the object was populated.

        Returns
            bool: Was it populated ?
        """
        return self._populated

    def populate(self):
        """
        Populate the current object.

        It will call the API to obtain current object's data.
        This need an ID.

        Returns:
            self: Current instance.
        """
        if not self._populated and self.id is not None:
            self._populated = True
            self._modified = False
            Request(self).get

        self._populated = True

        return self

    def save(self):
        """
        Save the current object.

        This will create or update the current object.

        Returns:
            self: Current instance.
        """
        if self._modified:
            Request(self).post

        self._modified = False

        return self

    def to_json(self):
        """
        Return a JSON representation of the current object.

        Be carefull, this is mainly used in `Object.save()` method.
        It will return all object data if no ID is present or
        if the current object is tagged as `modified`.
        Unless that, it will return a JSON with only the `id` key.

        Returns:
            str: A JSON representation of the current object.
        """
        representation = {}

        if self.id is not None and not self._modified:
            representation['id'] = self.id
        else:
            items = {
                k: v
                for k, v in self._data.items()
                if k in self._get_allowed_attributes()
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
                            if k in type(value)._get_allowed_attributes()
                        }
                else:
                    representation[key] = value

        return json.dumps(representation, separators=(',', ':'))

    @property
    def uri(self):
        """
        Return a complete location for the current object.

        This method uses `Config.host`, `Config.port` and `Config.version`
        to generate the complete location.

        If the current object has an ID, it will return the location for
        this entity.

        Returns:
            str: Uniform Resource Identifier.
        """
        conf = Config()

        if conf.port is not None:
            location = 'https://{}:{}'.format(conf.host, conf.port)
        else:
            location = 'https://{}'.format(conf.host)

        location += '/v{}'.format(conf.version)

        if self._ENDPOINT is not None:
            location += '/' + self._ENDPOINT

        if self.id is not None:
            location += '/' + self.id

        return location
