import random
from datetime import date, timedelta

from src.account import Account, AccountList, AccountManager
from src.advertisement import AdvertisementList, AdvertisementManager, AdvertisementSerialized
from src.exception import InvalidInputDataException


class Connector:
    def __init__(self, account_id: str = None, start: date = None, end: date = None):
        self.account_id = account_id
        self.start = start or date.today() - timedelta(days=random.randint(3, 6))
        self.end = end or date.today() - timedelta(days=random.randint(0, 3))
        self.accounts: AccountList = self._get_accounts()
        self.account: Account = self._get_target_account()
        self.account_ads_data: AdvertisementList = self._get_account_ad_data()

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

    def _print(self, model: AccountList | AdvertisementSerialized, by_alias=True):
        print(model.model_dump_json(indent=8, by_alias=by_alias))

    def _serialize_ads(self):
        aggregated_account_ads_data = self.account_ads_data.groupby_aggregate(
            group_by=['date', 'campaign_id'],
            aggregate_by=['impressions', 'clicks', 'conversions', 'cost'],
        )
        headers = list(aggregated_account_ads_data[0].model_dump(by_alias=True).keys())
        aggregated_rows = [list(item.model_dump().values()) for item in aggregated_account_ads_data]
        return AdvertisementSerialized(headers=headers, rows=aggregated_rows)

    def run(self):
        self._print(self.accounts)
        serialized_ads = self._serialize_ads()
        self._print(serialized_ads)
