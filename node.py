from __future__ import annotations

from enum import Enum
from typing import Any, Callable
from dataclasses import dataclass

class Operator(Enum):
    NULL = 0
    AND = 1
    OR = 2
    NOT = 3

def operator_null(_: list[Node]) -> float:
    return 0

def operator_and(a: list[Node]) -> float:
    ret = 0
    for i, node in enumerate(a):
        if i == 0:
            ret = node.value()
            continue
        ret = ret * node.value()

    return ret

def operator_or(a: list[Node]) -> float:
    ret = 0
    for i, node in enumerate(a):
        if i == 0:
            ret = node.value()
            continue
        ret = ret + node.value()

    if ret > 1:
        return 1

    return ret

def operator_not(a: list[Node]) -> float:
    if len(a) != 1:
        raise ValueError('Not operator must have exactly one child')
    return 1 - a[0].value()

@dataclass
class Node:
    name: str
    description: str
    parent: Node = None
    children: list[Node] = None

    def value(self) -> float:
        if not self.children:
            return 0
        return sum([child.value() for child in self.children])

    def add_child(self, child: Node):
        child.parent = self

        if not self.children:
            self.children = []
        self.children.append(child)

    def __str__(self):
        return f'{self.name} : {[child.__str__() for child in self.children]}'

    def dict(self) -> dict[str, Any]:
        return {
            'name': self.name,
            'node_type': self.__class__.__name__,
            'description': self.description,
            'children': [child.dict() for child in self.children]
        }

@dataclass
class GateNode(Node):
    op: Operator = Operator.NULL

    def value(self) -> float:
        if not self.children:
            return 0
        return operators[self.op](self.children)

    def dict(self):
        return {
            'name': self.name,
            'node_type': self.__class__.__name__,
            'description': self.description,
            'children': [child.dict() for child in self.children],
            'op': operators_to_str[self.op]
        }

@dataclass
class EventNode(Node):
    q: float = 0

    def value(self) -> float:
        return self.q

    def __str__(self):
        return f'{self.name}: {self.value()}'

    def dict(self):
        return {
            'name': self.name,
            'node_type': self.__class__.__name__,
            'description': self.description,
            'q': self.q
        }

operators: dict[Operator, Callable[list[Node], float]] = {
    Operator.NULL: operator_null,
    Operator.AND: operator_and,
    Operator.OR: operator_or,
    Operator.NOT: operator_not,
}

operators_to_str = {
    Operator.NOT: 'NOT',
    Operator.AND: 'AND',
    Operator.OR: 'OR',
}
