from datetime import date
from typing import Any, ClassVar

from pydantic import Field

from src.base import BaseModel, BaseModelList
from src.config import config
from src.exception import InvalidInputDataException
from src.libs.request import BaseRequest


class Advertisement(BaseModel):
    date: date
    campaign_id: str = Field(serialization_alias='campaignId')
    impressions: int = Field(ge=0)
    clicks: int = Field(ge=0)
    conversions: int = Field(ge=0)
    cost: float = Field(ge=0)


class AdvertisementList(BaseModelList[Advertisement]):
    pass


class AdvertisementStructured(BaseModel):
    headers: list[str]
    rows: list[list[Any]]


class AdvertisementManager(BaseModel):
    request: ClassVar = BaseRequest(
        base_url=f'{config.BASE_URL}/demo',
        supported_methods=['GET'],
    )

    @classmethod
    def get_data(cls, acount_id: str, start: date, end: date) -> AdvertisementList:
        if start > end:
            raise InvalidInputDataException(f'Start date {start} should be less than or equal to end date {end}')

        response = cls.request.get(url=f'/getData/{acount_id}', params={'start': str(start), 'end': str(end)})
        # TODO:
        # if not response or not response.get('data'):
        #     return AdvertisementList()
        return AdvertisementList.model_validate(response['data'])
