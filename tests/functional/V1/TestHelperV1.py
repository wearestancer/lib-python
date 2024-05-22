from stancer.core.enum import Version
from ..FunctionalTestHelper import TestHelper


class TestHelperV1(TestHelper):
    def setup_method(self,method):
        super().setup_method(method)
        self.conf.version = Version.API_V1

    def get_not_found_message(self, tested_object):
        name = str(tested_object.__class__.__name__)
        return f'No such {name.lower()} {format(tested_object.id)}'
