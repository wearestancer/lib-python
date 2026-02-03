"""Test payment object"""

from stancer.status import ThreedsStatus

from .TestHelper import TestHelper


class TestThreedsStatus(TestHelper):
    def test_none(self):
        assert ThreedsStatus.NONE == 'none'
        assert ThreedsStatus.has_member('NONE')
        assert ThreedsStatus.has_value('none')

    def test_required(self):
        assert ThreedsStatus.REQUIRED == 'required'
        assert ThreedsStatus.has_member('REQUIRED')
        assert ThreedsStatus.has_value('required')
