from typing import TypeVar

from pydantic import BaseModel as PydanticBaseModel, RootModel as PydanticRootModel

T = TypeVar('T', bound='BaseModel')


class BaseModel(PydanticBaseModel):
    pass


class BaseModelList(PydanticRootModel[list[T]]):
    def __iter__(self) -> T:
        return iter(self.root)
