from __future__ import annotations

import random
import typing

from .node import Node

T = typing.TypeVar("T")


class Tree(typing.Generic[T]):
    def __init__(self) -> None:
        self.root: Node[T] | None = None
        self.__nodes: dict[str, Node[T]] = {}
        self.__node_counter: int = -1

    # region PRIVATE
    def __append_root_data(self, node_data: T) -> Node[T]:
        if self.root is not None:
            raise ValueError("Root node already exists!")

        new_node: Node[T] = Node(id="root", data=node_data)

        self.root = new_node
        self.__nodes[new_node.id] = new_node
        return new_node

    def __append_child_data(self, node_data: T, node_id: str, parent: str) -> Node[T]:
        parent_node: Node[T] = self.__nodes[parent]
        new_node: Node[T] = Node(id=node_id, data=node_data)

        new_node.parent.append(parent_node)
        parent_node.children.append(new_node)

        self.__nodes[new_node.id] = new_node
        return new_node

    # endregion

    # region PUBLIC CREATE
    def append_data(self, node_data: T, node_id: str | None = None, parent: str | None = None) -> Node[T]:
        self.__node_counter += 1

        if node_id is None:
            node_id = str(self.__node_counter)

        if parent is None:
            return self.__append_root_data(node_data)
        else:
            return self.__append_child_data(node_data, node_id, parent)

    def append_subtree(self, subtree: Tree[T], parent: str) -> Tree[T]:
        if not parent in self.get_all_ids():
            raise ValueError("Parent node does not exist.")

        if subtree.root is None:
            raise ValueError("Subtree must have a root node!")

        subtree_root_node: Node[T] = self.append_data(node_data=subtree.root.data,
                                             parent=parent)

        stack: list[tuple[Node[T], str]] = []
        for child in subtree.root.children:
            stack.append((child, subtree_root_node.id))

        while stack:
            original_child, new_parent_id = stack.pop()

            new_child: Node[T] = self.append_data(node_data=original_child.data,
                                         parent=new_parent_id)

            for grandchild in original_child.children:
                stack.append((grandchild, new_child.id))

        return subtree

    # endregion

    # region PUBLIC READ
    def get_all_ids(self) -> list[str]:
        return list(self.__nodes.keys())

    def get_random_node(self) -> Node[T]:
        return random.choice(list(self.__nodes.values()))

    def get_random_non_root_node(self) -> Node[T]:
        non_root_nodes = [v for k, v in self.__nodes.items() if k != "root"]
        if not non_root_nodes:
            raise ValueError("No non-root nodes available.")
        return random.choice(non_root_nodes)

    def get_all_nodes(self) -> list[Node[T]]:
        return list(self.__nodes.values())

    def get_all_non_root_nodes(self) -> list[Node[T]]:
        return [v for k, v in self.__nodes.items() if k != "root"]

    # endregion

    # region PUBLIC UPDATE
    # endregion

    # region PUBLIC DELETE
    def delete_node(self, node_id: str, delete_children: bool = False) -> None:
        if node_id not in self.__nodes:
            raise KeyError(f"Node with id {node_id} not found in tree.")

        node: Node[T] = self.__nodes[node_id]

        if delete_children:
            stack: list[Node[T]] = list(node.children)
            while stack:
                child = stack.pop()
                stack.extend(child.children)
                del self.__nodes[child.id]

        if node.parent:
            parent = node.parent[0]
            parent.children.remove(node)

        del self.__nodes[node.id]
        if self.root == node:
            self.root = None

    # endregion

    # region PUBLIC DUNDER
    def __str__(self) -> str:
        if self.root is None:
            return "Tree is empty."

        result: list[str] = []
        stack: list[tuple["Node[T]", int]] = [(self.root, 0)]

        while stack:
            node, depth = stack.pop()
            result.append(f"{'  ' * depth}-> {node}")
            for child in reversed(node.children):
                stack.append((child, depth + 1))

        return "".join(result)
        # endregion
