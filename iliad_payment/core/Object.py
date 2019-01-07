# -*- coding: utf-8 -*-


class Object:
    """Manage common code between API object."""

    def __init__(self, id=None):
        """
        Create or get an API object.

        You can optionaly pass an id uppon instanciation, it will be used to
        get current object data on the API.

        If you did not provide an id, the current object will be a new API
        object.
        """
        self._id = id
        self._created = None
        self._data = {}

    @property
    def id(self):
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
