import pytest
from httpx import AsyncClient, ASGITransport

from boaviztapi.main import app

pytest_plugins = ("pytest_asyncio",)


def _body(storage_type="SSD", storage=1000, replication=1, **configuration):
    return {
        "configuration": {
            "storage_type": storage_type,
            "replication": replication,
            **configuration,
        },
        "usage": {"storage": storage, "usage_location": "FRA"},
    }


async def _post(body, **params):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        return await client.post("/v1/storage", json=body, params=params)


@pytest.mark.asyncio
async def test_storage_impact_is_linear_in_storage_and_replication():
    single = await _post(_body(storage=1000, replication=1), verbose=False)
    double = await _post(_body(storage=2000, replication=2), verbose=False)
    single_gwp = single.json()["impacts"]["gwp"]["embedded"]["value"]
    double_gwp = double.json()["impacts"]["gwp"]["embedded"]["value"]
    assert double_gwp == pytest.approx(4 * single_gwp)


@pytest.mark.asyncio
async def test_verbose_output_is_returned_by_default():
    response = await _post(_body())
    assert response.status_code == 200
    assert "verbose" in response.json()


@pytest.mark.asyncio
async def test_unsupported_storage_type_is_rejected():
    response = await _post(_body(storage_type="S3"))
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_hdd_response_carries_flat_impact_warning():
    response = await _post(_body(storage_type="HDD"), verbose=False)
    assert response.status_code == 200
    assert "HDD impact does not vary with capacity" in response.text
