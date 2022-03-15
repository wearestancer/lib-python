# -*- coding: utf-8 -*-

from datetime import datetime
from functools import wraps

from ...config import Config


# pylint: disable=too-many-branches, too-many-statements, too-many-locals

def validate_type(type_expected, **options):
    """
    Validate type, length... before setting values.

    This also add modified flag after modification.
    """

    config = Config()

    if 'silent' not in options:
        options['silent'] = False

    def get_min_max(options):
        minimum = None
        maximum = None

        if 'min' in options:
            minimum = options['min']

        if 'max' in options:
            maximum = options['max']

        return (minimum, maximum)

    def is_std_type():
        type_name = 'a ' + type_expected.__name__
        std_type = False

        if type_expected == str:
            type_name = 'a string'
            std_type = True

        if type_expected == int:
            type_name = 'an integer'
            std_type = True

        if type_expected == bool:
            type_name = 'a boolean'
            std_type = True

        return (std_type, type_name)

    def wrapper(method):
        @wraps(method)
        def wrapper(self, value=None, *args, **kwargs):  # pylint: disable=keyword-arg-before-vararg
            name = options.get('name', method.__name__.capitalize())
            message = None
            excep = ValueError
            is_optional = value is None and options.get('optional', False)

            (std_type, type_name) = is_std_type()

            if 'coerce' in options:
                value = options['coerce'](value)

                if value is None:
                    return None

            try:
                length = len(value)
            except TypeError:
                length = value

            if type_expected == datetime and isinstance(value, int):
                value = datetime.fromtimestamp(value, tz=config.default_timezone)

            if not isinstance(value, type_expected):
                message = f'{name} must be {type_name}.'
                excep = TypeError

                if not std_type:
                    message = f'You must provide a valid instance of {type_expected.__name__}.'

            if std_type and message is None:
                if 'length' in options and length != options['length']:
                    message = f'{name} must have {options["length"]} characters.'

                (minimum, maximum) = get_min_max(options)
                char_suffix = ''

                if isinstance(value, str):
                    char_suffix = ' characters'

                if minimum is not None:
                    if maximum is not None:
                        if length < minimum or length > maximum:
                            message = ' '.join([
                                f'{name} must be',
                                f'between {minimum} and {maximum}{char_suffix}.'
                            ])
                    elif length < minimum:
                        message = ' '.join([
                            f'{name} must be',
                            f'greater than or equal to {minimum}{char_suffix}.',
                        ])

                elif maximum is not None and length > maximum:
                    message = ' '.join([
                        f'{name} must be',
                        f'{maximum}{char_suffix} maximum.'
                    ])

                tmp_value = value

                if 'lowercase' in options and options['lowercase'] and hasattr(value, 'lower'):
                    tmp_value = value.lower()

                if 'allowed' in options and tmp_value not in options['allowed']:
                    message = ' '.join([
                        f'"{value}" is not a valid {options.get("name", method.__name__)},',
                        f'please use one of following: {", ".join(options["allowed"])}',
                    ])

                value = tmp_value

            if 'validation' in options and message is None:
                message = options['validation'](value)

            if message is not None and not is_optional:
                if 'throws' in options:
                    excep = options['throws']

                raise excep(message)

            res = method(self, value, *args, **kwargs)

            if hasattr(self, '_modified') and not options['silent']:
                self._modified = method.__name__  # pylint: disable=protected-access

            return res

        return wrapper

    return wrapper
