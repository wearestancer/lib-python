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

from functools import wraps


def populate_on_call(method):
    @wraps(method)
    def wrapper(self):
        if hasattr(self, 'populate'):
            self.populate()

        return method(self)
    return wrapper


def validate_type(type_expected, **options):
    def wrapper(method):
        @wraps(method)
        def wrapper(self, value, *args, **kwargs):
            name = options.get('name', method.__name__.capitalize())
            type_name = 'a ' + type_expected.__name__
            message = None
            std_type = False

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

                min = None
                max = None
                char_suffix = ''

                if 'min' in options:
                    min = options['min']

                if 'max' in options:
                    max = options['max']

                if isinstance(value, str):
                    char_suffix = ' characters'

                if min is not None:
                    if max is not None:
                        if length < min or length > max:
                            message = '{} must be between {} and {}{}.'.format(
                                name,
                                min,
                                max,
                                char_suffix,
                            )
                    elif length < min:
                        message = (
                            '{} must be greater '
                            'than or equal to {}{}.'
                        ).format(
                            name,
                            min,
                            char_suffix,
                        )

                elif max is not None and length > max:
                    message = '{} must be {}{} maximum.'.format(
                        name,
                        max,
                        char_suffix,
                    )

                tmp_value = value

                if (
                    'lowercase' in options
                    and options['lowercase']
                    and hasattr(value, 'lower')
                ):
                    tmp_value = value.lower()

                if (
                    'allowed' in options
                    and tmp_value not in options['allowed']
                ):
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
                raise TypeError(message)

            return method(self, value, *args, **kwargs)
        return wrapper
    return wrapper
