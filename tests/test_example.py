import pytest


@pytest.mark.django_db()  # noqa: PT023
def test_example():
	assert 1 + 1 == 2  # noqa: PLR2004
