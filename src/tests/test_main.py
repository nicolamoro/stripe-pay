import pytest


@pytest.mark.gen_test
async def test_hello_world(http_client, base_url):
    response = await http_client.fetch(base_url)
    assert response.code == 200
