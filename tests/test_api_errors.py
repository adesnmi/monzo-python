from monzo.monzo import Monzo
from monzo.errors import BadRequestError
import pytest


class TestApiErrors:
    @pytest.fixture
    def unauthorized_client(self):
        return Monzo("gibberish")

    def test_whoami(self, unauthorized_client):
        with pytest.raises(BadRequestError):
            unauthorized_client.whoami()
