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


class AccountManager(BaseModel):
    request: ClassVar = BaseRequest(
        base_url=f'{config.BASE_URL}/demo',
        supported_methods=['GET'],
    )

    @classmethod
    def get_ad_accounts(cls) -> AccountList:
        response = cls.request.get(url='/adAccounts')
        return AccountList.model_validate(response['ad_accounts'])
