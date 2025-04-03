from datetime import date
from typing import Any

from pydantic import Field

from src.base import BaseManager, BaseModel, BaseModelList
from src.exception import InvalidInputDataException


class Advertisement(BaseModel):
    date: date
    campaign_id: str = Field(serialization_alias='campaignId')
    impressions: int = Field(ge=0)
    clicks: int = Field(ge=0)
    conversions: int = Field(ge=0)
    cost: float = Field(ge=0)


class AdvertisementList(BaseModelList[Advertisement]):
    pass


class AdvertisementSerialized(BaseModel):
    headers: list[str]
    rows: list[list[Any]]


class AdvertisementManager(BaseManager):
    @classmethod
    def get_data(cls, acount_id: str, start: date, end: date) -> AdvertisementList:
        if start > end:
            raise InvalidInputDataException(f'Start date {start} should be less than or equal to end date {end}')

        response = cls.request.get(url=f'/getData/{acount_id}', params={'start': str(start), 'end': str(end)})
        if not (response and 'data' in response):
            raise InvalidInputDataException('Invalid response data')

        return AdvertisementList.model_validate(response['data'])
