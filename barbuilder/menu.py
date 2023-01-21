from argparse import ArgumentParser
from collections.abc import Callable
from time import sleep
from typing import Iterator

from .base import Item, ItemContainer, ItemParams, ItemParamsDict
from .items import HeaderItem, HeaderItemContainer, MenuItem, Reset
from .utils import deserialize_callback, P


class Menu(ItemContainer):
    def __init__(self, title: str | None = None, **params: ItemParams) -> None:
        super().__init__()
        self._headers = HeaderItemContainer()
        self._main: Callable[..., None] | None = None
        self._parser = ArgumentParser(add_help=False)
        self._parser.add_argument('--script-callbacks', nargs='+')

        if title:
            self.add_header(title, **params)

    def __iter__(self) -> Iterator[Item]:
        yield from self._headers
        if self:
            yield MenuItem('---')
        yield from self._children

    def __str__(self) -> str:
        lines = []
        for item in self:
            lines.append(str(item))
        return '\n'.join(lines) + '\n'

    @property
    def header(self) -> Item | None:
        if not self._headers:
            return None
        return self._headers[0]

    @property
    def title(self) -> str | None:
        if self.header is None:
            return None
        return self.header.title

    @title.setter
    def title(self, value: str) -> None:
        if self.header is None:
            self.add_header(value)
        else:
            self.header.title = value

    @property
    def params(self) -> ItemParamsDict | None:
        if not isinstance(self.header, HeaderItem):
            return None
        return self.header.params

    def add_header(self, title: str, **params: ItemParams) -> Item:
        return self._headers.add_item(title, **params)

    def add_item(self, title: str, **params: ItemParams) -> Item:
        return self._item_factory(MenuItem, title, **params)

    def add_divider(self) -> Item:
        return self.add_item('---')

    def runner(self, func: Callable[..., None]) -> Callable[..., None]:
        self._main = func
        return func

    def _run_callbacks(self, callbacks: list[str]) -> None:
        for callback in callbacks:
            func: Callable[..., object]
            args: P.args
            kwargs: P.kwargs
            func, args, kwargs = deserialize_callback(callback)
            func(*args, **kwargs)

    def run(self, repeat_interval: int | None = None) -> None:
        args = self._parser.parse_args()
        if args.script_callbacks is not None:
            self._run_callbacks(args.script_callbacks)
            return
        if self._main is None:
            raise RuntimeError('no main function specified')
        if not repeat_interval:
            self._main()
            print(self)
        else:
            while True:
                self._main()
                print(Reset())
                print(self, flush=True)
                sleep(repeat_interval)
