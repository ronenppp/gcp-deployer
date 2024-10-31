import pytest

from utils.utils import *


class TestUtils:
    @pytest.mark.parametrize("n", [4, 9])
    def test_generate_random_string(self, n):
        random_string = generate_random_string(n)
        assert isinstance(random_string, str) and len(random_string) == n
