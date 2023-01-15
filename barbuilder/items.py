from __future__ import annotations

from textwrap import indent

from .base import BaseItem, BaseItemContainer, ItemParams


class HeaderItem(BaseItem):
    pass


class HeaderItemContainer(BaseItemContainer[HeaderItem]):

    def add_item(self, title: str, **params: ItemParams) -> HeaderItem:
        return self._item_factory(HeaderItem, title, **params)


class MenuItem(BaseItem, BaseItemContainer['MenuItem']):

    def __init__(self, title: str, **params: ItemParams) -> None:
        super().__init__(title, **params)

    def __str__(self) -> str:
        lines = [super().__str__()]
        for item in self:
            lines.append(indent(str(item), '--'))
        if self._alternate is not None:
            lines.append(str(self._alternate))
        return '\n'.join(lines)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{self.title}", [{", ".join(repr(i) for i in self)}])'

    def add_item(self, title: str, **params: ItemParams) -> MenuItem:
        return self._item_factory(MenuItem, title, **params)

    def add_divider(self) -> MenuItem:
        return self.add_item('---')

# class MenuItemContainer(BaseItemContainer[MenuItem]):