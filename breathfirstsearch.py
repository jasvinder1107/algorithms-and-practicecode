#!/usr/bin/env python


def breathfirstsearch(g,firstelement):
    """
     This function implements breath first search given a graph g and source element as first element.

    """
    visited=[]
    queue=[firstelement]
    while queue:
        node=queue.pop(0)
        if node not in visited:
            visited.append(node)
            neighbours=g[node]
            for n in neighbours:
                queue.append(n)
    return visited


if __name__ == "__main__":

 graph = { 'A' : [ 'B', 'C','E'],
           'B' : [ 'A','D','E'],
           'C' : ['A','F','G'],
           'D' : ['B'],
           'E' : ['A','B','D'],
           'F' : ['C'],
           'G' : ['C'] }

 print("BFS sequence %s" % breathfirstsearch(graph,'A'))
