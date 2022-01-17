import pytest
from config import Config


@pytest.mark.gen_test
async def test_hello_world(http_client, base_url):
    # arrange
    url = f"{base_url}{Config.API_BASE_URL}/"

    # act
    response = await http_client.fetch(url)

    # assert
    assert response.code == 200
