from datetime import date
from unittest.mock import MagicMock, patch

import pytest

from src.advertisement import Advertisement, AdvertisementList, AdvertisementManager, AdvertisementSerialized
from src.exception import InvalidInputDataException


class TestAdvertisement:
    def test_advertisement_init_invalid(self):
        with pytest.raises(ValueError):
            Advertisement(date=None, campaign_id=None, impressions=None, clicks=None, conversions=None, cost=None)

        with pytest.raises(ValueError):
            Advertisement(date='2023-01-01', campaign_id=12345, impressions='100', clicks=10, conversions=5, cost=0.0)

        with pytest.raises(ValueError):
            Advertisement(date='2023-01-01', campaign_id='12345', impressions=-1, clicks=-10, conversions=-5, cost=-2.0)

    def test_advertisement_init(self):
        ad = Advertisement(date='2023-01-01', campaign_id='12345', impressions=100, clicks=10, conversions=5, cost=0.0)
        assert ad.date == date(2023, 1, 1)
        assert ad.campaign_id == '12345'
        assert ad.impressions == 100
        assert ad.clicks == 10
        assert ad.conversions == 5
        assert ad.cost == 0.0

        ad_dict = ad.model_dump(by_alias=True)
        assert ad_dict['date'] == date(2023, 1, 1)
        assert ad_dict['campaignId'] == '12345'
        assert ad_dict['impressions'] == 100
        assert ad_dict['clicks'] == 10
        assert ad_dict['conversions'] == 5
        assert ad_dict['cost'] == 0.0


class TestAdvertisementList:
    def test_advertisement_list_invalid(self):
        with pytest.raises(ValueError):
            AdvertisementList(
                [
                    {
                        'date': '2023-01-01',
                        'campaign_id': None,
                        'impressions': 100,
                        'clicks': 10,
                        'conversions': 5,
                        'cost': 0.0,
                    }
                ]
            )

    def test_advertisement_list_init(self):
        ad1 = Advertisement(
            date='2023-01-01',
            campaign_id='12345',
            impressions=100,
            clicks=10,
            conversions=5,
            cost=0.0,
        )
        ad2 = Advertisement(
            date='2023-01-02',
            campaign_id='67890',
            impressions=200,
            clicks=20,
            conversions=10,
            cost=1.0,
        )
        ad_list = [ad1, ad2]

        ad_list_model = AdvertisementList.model_validate(ad_list)
        assert len(ad_list_model) == 2
        assert ad_list_model[0] == ad1
        assert ad_list_model[1] == ad2

        ad_list_dict = ad_list_model.model_dump(by_alias=True)
        assert ad_list_dict[0]['campaignId'] == ad1.campaign_id
        assert ad_list_dict[1]['campaignId'] == ad2.campaign_id


class TestAdvertisementSerialized:
    def test_init_invalid(self):
        with pytest.raises(ValueError):
            AdvertisementSerialized(headers=None, rows=None)

        with pytest.raises(ValueError):
            AdvertisementSerialized(headers=['header1', 'header2'], rows=[None])

    def test_init(self):
        headers = ['header1', 'header2']
        rows = [['row1_col1', 'row1_col2'], ['row2_col1', 'row2_col2']]
        serialized_ads = AdvertisementSerialized(headers=headers, rows=rows)

        assert serialized_ads.headers == headers
        assert serialized_ads.rows == rows

        serialized_ads_dict = serialized_ads.model_dump(by_alias=True)
        assert serialized_ads_dict['headers'] == headers
        assert serialized_ads_dict['rows'] == rows

        # With models
        ad1 = Advertisement(
            date='2023-01-01',
            campaign_id='12345',
            impressions=100,
            clicks=10,
            conversions=5,
            cost=0.0,
        )
        ad2 = Advertisement(
            date='2023-01-02',
            campaign_id='67890',
            impressions=200,
            clicks=20,
            conversions=10,
            cost=1.0,
        )
        headers = list(ad1.model_dump(by_alias=True).keys())
        rows = [list(ad1.model_dump(by_alias=True).values()), list(ad2.model_dump(by_alias=True).values())]
        serialized_ads = AdvertisementSerialized(headers=headers, rows=rows)
        assert serialized_ads.headers == headers
        assert serialized_ads.rows == rows

        serialized_ads_dict = serialized_ads.model_dump(by_alias=True)
        assert serialized_ads_dict['headers'] == headers
        assert serialized_ads_dict['rows'] == rows


class TestAdvertisementManager:
    @patch('src.advertisement.AdvertisementManager.request.get')
    def test_get_data(self, advertisement_manager_request_get_mock: MagicMock):
        with pytest.raises(InvalidInputDataException):
            AdvertisementManager.get_data(acount_id='12345', start=date(2025, 4, 8), end=date(2025, 4, 8))

        with pytest.raises(InvalidInputDataException):
            advertisement_manager_request_get_mock.return_value = {}
            AdvertisementManager.get_data(acount_id='12345', start=date(2025, 4, 8), end=date(2025, 4, 8))

        with pytest.raises(InvalidInputDataException):
            advertisement_manager_request_get_mock.return_value = {
                'invalid_key': [
                    {
                        'campaign_id': '2025',
                        'clicks': 43,
                        'conversions': 4,
                        'cost': 83.18,
                        'date': '2025-04-08',
                        'impressions': 166,
                    },
                ]
            }
            AdvertisementManager.get_data(acount_id='12345', start=date(2025, 4, 8), end=date(2025, 4, 8))

        advertisement_manager_request_get_mock.reset_mock()
        advertisement_manager_request_get_mock.return_value = {
            'data': [
                {
                    'campaign_id': '2025',
                    'clicks': 43,
                    'conversions': 4,
                    'cost': 83.18,
                    'date': '2025-04-08',
                    'impressions': 166,
                },
                {
                    'campaign_id': '2025',
                    'clicks': 51,
                    'conversions': 7,
                    'cost': 21.31,
                    'date': '2025-04-08',
                    'impressions': 388,
                },
                {
                    'campaign_id': '2025',
                    'clicks': 19,
                    'conversions': 0,
                    'cost': 25.54,
                    'date': '2025-04-08',
                    'impressions': 354,
                },
            ]
        }
        AdvertisementManager.get_data(acount_id='12345', start=date(2025, 4, 8), end=date(2025, 4, 8))
        advertisement_manager_request_get_mock.assert_called_once_with(
            url='/getData/12345', params={'start': '2025-04-08', 'end': '2025-04-08'}
        )
