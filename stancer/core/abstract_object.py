# -*- coding: utf-8 -*-

from datetime import datetime
import json
from typing import Set
from typing import TypeVar

from ..config import Config
from .decorators import populate_on_call
from .request import Request


CurrentInstance = TypeVar('CurrentInstance', bound='AbstractObject')

# pylint: disable=too-many-branches


class AbstractObject(object):
    """Manage common code between API object."""

    _ENDPOINT = None  # pylint: disable=invalid-name
    _allowed_attributes = []
    _datetime_property = [
        'created',
    ]
    _default_values = {}
    _repr_ignore = set()

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
        self._data = {}
        self._bypass = False
        self._populated = True

        # init modified flags
        self.__modified = None
        del self._modified

        self.hydrate(**self._default_values)

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

        for key, value in self._data.items():
            representation[key] = value

        return representation

    def __repr__(self) -> str:
        args = []

        if self.id:
            args.append(f'"{self.id}"')

        for key in sorted(self._data.keys()):
            if key in self._repr_ignore:
                continue

            value = self._data.get(key)

            if isinstance(value, int):
                args.append(f'{key}={value}')
            else:
                args.append(f'{key}="{value}"')

        name = type(self).__name__

        return f'<{name}({", ".join(args)}) at 0x{id(self):02x}>'

    @property
    def _bypass(self) -> bool:
        return self.__bypass

    @_bypass.setter
    def _bypass(self, value: bool):
        self.__bypass = value

        for obj in self._data.values():
            # pylint: disable=protected-access
            if isinstance(obj, AbstractObject) and obj.__bypass != value:
                obj._bypass = value

    @classmethod
    def _get_allowed_attributes(cls) -> Set[str]:
        allowed = set()

        for parent in cls.mro():
            if hasattr(parent, '_allowed_attributes'):
                allowed.update(parent._allowed_attributes)  # pylint: disable=protected-access

        return allowed

    @classmethod
    def _get_datetime_property(cls) -> Set[str]:
        allowed = set()

        for parent in cls.mro():
            if hasattr(parent, '_datetime_property'):
                allowed.update(parent._datetime_property)  # pylint: disable=protected-access

        return allowed

    @property
    def _modified(self) -> Set[str]:
        return self.__modified

    @_modified.setter
    def _modified(self, value: str):
        self.__modified.add(value)

    @_modified.deleter
    def _modified(self):
        self.__modified = set()

        for obj in self._data.values():
            # pylint: disable=protected-access
            if isinstance(obj, AbstractObject) and obj._modified:
                del obj._modified

    @property
    def _populated(self) -> bool:
        return self.__populated

    @_populated.setter
    def _populated(self, value: bool):
        self.__populated = value

        for obj in self._data.values():
            # pylint: disable=protected-access
            if isinstance(obj, AbstractObject) and obj.__populated != value:
                obj._populated = value

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
    @populate_on_call
    def created(self) -> datetime:
        """
        Return the creation date and time of the current object.

        Returns:
            Creation date and time (into the API) during server side creation.
        """
        return self._data.get('created')

    def delete(self) -> CurrentInstance:
        """
        Delete the current object.

        Returns:
            Current instance.

        Raises:
            StancerHTTPError: On error during with the API.
        """
        Request().delete(self)

        # Force modified to allow sending it again to the API
        self._modified = 'id'

        return self

    def _hydrate_list(self, key, value):
        tmp = getattr(self, key)
        init_method = '_init_' + key
        new_values = []

        for current_value in value:
            missing = True
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

                if obj not in new_values:
                    new_values.append(obj)

            if missing:
                if not isinstance(val, AbstractObject):
                    cls = getattr(self, init_method)
                    val = cls(uid, **val)

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

                elif isinstance(tmp, AbstractObject) and not isinstance(value, AbstractObject):
                    val = {'id': value} if not isinstance(value, dict) else value

                    # pylint: disable=protected-access

                    modify = False
                    populated = tmp._populated
                    tmp._populated = True
                    value = tmp.hydrate(**val)
                    value._populated = populated

            if key in self._get_datetime_property() and isinstance(value, int):
                value = datetime.fromtimestamp(value, tz=config.default_timezone)

            if key == 'id':
                self._id = value
            else:
                applied = False

                try:
                    prop = dict(self.__class__.__dict__).get(key)

                    if prop is not None and prop.fset is not None:
                        prop.fset(self, value)
                        applied = True
                except ValueError:
                    if not self._bypass:
                        raise

                if not applied:
                    self._data[key] = value

                    if modify:
                        self._modified = key

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

    @property
    @populate_on_call
    def live_mode(self) -> bool:
        """
        Indicate if we are in live or test mode.

        True => live / False => test

        Returns:
            Are we in live mode ?
        """
        return self._data.get('live_mode')

    def populate(self) -> CurrentInstance:
        """
        Populate the current object.

        It will call the API to obtain current object's data.
        This need an ID.

        Returns:
            Current instance.
        """
        if self.id is not None and self._ENDPOINT is not None and not self._populated:
            self._populated = True
            Request().get(self)

            del self._modified

        self._populated = True

        return self

    def send(self) -> CurrentInstance:
        """
        Save the current object.

        This will create or update the current object.

        Returns:
            Current instance.

        Raises:
            StancerHTTPError: On error during with the API (may be child instance
                of StancerHTTPError).
        """
        if self._modified:
            if self.id is None:
                Request().post(self)
            else:
                Request().patch(self)

        del self._modified

        return self

    def to_json(self) -> str:
        """
        Return a JSON representation of the current object.

        Be carefull, this is mainly used in `Object.send()` method.
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
                    val = value.to_json_repr()

                    if val:
                        representation[key] = val
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
        port = ''

        if conf.port is not None:
            port = f':{conf.port}'

        location = f'https://{conf.host}{port}/v{conf.version}'

        if self._ENDPOINT is not None:
            location += '/' + self._ENDPOINT

        if self.id is not None:
            location += '/' + self.id

        return location
