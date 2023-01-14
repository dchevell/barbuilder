from collections.abc import MutableSequence


class BaseItem(MutableSequence):

    def __init__(self, title: str | None = None) -> None:
        self.title = title
        self.children: list[BaseItem] = []

    def __getitem__(self, index):
        return self.children[index]

    def __setitem__(self, index, value):
        self.children[index] = value

    def __delitem__(self, index):
        del self.children[index]

    def __len__(self):
        return len(self.children)

    def __iter__(self):
        return iter(self.children)

    def __bool__(self):
        return bool(self.children)

    def __repr__(self):
        name = self.__class__.__name__
        return f"{name}('{self.title}', children={self.children})"

    def append(self, item):
        self.children.append(item)

    def insert(self, i, item):
        self.children.insert(i, item)
