# -*- coding: utf-8 -*-

from builtins import int
from builtins import str

from functools import wraps


def populate_on_call(method):
    """
    Do a `populate` call before getting the value.

    This permits to get fresh data only when you need it,
    and reduce API calls.
    """
    @wraps(method)
    def wrapper(self):
        if hasattr(self, 'populate'):
            self.populate()

        return method(self)
    return wrapper


def validate_type(type_expected, **options):
    """
    Validate type, length... before setting values.

    This also add modified flag after modification.
    """
    def wrapper(method):
        @wraps(method)
        def wrapper(self, value, *args, **kwargs):
            name = options.get('name', method.__name__.capitalize())
            type_name = 'a ' + type_expected.__name__
            message = None
            std_type = False
            excep = ValueError

            try:
                length = len(value)
            except TypeError:
                length = value

            if type_expected == str:
                type_name = 'a string'
                std_type = True

            if type_expected == int:
                type_name = 'an integer'
                std_type = True

            if type_expected == bool:
                type_name = 'a boolean'
                std_type = True

            if not isinstance(value, type_expected):
                message = '{} must be {}.'.format(name, type_name)
                excep = TypeError

                if not std_type:
                    message = (
                        'You must provide a '
                        'valid instance of {}.'
                    ).format(type_expected.__name__)

            if std_type and message is None:
                if 'length' in options and length != options['length']:
                    message = '{} must have {} characters.'.format(
                        name,
                        options['length'],
                    )

                minimum = None
                maximum = None
                char_suffix = ''

                if 'min' in options:
                    minimum = options['min']

                if 'max' in options:
                    maximum = options['max']

                if isinstance(value, str):
                    char_suffix = ' characters'

                if minimum is not None:
                    if maximum is not None:
                        if length < minimum or length > maximum:
                            message = '{} must be between {} and {}{}.'.format(
                                name,
                                minimum,
                                maximum,
                                char_suffix,
                            )
                    elif length < minimum:
                        message = (
                            '{} must be greater '
                            'than or equal to {}{}.'
                        ).format(
                            name,
                            minimum,
                            char_suffix,
                        )

                elif maximum is not None and length > maximum:
                    message = '{} must be {}{} maximum.'.format(
                        name,
                        maximum,
                        char_suffix,
                    )

                tmp_value = value

                if 'lowercase' in options and options['lowercase'] and hasattr(value, 'lower'):
                    tmp_value = value.lower()

                if 'allowed' in options and tmp_value not in options['allowed']:
                    message = (
                        '"{}" is not a valid {}, '
                        'please use one of following: {}'
                    ).format(
                        value,
                        options.get('name', method.__name__),
                        ', '.join(options['allowed'])
                    )

                value = tmp_value

            if message is not None:
                if 'throws' in options:
                    excep = options['throws']

                raise excep(message)

            res = method(self, value, *args, **kwargs)

            if hasattr(self, '_modified'):
                self._modified = True  ## pylint: disable=protected-access

            return res
        return wrapper
    return wrapper
