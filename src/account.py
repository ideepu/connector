from pydantic import Field

from src.base import BaseManager, BaseModel, BaseModelList
from src.exception import InvalidInputDataException


class Account(BaseModel):
    name: str = Field(serialization_alias='accountName')
    id: str = Field(serialization_alias='accountId')


class AccountList(BaseModelList[Account]):
    pass


class AccountManager(BaseManager):
    @classmethod
    def get_ad_accounts(cls) -> AccountList:
        response = cls.request.get(url='/adAccounts')
        if not (response and 'ad_accounts' in response):
            raise InvalidInputDataException('Invalid response data')
        return AccountList.model_validate(response['ad_accounts'])
