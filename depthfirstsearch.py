#!/usr/bin/env python3


def depthfirstsearch(g,firstelement):
    """
     This function implements depth first search given a graph g and source element as firstelement.

    """
    visited=[]
    stack=[firstelement]
    while stack:
        node=stack[-1]
        if node not in visited:
            visited.append(node)
        delete_from_stack=True
        neighbours=g[node]
        for n in neighbours:
            if n not in visited:
                stack.extend(n)
                delete_from_stack=False
                break
        if delete_from_stack:
            stack.pop()
    return visited


if __name__ == "__main__":

 graph2= {'A': ['B','C','E'],
          'B': [ 'D','F'],
          'C': ['G'],
          'D': ['B'],
          'E': ['F'],
          'F': ['E'],
          'G': ['C']}

 print("DFS sequence %s" % depthfirstsearch(graph2,'A'))
