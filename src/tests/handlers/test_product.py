import json
from unittest.mock import MagicMock

import pytest
from stripe import Customer, PaymentIntent, Price, Product
from stripe.error import InvalidRequestError

from config import Config
from utils.auth import create_jwt_token


@pytest.mark.gen_test
async def test_product_purchase_post_unauthorized(http_client, base_url):
    # arrange
    url = f"{base_url}{Config.API_BASE_URL}/products/test_product/purchase"
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
    assert response.code == 401
    assert response_body["message"].startswith("Missing Authorization")


@pytest.mark.gen_test
async def test_product_purchase_post_error_on_customer(http_client, base_url, monkeypatch):
    # arrange
    url = f"{base_url}{Config.API_BASE_URL}/products/test_product/purchase"
    token = create_jwt_token("test_username")
    request_body = json.dumps({})

    _customer_retrieve_mock = MagicMock(
        side_effect=InvalidRequestError(
            "No such customer: 'test_username'",
            "id",
        )
    )
    monkeypatch.setattr(Customer, "retrieve", _customer_retrieve_mock)

    # act
    response = await http_client.fetch(
        url,
        method="POST",
        body=request_body,
        headers={"Authorization": f"Bearer {token}"},
        raise_error=False,
    )

    # assert
    response_body = json.loads(response.body)
    assert response.code == 400
    assert response_body["message"].startswith("No such customer: 'test_username'")


@pytest.mark.gen_test
async def test_product_purchase_post_error_on_payment_intent(http_client, base_url, monkeypatch):
    # arrange
    url = f"{base_url}{Config.API_BASE_URL}/products/test_product/purchase"
    token = create_jwt_token("test_username")
    request_body = json.dumps({})

    customer = {
        "id": "test_username",
        "email": "test@user.com",
        "name": "Test User",
        "phone": "+391234567890",
    }
    product = {
        "id": "product_1",
        "active": True,
        "description": "product 1 description",
        "name": "product 1 name",
    }
    prices = {
        "data": [
            {
                "currency": "eur",
                "unit_amount": 100,
            }
        ]
    }

    _customer_retrieve_mock = MagicMock(return_value=customer)
    monkeypatch.setattr(Customer, "retrieve", _customer_retrieve_mock)

    _product_retrieve_mock = MagicMock(return_value=product)
    monkeypatch.setattr(Product, "retrieve", _product_retrieve_mock)

    _price_list_mock = MagicMock(return_value=prices)
    monkeypatch.setattr(Price, "list", _price_list_mock)

    _payment_intent_create_mock = MagicMock(
        side_effect=InvalidRequestError(
            "Error on Payment Intent",
            None,
        )
    )
    monkeypatch.setattr(PaymentIntent, "create", _payment_intent_create_mock)

    # act
    response = await http_client.fetch(
        url,
        method="POST",
        body=request_body,
        headers={"Authorization": f"Bearer {token}"},
        raise_error=False,
    )

    # assert
    response_body = json.loads(response.body)
    assert response.code == 400
    assert response_body["message"].startswith("Error on Payment Intent")


@pytest.mark.gen_test
async def test_product_purchase_post_ok(http_client, base_url, monkeypatch):
    # arrange
    url = f"{base_url}{Config.API_BASE_URL}/products/test_product/purchase"
    token = create_jwt_token("test_username")
    request_body = json.dumps({})

    customer = {
        "id": "test_username",
        "email": "test@user.com",
        "name": "Test User",
        "phone": "+391234567890",
    }
    product = {
        "id": "product_1",
        "active": True,
        "description": "product 1 description",
        "name": "product 1 name",
    }
    prices = {
        "data": [
            {
                "currency": "eur",
                "unit_amount": 100,
            }
        ]
    }
    payment_intent = {
        "id": "payment-intent-id",
        "amount": 100,
        "currency": "eur",
        "customer": "test_username",
        "receipt_email": "test@user.com",
        "status": "success",
    }

    _customer_retrieve_mock = MagicMock(return_value=customer)
    monkeypatch.setattr(Customer, "retrieve", _customer_retrieve_mock)

    _product_retrieve_mock = MagicMock(return_value=product)
    monkeypatch.setattr(Product, "retrieve", _product_retrieve_mock)

    _price_list_mock = MagicMock(return_value=prices)
    monkeypatch.setattr(Price, "list", _price_list_mock)

    _payment_intent_create_mock = MagicMock(return_value=payment_intent)
    monkeypatch.setattr(PaymentIntent, "create", _payment_intent_create_mock)

    # act
    response = await http_client.fetch(
        url,
        method="POST",
        body=request_body,
        headers={"Authorization": f"Bearer {token}"},
        raise_error=False,
    )

    # assert
    response_body = json.loads(response.body)
    assert response.code == 200
    assert response_body == payment_intent
