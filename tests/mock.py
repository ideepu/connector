from datetime import date

from src.base import BaseModel, BaseModelList


class MockModel(BaseModel):
    key1: str
    key2: int
    key3: date


class MockModelList(BaseModelList[MockModel]):
    pass
