import json
from unittest.mock import MagicMock

import pytest
from stripe import Price, Product

from config import Config
from utils.auth import create_jwt_token


@pytest.mark.gen_test
async def test_products_get_unauthorized(http_client, base_url):
    # arrange
    url = f"{base_url}{Config.API_BASE_URL}/products"

    # act
    response = await http_client.fetch(
        url,
        method="GET",
        raise_error=False,
    )

    # assert
    response_body = json.loads(response.body)
    assert response.code == 401
    assert response_body["message"].startswith("Missing Authorization")


@pytest.mark.gen_test
async def test_products_get_ok(http_client, base_url, monkeypatch):
    # arrange
    url = f"{base_url}{Config.API_BASE_URL}/products"
    token = create_jwt_token("test_username")
    products = {
        "data": [
            {
                "id": "product_1",
                "active": True,
                "description": "product 1 description",
                "name": "product 1 name",
            },
            {
                "id": "product_2",
                "active": True,
                "description": "product 2 description",
                "name": "product 2 name",
            },
            {
                "id": "product_3",
                "active": True,
                "description": "product 3 description",
                "name": "product 3 name",
            },
        ]
    }

    prices = {
        "data": [
            {
                "currency": "eur",
                "unit_amount": 100,
            }
        ]
    }

    _product_list_mock = MagicMock(return_value=products)
    monkeypatch.setattr(Product, "list", _product_list_mock)

    _price_list_mock = MagicMock(return_value=prices)
    monkeypatch.setattr(Price, "list", _price_list_mock)

    # act
    response = await http_client.fetch(
        url,
        method="GET",
        headers={"Authorization": f"Bearer {token}"},
        raise_error=False,
    )

    # assert
    response_body = json.loads(response.body)
    assert response.code == 200
    assert response_body == {"data": [{**p, "price": prices["data"][0]} for p in products["data"]]}
