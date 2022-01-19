import json
from unittest.mock import MagicMock

import pytest
from stripe import Customer
from stripe.error import InvalidRequestError

from config import Config
from utils.auth import create_jwt_token


@pytest.mark.gen_test
async def test_customer_delete_unauthorized(http_client, base_url):
    # arrange
    url = f"{base_url}{Config.API_BASE_URL}/customers/test_username"

    # act
    response = await http_client.fetch(
        url,
        method="DELETE",
        raise_error=False,
    )

    # assert
    response_body = json.loads(response.body)
    assert response.code == 401
    assert response_body["message"].startswith("Missing Authorization")


@pytest.mark.gen_test
async def test_customer_delete_different_user(http_client, base_url):
    # arrange
    url = f"{base_url}{Config.API_BASE_URL}/customers/test_username"
    token = create_jwt_token("test_username_2")

    # act
    response = await http_client.fetch(
        url,
        method="DELETE",
        headers={"Authorization": f"Bearer {token}"},
        raise_error=False,
    )

    # assert
    response_body = json.loads(response.body)
    assert response.code == 403
    assert response_body["message"].startswith("Forbidden to delete a customer other than yourself")


@pytest.mark.gen_test
async def test_customer_delete_not_found(http_client, base_url, monkeypatch):
    # arrange
    url = f"{base_url}{Config.API_BASE_URL}/customers/test_username"
    token = create_jwt_token("test_username")

    _delete_mock = MagicMock(
        side_effect=InvalidRequestError(
            "No such customer: 'test_username'",
            "id",
        )
    )
    monkeypatch.setattr(Customer, "delete", _delete_mock)

    # act
    response = await http_client.fetch(
        url,
        method="DELETE",
        headers={"Authorization": f"Bearer {token}"},
        raise_error=False,
    )

    # assert
    response_body = json.loads(response.body)
    assert response.code == 400
    assert response_body["message"].startswith("No such customer: 'test_username'")


@pytest.mark.gen_test
async def test_customer_delete_ok(http_client, base_url, monkeypatch):
    # arrange
    url = f"{base_url}{Config.API_BASE_URL}/customers/test_username"
    token = create_jwt_token("test_username")

    _delete_mock = MagicMock()
    monkeypatch.setattr(Customer, "delete", _delete_mock)

    # act
    response = await http_client.fetch(
        url,
        method="DELETE",
        headers={"Authorization": f"Bearer {token}"},
        raise_error=False,
    )

    # assert
    assert response.code == 204
