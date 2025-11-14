import dataclasses
import typing

T = typing.TypeVar('T')

@dataclasses.dataclass(eq=False)
class Node(typing.Generic[T]):
    id: str
    data: T
    parent: list[typing.Self] = dataclasses.field(default_factory=list[typing.Self])
    children: list[typing.Self] = dataclasses.field(default_factory=list[typing.Self])

    def __str__(self) -> str:
        return f"Node({self.id}): {self.data}\n"
