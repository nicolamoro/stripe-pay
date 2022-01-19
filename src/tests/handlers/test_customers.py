import json
from unittest.mock import MagicMock

import pytest
from stripe import Customer
from stripe.error import InvalidRequestError

from config import Config


@pytest.mark.gen_test
async def test_customers_post_invalid_data(http_client, base_url):
    # arrange
    url = f"{base_url}{Config.API_BASE_URL}/customers"
    request_body = json.dumps({})

    # act
    response = await http_client.fetch(
        url,
        method="POST",
        body=request_body,
        raise_error=False,
    )

    # assert
    response_body = json.loads(response.body)
    assert response.code == 400
    assert response_body["message"].startswith("Invalid data")


@pytest.mark.gen_test
async def test_customers_post_already_present(http_client, base_url, monkeypatch):
    # arrange
    url = f"{base_url}{Config.API_BASE_URL}/customers"
    request_body = json.dumps(
        {
            "id": "test_username",
            "password": "test_password",
            "email": "test@user.com",
            "name": "Test User",
            "phone": "+391234567890",
        }
    )

    _create_mock = MagicMock(
        side_effect=InvalidRequestError(
            "Customer already exists.",
            None,
        )
    )
    monkeypatch.setattr(Customer, "create", _create_mock)

    # act
    response = await http_client.fetch(
        url,
        method="POST",
        body=request_body,
        raise_error=False,
    )

    # assert
    response_body = json.loads(response.body)
    assert response.code == 400
    assert response_body["message"].startswith("Customer already exists")


@pytest.mark.gen_test
async def test_customers_post_ok(http_client, base_url, monkeypatch):
    # arrange
    url = f"{base_url}{Config.API_BASE_URL}/customers"
    customer = {
        "id": "test_username",
        "password": "test_password",
        "email": "test@user.com",
        "name": "Test User",
        "phone": "+391234567890",
    }
    request_body = json.dumps(customer)

    _create_mock = MagicMock(return_value=customer)
    monkeypatch.setattr(Customer, "create", _create_mock)

    # act
    response = await http_client.fetch(
        url,
        method="POST",
        body=request_body,
        raise_error=False,
    )

    # assert
    response_body = json.loads(response.body)
    assert response.code == 201
    assert response_body == {k: v for k, v in customer.items() if k not in ["password"]}
