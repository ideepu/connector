import random
from datetime import date, timedelta

from src.account import AccountManager
from src.advertisement import Advertisement, AdvertisementManager, AdvertisementStructured


class Connector:
    def __init__(self, account_id: str = None, start: date = None, end: date = None):
        self.account_id = account_id
        self.start = start
        self.end = end

    def run(self):
        accounts = AccountManager.get_ad_accounts()
        print(accounts.model_dump_json(indent=8, by_alias=True))
        account = random.choice(accounts)

        start = date.today() - timedelta(days=random.randint(30, 60))
        end = date.today() - timedelta(days=random.randint(0, 30))
        account_ads_data = AdvertisementManager.get_data(account.id, start=start, end=end)
        if not account_ads_data:
            print('No data found')
            return
        grouped_by_date_data = account_ads_data.group_by(keys=('date', 'campaign_id'))

        headers = list(account_ads_data.first().model_dump(by_alias=True).keys())
        aggregated_rows: list[dict] = []
        for group in grouped_by_date_data:
            if not group:
                continue
            aggregated_data = group.aggregate(keys=('impressions', 'clicks', 'conversions', 'cost'))
            aggregated_data['date'] = group.first().date
            aggregated_data['campaign_id'] = group.first().campaign_id
            ad_data = Advertisement.model_validate(aggregated_data)
            aggregated_rows.append(list(ad_data.model_dump().values()))

        structured_data = AdvertisementStructured(headers=headers, rows=aggregated_rows)
        print(structured_data.model_dump_json(indent=8))
