from typing import Iterator

from .base import BaseItem, BaseItemContainer, ItemParams, ItemParamsDict
from .items import HeaderItem, HeaderItemContainer, MenuItem


class Menu(BaseItemContainer[BaseItem]):
    def __init__(self, title: str | None = None, streamable: bool = False,
                 **params: ItemParams) -> None:
        super().__init__()
        self.streamable = streamable
        self._headers = HeaderItemContainer()

        if title:
            self.add_header(title, **params)

    def __iter__(self) -> Iterator[BaseItem]:
        yield from self._headers
        if self:
            yield MenuItem('---')
        yield from self._children

    def __str__(self) -> str:
        lines = []
        for item in self:
            lines.append(str(item))
        return '\n'.join(lines)

    def add_header(self, title: str, **params: ItemParams) -> BaseItem:
        return self._headers.add_item(title, **params)

    def add_item(self, title: str, **params: ItemParams) -> BaseItem:
        return self._item_factory(MenuItem, title, **params)

    def add_divider(self):
        return self._item_factory(MenuItem, '---')

    @property
    def header(self) -> HeaderItem | None:
        if self._headers:
            return self._headers[0]
        return None

    @property
    def params(self) -> ItemParamsDict | None:
        if self._headers:
            return self._headers[0].params
        return None

