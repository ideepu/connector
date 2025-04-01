from src.account import AdAccount


class Connector:
    def run(self):
        ad_accounts = AdAccount.get_ad_accounts()
        print(ad_accounts.ad_accounts.model_dump_json(indent=8, by_alias=True))
