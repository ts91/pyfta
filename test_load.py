from __future__ import annotations

import json
import os

from load import load_tree

def test_load():
    tree1 = json.load(open('example.json'))
    root = load_tree(tree1)
    json.dump(root.dict(), open('test.json', 'w'), indent=4)
    tree2 = json.load(open('test.json'))
    os.remove('test.json')
    assert tree1 == tree2
