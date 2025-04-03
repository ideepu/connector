from datetime import date
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from src.account import AccountList
from src.advertisement import AdvertisementList, AdvertisementSerialized
from src.connector import Connector
from src.exception import InvalidInputDataException


class TestConnector:
    @patch('src.account.AccountManager.get_ad_accounts')
    @patch('src.advertisement.AdvertisementManager.get_data')
    def test_init_failed(
        self,
        mock_get_ad_data: MagicMock,
        mock_get_accounts: MagicMock,
        mock_account_list: AccountList,
    ):
        account_id: Any = 2342
        start: Any = '2023-01-01'
        end: Any = '2023-01-31'
        start_date = date.fromisoformat(start)
        end_date = date.fromisoformat(end)
        with pytest.raises(InvalidInputDataException):
            Connector(account_id=account_id, start=start_date, end=end_date)
        with pytest.raises(InvalidInputDataException):
            Connector(start=start, end=end_date)
        with pytest.raises(InvalidInputDataException):
            Connector(start=start_date, end=end)
        mock_get_accounts.assert_not_called()
        mock_get_ad_data.assert_not_called()
        mock_get_accounts.return_value = []

        # No accounts
        with pytest.raises(InvalidInputDataException):
            Connector(start=start_date, end=end_date)
        mock_get_accounts.assert_called_once()
        mock_get_ad_data.assert_not_called()
        mock_get_accounts.reset_mock(return_value=True)

        # Incorrect account ID
        mock_get_accounts.return_value = mock_account_list
        with pytest.raises(InvalidInputDataException):
            Connector(account_id='incorrect_account_id', start=start_date, end=end_date)
        mock_get_accounts.assert_called_once()
        mock_get_ad_data.assert_not_called()
        mock_get_accounts.reset_mock()

        # Ad data not founds
        mock_get_ad_data.return_value = []
        with pytest.raises(InvalidInputDataException):
            Connector(account_id=mock_account_list[0].id, start=start_date, end=end_date)
        mock_get_accounts.assert_called_once()
        mock_get_ad_data.assert_called_once_with(
            mock_account_list[0].id,
            start=start_date,
            end=end_date,
        )

    @patch('src.account.AccountManager.get_ad_accounts')
    @patch('src.advertisement.AdvertisementManager.get_data')
    def test_init(
        self,
        mock_get_ad_data: MagicMock,
        mock_get_accounts: MagicMock,
        mock_account_list: AccountList,
        mock_advertisement_list: AdvertisementList,
    ):
        # Valid account ID
        account_id = mock_account_list[0].id
        start: Any = '2023-01-01'
        end: Any = '2023-01-31'
        start_date = date.fromisoformat(start)
        end_date = date.fromisoformat(end)
        mock_get_accounts.return_value = mock_account_list
        mock_get_ad_data.return_value = mock_advertisement_list
        connector = Connector(account_id=account_id, start=start_date, end=end_date)
        assert connector.account_id == mock_account_list[0].id
        assert connector.accounts == mock_account_list
        assert connector.account == mock_account_list[0]
        assert connector.account_ads_data == mock_advertisement_list
        mock_get_accounts.assert_called_once()
        mock_get_ad_data.assert_called_once_with(
            mock_account_list[0].id,
            start=connector.start,
            end=connector.end,
        )
        mock_get_accounts.reset_mock()
        mock_get_ad_data.reset_mock()

        # Valid random account
        connector = Connector(start=start_date, end=end_date)
        assert connector.account in mock_account_list
        assert connector.account_ads_data == mock_advertisement_list
        mock_get_accounts.assert_called_once()
        mock_get_ad_data.assert_called_once_with(
            connector.account.id,
            start=connector.start,
            end=connector.end,
        )

    @patch('src.account.AccountManager.get_ad_accounts')
    @patch('src.advertisement.AdvertisementManager.get_data')
    def test_serialize_ads(
        self,
        mock_get_ad_data: MagicMock,
        mock_get_accounts: MagicMock,
        mock_account_list: AccountList,
        mock_advertisement_list: AdvertisementList,
    ):
        start: Any = '2023-01-01'
        end: Any = '2023-01-31'
        start_date = date.fromisoformat(start)
        end_date = date.fromisoformat(end)
        mock_get_accounts.return_value = mock_account_list
        mock_get_ad_data.return_value = mock_advertisement_list
        connector = Connector(start=start_date, end=end_date)
        serialized_ads = connector._serialize_ads()  # pylint: disable=protected-access
        assert isinstance(serialized_ads, AdvertisementSerialized)
        assert serialized_ads.headers == list(mock_advertisement_list[0].model_dump(by_alias=True).keys())
        assert serialized_ads.rows == [list(ad.model_dump(by_alias=True).values()) for ad in mock_advertisement_list]
