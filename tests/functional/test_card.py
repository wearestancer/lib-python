"""Functional tests for card object"""

from datetime import datetime
import pytest

from stancer import Card
from stancer.exceptions import ConflictError
from stancer.exceptions import NotFoundError
from .TestHelper import TestHelper


class TestFunctionalCard(TestHelper):
    def test_get(self):
        with pytest.raises(NotFoundError) as error:
            obj = Card(self.random_string(29))
            obj.name

        assert error.value.message == 'No such card {}'.format(obj.id)
        assert error.value.reason == 'Not Found'
        assert error.value.status_code == 404
        assert error.value.type == 'invalid_request_error'

        card = Card('card_9bKZ9cr0Ji0qSPs5c1uMQG5z')

        assert card.brand == 'visa'
        assert card.country == 'US'
        assert card.exp_month == 2
        assert card.exp_year == 2030
        assert card.funding == 'credit'
        assert card.last4 == '3055'
        assert card.nature == 'personnal'
        assert card.network == 'visa'

        assert isinstance(card.created, datetime)
        assert card.created.timestamp() == 1579024205

    def test_crud(self):
        obj = Card()

        month = self.random_integer(1, 12)
        year = self.random_year() + 20  # To be sure we do not have a conflict with previous tests

        cvc = str(self.random_integer(100, 999))
        name = 'Pickle Rick (' + self.random_string(10) + ')'
        number = self.get_card_number()

        last4 = number[-4:]

        # Create

        card = Card(cvc=cvc, exp_month=month, exp_year=year, number=number)

        assert card.send() == card
        assert card.id.startswith('card_')

        card_id = card.id

        # No duplicate

        card = Card(cvc=cvc, exp_month=month, exp_year=year, number=number)

        with pytest.raises(ConflictError):
            card.send()

        # Update

        card = Card(card_id)
        card.name = name

        assert card.send() == card
        assert card.name == name

        # Read

        card = Card(card_id)

        assert card.cvc is None  # CVC can not be obtain
        assert card.exp_month == month
        assert card.exp_year == year
        assert card.name == name
        assert card.number is None  # Number can not be obtain
        assert card.last4 == last4  # But last 4 digits can

        # We can not valid values here
        assert card.funding is not None
        assert card.nature is not None
        assert card.network is not None

        # Delete

        card = Card(card_id)

        assert card.delete() == card
        assert card.id is None

        # We could not get this card anymore

        with pytest.raises(
            NotFoundError,
            match='No such card {}'.format(card_id),
        ):
            Card(card_id).name
