import random
from datetime import date
from typing import Any

from src.account import Account, AccountList, AccountManager
from src.advertisement import AdvertisementList, AdvertisementManager, AdvertisementSerialized
from src.exception import InvalidInputDataException


class Connector:
    def __init__(self, start: date, end: date, account_id: str = None):
        self.account_id = account_id
        self.start = start
        self.end = end
        self._init_input()
        self.accounts: AccountList = self._get_accounts()
        self.account: Account = self._get_target_account()
        self.account_ads_data: AdvertisementList = self._get_account_ad_data()

    def _init_input(self):
        if not (isinstance(self.start, date) and isinstance(self.end, date)):
            raise InvalidInputDataException('Start and end dates should be of type date')

        if self.account_id and not isinstance(self.account_id, str):
            raise InvalidInputDataException(f'Account ID {self.account_id} should be a string')

    def _get_accounts(self):
        accounts = AccountManager.get_ad_accounts()
        if not accounts:
            raise InvalidInputDataException('No accounts found')
        return accounts

    def _get_target_account(self):
        if self.account_id:
            account = self.accounts.get_by_key_value(key='id', value=self.account_id)
            if not account:
                raise InvalidInputDataException(f'Account with id {self.account_id} not found')
            return account
        return random.choice(self.accounts)

    def _get_account_ad_data(self):
        ads_data = AdvertisementManager.get_data(self.account.id, start=self.start, end=self.end)
        if not ads_data:
            raise InvalidInputDataException('No ads data found')
        return ads_data

    def run(self):
        self._print(self.accounts)
        serialized_ads = self._serialize_ads()
        self._print(serialized_ads)

    def _print(self, model: AccountList | AdvertisementSerialized, by_alias=True):
        print(model.model_dump_json(indent=8, by_alias=by_alias))

    def _serialize_ads(self) -> AdvertisementSerialized:
        aggregated_account_ads_dict: list[Any] = self.account_ads_data.groupby_aggregate(
            group_by=['date', 'campaign_id'],
            aggregate_by=['impressions', 'clicks', 'conversions', 'cost'],
        )
        aggregated_account_ads_data = AdvertisementList(aggregated_account_ads_dict)
        headers = list(aggregated_account_ads_data[0].model_dump(by_alias=True).keys())
        aggregated_rows = [list(item.model_dump().values()) for item in aggregated_account_ads_data]
        return AdvertisementSerialized(headers=headers, rows=aggregated_rows)
