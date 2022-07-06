"""Test abstract search object"""

from datetime import datetime
from datetime import timedelta
import pytest
from time import time

from stancer.core import AbstractObject
from stancer.core import AbstractSearch
from stancer.exceptions import InvalidSearchFilter
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
            AbstractSearch.list(created=AbstractObject())

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

    def test_invalid_filters(self):
        with pytest.raises(
            InvalidSearchFilter,
            match='Invalid search filters.',
        ):
            AbstractSearch.list()

        with pytest.raises(
            InvalidSearchFilter,
            match='Invalid search filters.',
        ):
            AbstractSearch.list(foo='bar')

    def test_invalid_limit(self):
        with pytest.raises(
            InvalidSearchFilter,
            match='Limit must be between 1 and 100.',
        ):
            AbstractSearch.list(limit=0)

        with pytest.raises(
            InvalidSearchFilter,
            match='Limit must be between 1 and 100.',
        ):
            AbstractSearch.list(limit=101)

        with pytest.raises(
            InvalidSearchFilter,
            match='Limit must be between 1 and 100.',
        ):
            AbstractSearch.list(limit=self.random_string(10))

        with pytest.raises(
            InvalidSearchFilter,
            match='Limit must be between 1 and 100.',
        ):
            AbstractSearch.list(limit=AbstractObject())

    def test_invalid_start(self):
        with pytest.raises(
            InvalidSearchFilter,
            match='Start must be a positive integer.',
        ):
            AbstractSearch.list(start=-1)

        with pytest.raises(
            InvalidSearchFilter,
            match='Start must be a positive integer.',
        ):
            AbstractSearch.list(start=self.random_string(10))

        with pytest.raises(
            InvalidSearchFilter,
            match='Start must be a positive integer.',
        ):
            AbstractSearch.list(start=AbstractObject())
