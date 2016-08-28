from monzo.monzo import Monzo
from monzo.errors import UnauthorizedError
import pytest

class TestApiErrors:
    @pytest.fixture
    def unauthorized_client(self):
        return Monzo('gibberish')

    def test_whoami(self, unauthorized_client):
        with pytest.raises(UnauthorizedError):
            unauthorized_client.whoami()
