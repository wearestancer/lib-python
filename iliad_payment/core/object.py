# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring

# pylint: enable=missing-docstring
from datetime import datetime


class Object:
    """Manage common code between API object."""

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

    def hydrate(self, params):
        """
        Hydrate current object.

        `params` supposed to be a dictionary within each key will be
        an object property.
        """

        for key, value in params.items():
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
