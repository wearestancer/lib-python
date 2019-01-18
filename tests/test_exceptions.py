"""Test exceptions"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from future import standard_library
standard_library.install_aliases()

from builtins import *  # pylint: disable=unused-wildcard-import, wildcard-import

from iliad_payment.exceptions import IliadException
from iliad_payment.exceptions import IliadTypeError
from iliad_payment.exceptions import IliadValueError
from iliad_payment.exceptions import IliadWarning
from .TestHelper import TestHelper


class TestExceptions(TestHelper):
    def test_iliad_exception(self):
        assert issubclass(IliadException, Exception)

    def test_iliad_type_error(self):
        assert issubclass(IliadTypeError, IliadException)
        assert issubclass(IliadTypeError, TypeError)

    def test_iliad_value_error(self):
        assert issubclass(IliadValueError, IliadException)
        assert issubclass(IliadValueError, ValueError)

    def test_iliad_warning(self):
        assert issubclass(IliadWarning, IliadException)
        assert issubclass(IliadWarning, Warning)
