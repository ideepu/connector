from __future__ import annotations

import itertools
from collections import defaultdict
from typing import Any, Iterable, TypeVar

from pydantic import BaseModel as PydanticBaseModel, RootModel as PydanticRootModel

from src.exception import InvalidInputDataException

T = TypeVar('T', bound='BaseModel')


class BaseModel(PydanticBaseModel):
    pass


class BaseModelList(PydanticRootModel[list[T]]):
    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item: int) -> T:
        return self.root[item]

    def __len__(self) -> int:
        return len(self.root)

    def append(self, item: T):
        self.root.append(item)

    def first(self) -> T | None:
        for model in self:
            return model

    def group_by(self, keys: Iterable[Any]) -> Iterable[BaseModelList[T]]:
        sorted_data = sorted(self, key=lambda x: {getattr(x, key) for key in keys})
        grouped_data = itertools.groupby(sorted_data, key=lambda x: {getattr(x, key) for key in keys})
        for _, group in grouped_data:
            yield self.__class__(group)

    # TODO: Implement the aggregate method in generic way
    def aggregate(self, keys: Iterable[Any]) -> dict[Any, Any]:
        aggregate_dict = defaultdict(int)
        for obj in self:
            for key in keys:
                try:
                    aggregate_dict[key] += getattr(obj, key)
                except TypeError as e:
                    raise InvalidInputDataException(f'Key {key} is not a number') from e
        return aggregate_dict
