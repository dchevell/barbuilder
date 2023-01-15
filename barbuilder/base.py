from __future__ import annotations

import os
from collections.abc import MutableMapping, MutableSequence
from pathlib import Path
from typing import (Any, Iterable, Iterator, ParamSpec, SupportsIndex, TypeVar,
                    overload)

PLUGIN_PATH = Path(os.environ.get('SWIFTBAR_PLUGIN_PATH', '.'))

ItemParams = str | int | bool
ItemParamsDict = dict[str, ItemParams]


class Params:
    def __init__(self, **params: ItemParams) -> None:
        self.__dict__.update(params)

    def __getitem__(self, key: str) -> ItemParams:
        return self.__dict__[key]

    def __setitem__(self, key: str, value: ItemParams) -> None:
        self.__dict__[key] = value

    def __delitem__(self, key: str) -> None:
        del self.__dict__[key]

    def __contains__(self, key):
        return key in self.__dict__

    def __iter__(self) -> Iterator[(str, ItemParams)]:
        return iter(self.__dict__.items())

    def __len__(self) -> int:
        return len(self.__dict__)

    def __bool__(self):
        return bool(self.__dict__)

class BaseItem:

    def __init__(self, title: str, params: Params = None, **kwargs: ItemParams) -> None:
        super().__init__()
        self.title = title
        self._alternate: BaseItem | None = None
        if params:
            self.params = params
        else
            self.params = Params(**params)

    def __str__(self) -> str:
        if not self.params:
            return self.title
        title = self.title.replace(chr(124), chr(9474)) # melonamin is a smartass
        params_str = ' '.join([f'{k}="{v}"' for k,v in self.params])
        return f'{title} | {params_str}'

    def __repr__(self) -> str:
        return '{}("{}")'.format(self.__class__.__name__, self.title)

    @property
    def params(self) -> ItemParamsDict:
        return self._params

    def set_alternate(self, title: str, **params: ItemParams) -> BaseItem:
        cls = self.__class__
        params['alternate'] = True
        self._alternate = cls(title, **params)
        return self._alternate


T = TypeVar('T', bound=BaseItem)

class BaseItemContainer(MutableSequence[T]):

    def __init__(self) -> None:
        self._children: list[T] = []

    @overload
    def __getitem__(self, index: int) -> T:
        ...
    @overload
    def __getitem__(self, index: slice) -> list[T]:
        ...
    def __getitem__(self, index: SupportsIndex | slice) -> T | list[T]:
        return self._children[index]

    @overload
    def __setitem__(self, index: SupportsIndex, item: T) -> None:
        ...
    @overload
    def __setitem__(self, index: slice, item: Iterable[T]) -> None:
        ...
    def __setitem__(self, index: SupportsIndex | slice, item: T | Iterable[T]) -> None:
        if isinstance(index, SupportsIndex) and not isinstance(item, Iterable):
            self._children[index] = item
        elif isinstance(index, slice) and isinstance(item, Iterable):
            self._children[index] = item
        else:
            raise TypeError(f"{index}/{item} Invalid index/item type.")

    def __delitem__(self, index: int | slice) -> None:
        del self._children[index]

    def __len__(self) -> int:
        return len(self._children)

    def __iter__(self) -> Iterator[T]:
        return iter(self._children)

    def __bool__(self) -> bool:
        return bool(self._children)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({", ".join(repr(i) for i in self)})'

    def append(self, item: T) -> None:
        self._children.append(item)

    def insert(self, index: int, item: T) -> None:
        self._children.insert(index, item)

    def _item_factory(self, cls: type[T], title: str, **params: ItemParams) -> T:
        item = cls(title, **params)
        self.append(item)
        return item

