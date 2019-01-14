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

from .core.singleton import Singleton


class Config(Singleton):
    """Handle configuration, connection and credential to API"""

    def __init__(self):
        self._host = 'api.iliad78.net'
        self._version = 1

    @property
    def host(self):
        """API host."""
        return self._host

    @host.setter
    def host(self, value):
        self._host = value

    @property
    def version(self):
        """API version."""
        return self._version

    @version.setter
    def version(self, value):
        self._version = value
