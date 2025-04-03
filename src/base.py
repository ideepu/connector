from __future__ import annotations

from collections import defaultdict
from typing import Any, Callable, ClassVar, Generic, Iterable, TypeVar

from pydantic import BaseModel as PydanticBaseModel, RootModel as PydanticRootModel

from src.config import config
from src.libs.request import BaseRequest

T = TypeVar('T', bound=PydanticBaseModel)


class BaseModel(PydanticBaseModel):
    pass


class BaseModelList(PydanticRootModel[list[T]], Generic[T]):
    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item: int) -> T:
        return self.root[item]

    def __len__(self) -> int:
        return len(self.root)

    def append(self, item: T):
        self.root.append(item)

    def get_by_key_value(self, key: Any, value: Any) -> T | None:
        for model in self:
            if getattr(model, key) == value:
                return model
        return None

    def groupby_aggregate(
        self,
        group_by: Iterable[Any],
        aggregate_by: Iterable[Any],
        agg_func: Callable = sum,
    ) -> BaseModelList[T]:
        grouped_data: dict[Any, dict[Any, list]] = defaultdict(lambda: {field: [] for field in aggregate_by})
        for entry in self:
            key = tuple(getattr(entry, field) for field in group_by)
            for field in aggregate_by:
                grouped_data[key][field].append(getattr(entry, field))

        aggregated_result: list[Any] = []
        for key, fields in grouped_data.items():
            aggregated_result.append(
                {**dict(zip(group_by, key)), **{field: agg_func(values) for field, values in fields.items()}}
            )

        return self.__class__(aggregated_result)


class BaseManager(BaseModel):
    request: ClassVar = BaseRequest(
        base_url=f'{config.BASE_URL}/{config.BASE_URL_PREFIX}',
        supported_methods=['GET'],
    )
