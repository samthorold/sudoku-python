from __future__ import annotations
from dataclasses import dataclass
from typing import Iterator


@dataclass
class Node:
    val: int
    left: Node | None = None
    right: Node | None = None


def insert_before(node: Node, new: Node) -> Node:
    if node.left:
        node.left.right = new
        new.left = node.left
    new.right = node
    node.left = new
    return new


def insert_after(node: Node, new: Node) -> Node:
    if node.right:
        new.right = node.right
        new.right.left = new
    new.left = node
    node.right = new
    return new


def pairs(nodes: Iterator[Node]) -> Iterator[tuple[Node, Node]]:
    pair = []
    for node in nodes:
        pair.append(node)
        if len(pair) > 1:
            yield tuple(pair)
        if len(pair) >= 2:
            pair = pair[-1:]


def create_list(nodes: Iterator[Node]):
    for l, r in pairs(nodes):
        yield insert_after(l, r)


def forwards(node: Node) -> Iterator[Node]:
    yield node
    while node := node.right:
        yield node
