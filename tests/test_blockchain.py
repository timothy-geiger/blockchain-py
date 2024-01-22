import pytest


class TestBlockchain:
    @pytest.mark.parametrize('sender, recipient, amount', [
        ('1', '2', 5),
        ('2', '3', 5)
    ])
    def test_transactions(self, sender, recipient, amount):
        assert sender != recipient
