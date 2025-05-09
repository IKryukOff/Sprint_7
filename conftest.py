from typing import Any

import pytest
from data import order
from faker import Faker


@pytest.fixture()
def courier_data() -> dict[str, str]:
    fake = Faker()
    return {'login': fake.user_name(),
            'password': fake.password(),
            'firstName': fake.file_name()}


@pytest.fixture()
def order_data() -> dict[str, Any]:
    return order.order_data
