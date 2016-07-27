from mondo.mondo import Mondo
from mondo.errors import UnauthorizedError
import pytest

class TestApiErrors:
    @pytest.fixture
    def unauthorized_client(self):
        return Mondo('gibberish')

    def test_whoami(self, unauthorized_client):
        with pytest.raises(UnauthorizedError):
            unauthorized_client.whoami()
