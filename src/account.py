from typing import ClassVar

from pydantic import Field

from src.base import BaseModel, BaseModelList
from src.config import config
from src.libs.request import BaseRequest


class Account(BaseModel):
    name: str = Field(serialization_alias='accountName')
    id: str = Field(serialization_alias='accountId')


class AccountList(BaseModelList[Account]):
    pass


class AdAccount(BaseModel):
    accounts_request: ClassVar = BaseRequest(
        base_url=f'{config.BASE_URL}/demo',
        supported_methods=['GET'],
    )

    ad_accounts: AccountList

    @classmethod
    def get_ad_accounts(cls) -> 'AdAccount':
        response = cls.accounts_request.get(url='/adAccounts')
        return cls.model_validate(response)
