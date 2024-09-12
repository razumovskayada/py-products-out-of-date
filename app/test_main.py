import pytest

import datetime

from app.main import outdated_products

from unittest import mock


@pytest.fixture()
def mock_today_datetime() -> None:
    with mock.patch("datetime.date") as mock_today_date:
        yield mock_today_date


@pytest.mark.parametrize(
    "products,result,today_date",
    [
        (
            [
                {
                    "name": "salmon",
                    "expiration_date": datetime.date(2022, 2, 10),
                    "price": 600
                }
            ],
            [], datetime.date(2022, 2, 9)
        ),
        (
            [
                {
                    "name": "salmon",
                    "expiration_date": datetime.date(2022, 2, 10),
                    "price": 600
                }
            ],
            [], datetime.date(2022, 2, 10)
        ),
        (
            [
                {
                    "name": "chicken",
                    "expiration_date": datetime.date(2022, 2, 5),
                    "price": 120
                }
            ],
            ["chicken"], datetime.date(2022, 2, 6)
        ),
    ],
    ids=[
        "should return empty list if both element "
        "expiration date is bigger than today's date",
        "should return empty list when "
        "expiration date equals today's date",
        "should return product's name when "
        "today's date is bigger than expiration date",
    ]
)
def test_if_product_is_outdated_with_different_dates(
        products: list,
        result: list,
        today_date: callable,
        mock_today_datetime: callable
) -> None:
    mock_today_datetime.return_value = products[0]["expiration_date"]
    mock_today_datetime.today.return_value = today_date
    assert outdated_products(products) == result
