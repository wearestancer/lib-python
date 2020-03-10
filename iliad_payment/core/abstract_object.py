# -*- coding: utf-8 -*-

from datetime import datetime
import json
from typing import List
from typing import TypeVar

from ..config import Config
from .request import Request


CurrentInstance = TypeVar('CurrentInstance', bound='AbstractObject')

# pylint: disable=too-many-branches


class AbstractObject(object):
    """Manage common code between API object."""

    _ENDPOINT = None  # pylint: disable=invalid-name
    _allowed_attributes = []

    def __init__(self, uid: str = None, **kwargs):
        """
        Create or get an API object.

        You can optionaly pass an id uppon instanciation, it will be used to
        get current object data on the API.

        If you did not provide an id, the current object will be a new API
        object.

        You may also pass keywords arguments, we will use them hydrate the object.

        Args:
            uid: Object identifier.
            **kwargs: Arbitrary keyword arguments, used to hydrate the object.

        Returns:
            An instance of the current object.
        """
        self._id = uid
        self._created = None
        self._data = {}
        self._modified = set()
        self._populated = True

        if kwargs:
            self.hydrate(**kwargs)

        self._populated = False

    @property
    def __dict__(self) -> dict:
        """
        Dictionary for instance variables.

        Returns:
            A simple representation of the current object.
        """
        representation = {}

        if self.id is not None:
            representation['id'] = self.id

        if self.created is not None:
            representation['created'] = self.created

        for key, value in self._data.items():
            representation[key] = value

        return representation

    @property
    def id(self) -> str:  # pylint: disable=invalid-name
        """
        Return current object ID.

        Returns:
            Current ID.
        """
        return self._id

    @id.deleter
    def id(self):  # pylint: disable=invalid-name
        self._id = None

    @property
    def created(self) -> datetime:
        """
        Return the creation date and time of the current object.

        Returns:
            Creation date and time (into the API) during server side creation.
        """
        return self._created

    def delete(self) -> CurrentInstance:
        """
        Delete the current object.

        Returns:
            Current instance.

        Raises:
            IliadHTTPError: On error during with the API.
        """
        Request(self).delete  ## pylint: disable=expression-not-assigned

        self._modified = [
            'id', # Force modified to allow sending it again to the API
        ]

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

    def _hydrate_list(self, key, value):
        tmp = getattr(self, key)
        init_method = '_init_' + key
        new_values = []

        for current_value in value:
            missing = True
            uid = None
            val = current_value

            if isinstance(current_value, str):
                uid = current_value
                val = {}
            elif isinstance(current_value, AbstractObject):
                uid = current_value.id
            else:
                uid = current_value.get('id')

            for obj in tmp:
                if obj.id == uid:
                    missing = False

                    if isinstance(val, AbstractObject):
                        obj.hydrate(**val.__dict__)
                    else:
                        obj.hydrate(**val)

                if not obj in new_values:
                    new_values.append(obj)

            if missing:
                if not isinstance(val, AbstractObject):
                    cls = getattr(self, init_method)

                    obj = cls(uid)

                    obj._populated = True   # pylint: disable=protected-access
                    obj.hydrate(**val)
                    obj._populated = False  # pylint: disable=protected-access

                    val = obj

                if val not in new_values:
                    new_values.append(val)

        return new_values

    def hydrate(self, **params) -> CurrentInstance:
        """
        Hydrate current object.

        Args:
            **params: Elements used to hydrate the object.
                Every key matching an object property will be used.

        Returns:
            Current instance.
        """
        config = Config()

        for key, value in list(params.items()):
            if value is not False and not value:
                continue

            modify = True

            if hasattr(self, key):
                tmp = getattr(self, key)
                init_method = '_init_' + key

                if isinstance(tmp, list) and isinstance(value, list) and hasattr(self, init_method):
                    value = self._hydrate_list(key, value)
                    modify = not all(isinstance(val, AbstractObject) for val in value)

                if isinstance(tmp, datetime):
                    tmp = None

                if tmp is None and isinstance(value, AbstractObject):
                    (tmp, value) = (value, {})

                if tmp is None and hasattr(self, init_method):
                    tmp = getattr(self, init_method)

                if callable(tmp):
                    modify = False

                    if isinstance(value, dict):
                        value = tmp(**value)
                    else:
                        value = tmp(value)

                elif hasattr(tmp, 'hydrate'):
                    val = {'id': value} if isinstance(value, str) else value
                    modify = False

                    if val is not None:
                        tmp._populated = True  ## pylint: disable=protected-access
                        value = tmp.hydrate(**val)
                        value._populated = self._populated  ## pylint: disable=protected-access

            if key == 'id':
                self._id = value
            elif key == 'created':
                self._created = datetime.fromtimestamp(value, tz=config.default_timezone)
            else:
                self._data[key] = value

                if modify:
                    self._modified.add(key)

        return self

    @property
    def is_complete(self) -> bool:
        """
        Indicate if all mandatory data are provided.

        Should be modified in other sub classes.

        Returns:
            Is the object complete ?
        """
        return True

    @property
    def is_modified(self) -> bool:
        """
        Indicate if the object was modified.

        Returns
            Was it modified ?
        """
        if len(self._modified) > 0:
            return True

        for key, value in self._data.items():
            if key not in self._get_allowed_attributes():
                continue

            if isinstance(value, AbstractObject) and value.is_modified:
                return True

            if isinstance(value, list):
                for val in value:
                    if isinstance(val, AbstractObject) and val.is_modified:
                        return True

        return False

    @property
    def is_not_complete(self) -> bool:
        """
        Indicate if all mandatory data are NOT provided.

        It's simply a `not self.is_complete`.

        Returns:
            Is the object not complete ?
        """
        return not self.is_complete

    @property
    def is_not_modified(self) -> bool:
        """
        Indicate if the object was not modified.

        Returns
            Was it not modified ?
        """
        return not self.is_modified

    @property
    def is_not_populated(self) -> bool:
        """
        Indicate if the object was not populated.

        Returns
            Was it not populated ?
        """
        return not self.is_populated

    @property
    def is_populated(self) -> bool:
        """
        Indicate if the object was populated.

        Returns
            Was it populated ?
        """
        return self._populated

    def populate(self) -> CurrentInstance:
        """
        Populate the current object.

        It will call the API to obtain current object's data.
        This need an ID.

        Returns:
            Current instance.
        """
        if self.id is not None and not self._populated:
            self._populated = True
            Request(self).get  ## pylint: disable=expression-not-assigned
            self._modified.clear()

        self._populated = True

        return self

    def save(self) -> CurrentInstance:
        """
        Save the current object.

        This will create or update the current object.

        Returns:
            Current instance.

        Raises:
            IliadHTTPError: On error during with the API (may be child instance of IliadHTTPError).
        """
        if self._modified:
            Request(self).post  ## pylint: disable=expression-not-assigned

        self._modified.clear()

        return self

    def to_json(self) -> str:
        """
        Return a JSON representation of the current object.

        Be carefull, this is mainly used in `Object.save()` method.
        It will return all object data if no ID is present or
        if the current object is tagged as `modified`.
        Unless that, it will return a JSON with only the `id` key.

        Returns:
            A JSON representation of the current object.
        """
        return json.dumps(self.to_json_repr(), separators=(',', ':'))

    def to_json_repr(self) -> dict:
        """
        Return a dictionnary which will be used to make a JSON representation.

        Returns:
            A JSON still as a dictionnary.
        """
        representation = {}

        if self.id is not None and self.is_not_modified:
            representation = self.id
        else:
            items = {
                k: v
                for k, v in self._data.items()
                if k in self._get_allowed_attributes()
                and v is not None
                and (k in self._modified or (isinstance(v, AbstractObject) and v.is_modified))
            }

            for key, value in items.items():
                if hasattr(value, 'to_json_repr'):
                    representation[key] = value.to_json_repr()
                else:
                    representation[key] = value

        return representation

    @property
    def uri(self) -> str:
        """
        Return a complete location for the current object.

        This method uses `Config.host`, `Config.port` and `Config.version`
        to generate the complete location.

        If the current object has an ID, it will return the location for
        this entity.

        Returns:
            Uniform Resource Identifier.
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
