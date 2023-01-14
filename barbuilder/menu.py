import os
from pathlib import Path

from .base import BaseItem
from .utils import open_callback_url


class MenuItem(BaseItem):

    def __init__(self, title: str, **params: dict[str, int | str | bool ]) -> None:
        super().__init__()
        self.title = title
        self._alternate_item: MenuItem | None = None
        # params must be defined last
        self.params = params

    def __setattr__(self, name, value):
        excluded_names = ['params', *dir(self)]
        if 'params' in self.__dict__ and name not in excluded_names:
            self.params[name] = value
        else:
            self.__dict__[name] = value

    def __getattr__(self, name):
        obj_names = dir(self)
        if 'params' in self.__dict__ and name in self.params:
            return self.params[name]
        try:
            return self.__dict__[name]
        except KeyError as e:
            raise NameError(f'name {name} is not defined.')

    def append_item(self, item: str | MenuItem, **params: dict) -> None:
        if not isinstance(item, MenuItem):
            item = MenuItem(item, **params)
        self.append(item)

    def append_divider(self):
        super().append(MenuDivider())

    def set_alternate_item(self, item: MenuItem | str, **params: dict) -> None:
        if not isinstance(item, MenuItem):
            item = MenuItem(item, **params)
        item.alternate = True
        self._alternate_item = item


class MenuDivider(MenuItem):

    def __init__(self):
        super().__init__('---')


class Menu(MenuItem):

    def __init__(self, title: str | None = None, streamable: bool = False,
                 **params: dict) -> None:

        self.title_items: list[MenuItem] = []
        if title:
            self.append_title(title, **params)
        self.streamable = streamable
        self.plugin_path = Path(os.environ.get('SWIFTBAR_PLUGIN_PATH', '.'))
        super().__init__(title or '')

    @property
    def title(self) -> str | None:
        if self.title_items:
            return self.title_items[0].title
        return None

    @title.setter
    def title(self, title: str) -> None:
        if self.title_items:
            self.title_items[0].title = title
        else:
            self.append_title(title)

    @property
    def params(self) -> dict:
        if self.title_items:
            return self.title_items[0].params
        return dict()

    @params.setter
    def params(self, value) -> None:
        if self.title_items:
            self.title_items[0].params = value

    def append_title(self, item, **params: dict) -> None:
        if not isinstance(item, MenuItem):
            item = MenuItem(item, **params)
        self.title_items.append(item)
        return item

    def append_item(self, item: str | MenuItem, **params: dict) -> None:
        if not isinstance(item, MenuItem):
            item = MenuItem(item, **params)
        self.append(item)

    def render(self):
        lines = []
        if self.streamable:
            lines.append('~~~')
        for title in self.title_items:
            for line in render(title, children=False):
                lines.append(line)
        lines.append('---')
        for child in self.children:
            for line in render(child):
                lines.append(line)
        return '\n'.join(lines)

    def refresh(self):
        open_callback_url('refreshplugin', name=self.plugin_path.name)

    def refreshall(self):
        open_callback_url('refreshallplugins')

    def enable(self):
        open_callback_url('enableplugin', name=self.plugin_path.name)

    def disable(self):
        open_callback_url('disableplugin', name=self.plugin_path.name)

    def toggle(self):
        open_callback_url('toggleplugin', name=self.plugin_path.name)

    def notify(self, **params):
        open_callback_url('notify', name=self.plugin_path.name, **params)


def render(menu_item, children=True, indent=0):
    line = str(menu_item.title).replace('|', '│')
    line = ('--' * indent) + line
    if menu_item.params:
        params = ' '.join([f'{k}="{v}"' for k,v in menu_item.params.items()])
        line = f'{line} | {params}'
    yield line
    if children:
        for child in menu_item.children:
            yield from render(child, indent=indent+1)
    if menu_item._alternate_item:
        yield from render(menu_item._alternate_item)
