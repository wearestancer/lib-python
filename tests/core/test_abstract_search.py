"""Test abstract search object"""

from datetime import datetime
from datetime import timedelta
import pytest
from time import time

from iliad_payment.core import AbstractSearch
from iliad_payment.exceptions import InvalidSearchFilter
from ..TestHelper import TestHelper


class TestAbstractSearch(TestHelper):
    def test_invalid_created(self):
        with pytest.raises(
            InvalidSearchFilter,
            match='Created must be a position integer or a DateTime object.',
        ):
            AbstractSearch.list(created=-1)

        with pytest.raises(
            InvalidSearchFilter,
            match='Created must be a position integer or a DateTime object.',
        ):
            AbstractSearch.list(created=self.random_string(10))

        with pytest.raises(
            InvalidSearchFilter,
            match='Created must be a position integer or a DateTime object.',
        ):
            AbstractSearch.list(created=AbstractSearch())

        with pytest.raises(
            InvalidSearchFilter,
            match='Created must be in the past.',
        ):
            AbstractSearch.list(created=time() + 100)

        with pytest.raises(
            InvalidSearchFilter,
            match='Created must be in the past.',
        ):
            date = datetime.now() + timedelta(days=1)
            AbstractSearch.list(created=date)
