import json
from unittest.mock import MagicMock

import pytest
from stripe import Customer
from stripe.error import InvalidRequestError

from config import Config


@pytest.mark.gen_test
async def test_login_post_invalid_data(http_client, base_url):
    # arrange
    url = f"{base_url}{Config.API_BASE_URL}/login"
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
async def test_login_post_user_not_found(http_client, base_url, monkeypatch):
    # arrange
    url = f"{base_url}{Config.API_BASE_URL}/login"
    request_body = json.dumps({"username": "test_username", "password": "test_password"})

    _retrieve_mock = MagicMock(
        side_effect=InvalidRequestError(
            "No such customer: 'test_username'",
            "id",
        )
    )
    monkeypatch.setattr(Customer, "retrieve", _retrieve_mock)

    # act
    response = await http_client.fetch(
        url,
        method="POST",
        body=request_body,
        raise_error=False,
    )

    # assert
    response_body = json.loads(response.body)
    assert response.code == 401
    assert response_body["message"].startswith("User not found")


@pytest.mark.gen_test
async def test_login_post_user_invalid_password(http_client, base_url, monkeypatch):
    # arrange
    url = f"{base_url}{Config.API_BASE_URL}/login"
    request_body = json.dumps({"username": "test_username", "password": "test_password"})
    customer = {"metadata": {"password": "some_password_hash"}}

    _retrieve_mock = MagicMock(return_value=customer)
    monkeypatch.setattr(Customer, "retrieve", _retrieve_mock)

    # act
    response = await http_client.fetch(
        url,
        method="POST",
        body=request_body,
        raise_error=False,
    )

    # assert
    response_body = json.loads(response.body)
    assert response.code == 401
    assert response_body["message"].startswith("Invalid password")


@pytest.mark.gen_test
async def test_login_post_user_ok(http_client, base_url, monkeypatch):
    # arrange
    url = f"{base_url}{Config.API_BASE_URL}/login"
    request_body = json.dumps({"username": "test_username", "password": "test_password"})
    customer = {"metadata": {"password": "2af5628f591780eda39399a4d6b58395b07246a8c76f768633a5966c1caa28d2"}}

    _retrieve_mock = MagicMock(return_value=customer)
    monkeypatch.setattr(Customer, "retrieve", _retrieve_mock)

    # act
    response = await http_client.fetch(
        url,
        method="POST",
        body=request_body,
        raise_error=False,
    )

    # assert
    response_body = json.loads(response.body)
    assert response.code == 200
    assert response_body.get("access_token") is not None
