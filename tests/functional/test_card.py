"""Functional tests for card object"""

import uuid

from datetime import datetime

import pytest

from stancer.card import Card
from stancer.core.enum.version import Version
from stancer.exceptions import ConflictError
from stancer.exceptions import NotFoundError

from .FunctionalTestHelper import FunctionalTestHelper


class TestFunctionalCard(FunctionalTestHelper):
    def personal(self):
        if self.conf.version == Version.API_V1:
            return 'personnal'
        return 'personal'

    @pytest.mark.parametrize('version', FunctionalTestHelper.version_provider())
    def test_get(self, version):
        self.conf.version = version
        with pytest.raises(NotFoundError) as error:
            obj = Card(f'card_{self.random_string(24)}')
            assert obj.name

        assert error.value.message == self.get_not_found_message(obj)
        assert error.value.reason == 'Not Found'
        assert error.value.status_code == 404

        card = Card('card_qmBSM2yPUintympn5To5MTYt')

        assert card.brand == 'visa'
        assert card.country == 'FR'
        assert card.exp_month == 3
        assert card.exp_year == 2031
        assert card.funding == 'credit'
        assert card.last4 == '0077'
        assert card.nature == self.personal()
        assert card.network == 'national'

        assert isinstance(card.created, datetime)
        assert card.created.timestamp() == 1759503504

    @pytest.mark.parametrize('version', FunctionalTestHelper.version_provider())
    def test_minimum_crud(self, version):
        self.conf.version = version
        month = self.random_integer(1, 11)
        year = (
            self.random_year() + 20
        )  # We add 20 years to be sure we do not have a conflict with previous tests
        number = self.get_card_number()

        last4 = number[-4:]

        # Create

        card = Card(exp_month=month, exp_year=year, number=number)
        assert card.send() == card
        assert card.id.startswith('card_')

        card_id = card.id

        # CHANGE: IN api v1 we couldn't create duplicate, now it is possible

        card = Card(exp_month=month, exp_year=year, number=number)
        # WARNING We make conditional statements in test
        # api v2 can create new card with the same info, apiv1 cannot
        if self.conf.version != Version.API_V1:
            assert card.send() == card
            assert card.id == card_id
        else:
            with pytest.raises(ConflictError):
                card.send()
        # Update The Date

        card = Card(card_id)
        month2 = month + 1
        year2 = year + 5
        card.exp_month = month2
        card.exp_year = year2

        assert card.send() == card
        assert card.exp_month == month2
        assert card.exp_year == year2

        # Read

        card = Card(card_id)

        assert card.cvc is None  # CVC can not be obtain
        assert card.exp_month == month2
        assert card.exp_year == year2
        assert card.number is None  # Number can not be obtain
        assert card.last4 == last4  # But last 4 digits can
        assert not card.deleted
        # We can not valid values here
        assert card.funding is not None
        assert card.nature is not None
        assert card.network is not None

        # Delete

        card = Card(card_id)

        assert card.delete() == card
        if self.conf.version == Version.API_V1:
            assert card.id is None

            # We could not get this card anymore

            with pytest.raises(NotFoundError, match=f'No such card {card_id}'):
                Card(card_id).name
        else:
            assert card.id == card_id
            assert card.cvc is None  # CVC can not be obtain
            assert card.exp_month == month2
            assert card.exp_year == year2
            assert card.number is None  # Number can not be obtain
            assert card.last4 == last4  # But last 4 digits can

            # We can not valid values here
            assert card.funding is not None
            assert card.nature is not None
            assert card.network is not None
            assert card.deleted

            # We cannot Patch a Deleted Card

            card = Card(card_id)
            card.exp_year = year2 + 1

            with pytest.raises(NotFoundError, match=f'Card `{card.id}` not found'):
                card.send()

    @pytest.mark.parametrize('version', FunctionalTestHelper.version_provider())
    def test_complete_crud_card(self, version):
        self.conf.version = version
        card = Card()
        cvc = str(self.random_integer(100, 999))
        exp_month = self.random_integer(1, 12)
        exp_year = self.random_year() + 20
        external_id = uuid.uuid4()
        name = "John's Card"
        number = self.get_card_number()
        tokenize = bool(self.random_bool())
        zip_code = str(self.random_integer(10, 1000))

        last4 = number[-4:]

        card.cvc = cvc
        card.exp_month = exp_month
        card.exp_year = exp_year
        card.name = name
        card.number = number
        card.external_id = external_id
        card.tokenize = tokenize
        card.zip_code = zip_code

        assert card.id is None

        ## Create
        assert card.send() == card
        assert card.id is not None

        assert card.cvc == cvc
        assert not card.deleted
        assert card.exp_month == exp_month
        assert card.exp_year == exp_year
        assert card.external_id == str(external_id)
        assert card.last4 == last4
        assert card.name == name
        assert card.number == number
        assert card.tokenize == tokenize
        assert card.zip_code == zip_code

        assert card.brand is not None
        assert card.country is not None
        assert card.created is not None
        assert card.funding is not None
        assert card.nature is not None
        assert card.network is not None

        ## Read
        card2 = Card(card.id)
        card2.send()

        assert card2.exp_month == exp_month
        assert card2.exp_year == exp_year
        assert card2.external_id == str(external_id)
        assert not card2.deleted
        assert card2.id == card.id
        assert card2.last4 == last4
        assert card2.name == name
        assert card2.number is None  # We cannot retrieve card number
        assert card2.zip_code == zip_code

        assert card2.brand is not None
        assert card2.country is not None
        assert card2.created is not None
        assert card2.funding is not None
        assert card2.nature is not None
        assert card2.network is not None

        ## Update

        exp_month2 = self.random_integer(1, 12)
        exp_year2 = self.random_year() + 20
        external_id2 = uuid.uuid4()
        zip_code2 = zip_code + '1'

        card2.exp_month = exp_month2
        card2.exp_year = exp_year2
        card2.external_id = str(external_id2)
        card2.zip_code = zip_code2

        card2.send()

        ## As the card is a new object we check get all but only Get fields.
        assert card2.exp_month == exp_month2
        assert card2.exp_year == exp_year2
        assert card2.external_id == str(external_id2)
        assert card2.id == card.id
        assert card2.last4 == last4
        assert card2.name == name
        assert card2.number is None  # We cannot retrieve card number
        assert card2.zip_code == zip_code2

        assert card2.brand is not None
        assert card2.country is not None
        assert card2.created is not None
        assert not card2.deleted
        assert card2.funding is not None
        assert card2.nature is not None
        assert card2.network is not None

        ## Delete
        card2.delete()

        assert card2.exp_month == exp_month2
        assert card2.exp_year == exp_year2
        assert card2.external_id == str(external_id2)

        # WARNING conditional in test,
        # API V1 doesn't handle well the deletion of objects, such as card.
        if self.conf.version == Version.API_V1:
            assert card2.deleted is None
            assert card2.id is None
            with pytest.raises(NotFoundError, match=f'No such card {card.id}'):
                Card(card.id).name
        else:
            assert card2.deleted
            assert card2.id == card.id
            assert card2.last4 == last4
            assert card2.name == name
            assert card2.number is None  # We cannot retrieve card number
            assert card2.zip_code == zip_code2

            assert card2.brand is not None
            assert card2.country is not None
            assert card2.created is not None
            assert card2.funding is not None
            assert card2.nature is not None
            assert card2.network is not None
