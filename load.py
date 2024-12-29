from __future__ import annotations

from node import Node, GateNode, EventNode, Operator

def load_tree(tree: dict) -> Node:
    if tree['node_type'] == 'GateNode':
        ret = GateNode(
            name=tree['name'],
            description=tree['description'],
            op = Operator[tree['op']],
        )
        for child in tree['children']:
            ret.add_child(load_tree(child))
    elif tree['node_type'] == 'EventNode':
        ret = EventNode(
            name=tree['name'],
            description=tree['description'],
            q = tree['q'],
        )
    else:
        raise ValueError(f'Unknown node type: {tree["node_type"]}')

    return ret
