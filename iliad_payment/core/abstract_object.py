# -*- coding: utf-8 -*-

from datetime import datetime
import json
from typing import List
from typing import TypeVar

from ..config import Config
from .request import Request


CurrentInstance = TypeVar('CurrentInstance', bound='AbstractObject')


class AbstractObject(object):
    """Manage common code between API object."""

    _ENDPOINT = None  # pylint: disable=invalid-name
    _allowed_attributes = []

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
    def __dict__(self) -> dict:
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
            if hasattr(value, '__dict__') and not isinstance(value, str):
                representation[key] = value.__dict__
            else:
                representation[key] = value

        return representation

    @property
    def id(self) -> str:  # pylint: disable=invalid-name
        """
        Return current object ID.

        Returns:
            str: Current ID.
        """
        return self._id

    @property
    def created(self) -> datetime:
        """
        Return the creation date and time of the current object.

        Returns:
            datetime: Creation date and time (into the API)
                during server side creation.
        """
        return self._created

    def delete(self) -> CurrentInstance:
        """
        Delete the current object.

        Returns:
            self: Current instance.
        """
        Request(self).delete  ## pylint: disable=expression-not-assigned

        self._modified = True

        return self

    @classmethod
    def _get_allowed_attributes(cls) -> List[str]:
        allowed = []

        if hasattr(cls, '_allowed_attributes'):
            allowed = cls._allowed_attributes

        for parent in cls.mro():
            if parent != cls and hasattr(parent, '_allowed_attributes'):
                allowed += parent._allowed_attributes  ## pylint: disable=protected-access

        return allowed

    def hydrate(self, params: dict) -> CurrentInstance:
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

                    if val is not None:
                        tmp._populated = True  ## pylint: disable=protected-access
                        value = tmp.hydrate(val)
                        value._populated = self._populated  ## pylint: disable=protected-access

            if key == 'id':
                self._id = value
            elif key == 'created':
                self._created = datetime.fromtimestamp(value)
            else:
                self._data[key] = value

        return self

    @property
    def is_complete(self) -> bool:
        """
        Indicate if all mandatory data are provided.

        Should be modified in other sub classes.

        Returns:
            bool: Is the object complete ?
        """
        return True

    @property
    def is_modified(self) -> bool:
        """
        Indicate if the object was modified.

        Returns
            bool: Was it modified ?
        """
        return self._modified

    @property
    def is_not_complete(self) -> bool:
        """
        Indicate if all mandatory data are NOT provided.

        It's simply a `not self.is_complete`.

        Returns:
            bool: Is the object not complete ?
        """
        return not self.is_complete

    @property
    def is_not_modified(self) -> bool:
        """
        Indicate if the object was not modified.

        Returns
            bool: Was it not modified ?
        """
        return not self.is_modified

    @property
    def is_not_populated(self) -> bool:
        """
        Indicate if the object was not populated.

        Returns
            bool: Was it not populated ?
        """
        return not self.is_populated

    @property
    def is_populated(self) -> bool:
        """
        Indicate if the object was populated.

        Returns
            bool: Was it populated ?
        """
        return self._populated

    def populate(self) -> CurrentInstance:
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
            Request(self).get  ## pylint: disable=expression-not-assigned

        self._populated = True

        return self

    def save(self) -> CurrentInstance:
        """
        Save the current object.

        This will create or update the current object.

        Returns:
            self: Current instance.
        """
        if self._modified:
            Request(self).post  ## pylint: disable=expression-not-assigned

        self._modified = False

        return self

    def to_json(self) -> str:
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
                and v is not None
            }

            for key, value in items.items():
                if hasattr(value, '__dict__') and not isinstance(value, str):
                    child = value.__dict__

                    if 'id' in child and child['id'] is not None:
                        representation[key] = {'id': child['id']}
                    else:
                        representation[key] = {
                            k: v
                            for k, v in child.items()
                            if k in type(value)._get_allowed_attributes()  ## pylint: disable=protected-access
                            and v is not None
                        }
                else:
                    representation[key] = value

        return json.dumps(representation, separators=(',', ':'))

    @property
    def uri(self) -> str:
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
