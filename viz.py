from __future__ import annotations
import json
import graphviz

from load import load_tree
from node import Node, GateNode, EventNode

def make_dot(n: Node) -> str:
    def make_dot_operator(n: Node) -> str:
        if not isinstance(n, GateNode):
            return ''
        return f'''<TR><TD PORT="here">{n.op}</TD></TR>'''

    return f'''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
                    <TR>
                        <TD PORT="there">{n.name}</TD>
                        <TD>{n.description}</TD>
                    </TR>
                    <TR>
                        <TD>Q</TD>
                        <TD>{n.value():.8f}</TD>
                    </TR>
                    {make_dot_operator(n)}
                </TABLE>>'''


def add_node(dot: graphviz.Digraph, n: Node):
    if isinstance(n, EventNode):
        dot.node(n.name, label=make_dot(n), shape='plaintext', color='black', fillcolor='lightyellow', style='filled')
    else:
        dot.node(n.name, label=make_dot(n), shape='plaintext', color='black')

    if not n.children:
        return
    for child in n.children:
        add_node(dot, child)
        dot.edge(f'{n.name}:here:s', f'{child.name}:there:n')

def generate_viz(filename: str, oformat: str = 'pdf', output: str = 'out'):
    dot = graphviz.Digraph(filename, format=oformat, engine='dot', graph_attr={'rankdir': 'HB'})
    with open(filename, 'r', encoding='utf-8') as f:
        root = load_tree(json.load(f))
        add_node(dot, root)
        dot.render(directory=output).replace('\\', '/')

if __name__ == '__main__':
    generate_viz('example.json')