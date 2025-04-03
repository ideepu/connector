from typing import Any

import pytest

from src.account import AccountList
from src.advertisement import AdvertisementList
from tests.mock import MockModelList


@pytest.fixture
def mock_model_list() -> MockModelList:
    data: list[Any] = [
        {
            'key1': 'value1',
            'key2': 1,
            'key3': '2025-04-03',
        },
        {
            'key1': 'value1',
            'key2': 2,
            'key3': '2025-04-03',
        },
        {
            'key1': 'value2',
            'key2': 3,
            'key3': '2025-04-03',
        },
        {
            'key1': 'value3',
            'key2': 4,
            'key3': '2025-04-04',
        },
    ]
    return MockModelList(data)


@pytest.fixture
def mock_account_list() -> AccountList:
    data: list[Any] = [
        {
            'name': 'Test Account 1',
            'id': '12345',
        },
        {
            'name': 'Test Account 2',
            'id': '67890',
        },
    ]
    return AccountList(data)


@pytest.fixture
def mock_advertisement_list() -> AdvertisementList:
    data: list[Any] = [
        {
            'date': '2023-01-01',
            'campaign_id': '12345',
            'impressions': 100,
            'clicks': 10,
            'conversions': 5,
            'cost': 0.0,
        },
        {
            'date': '2023-01-02',
            'campaign_id': '67890',
            'impressions': 200,
            'clicks': 20,
            'conversions': 10,
            'cost': 1.0,
        },
    ]
    return AdvertisementList(data)
