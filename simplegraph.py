__author__ = 'flyee'

""" A Python Class
A simple Python graph class, demonstrating the essential
facts and functionality of graphs.
"""


class SimpleGraph(object):

    """ Simple graph: undirected, loop-less graph.
    dict of sets:
    {1 : {2, 3}, 2 : {1}, 3 : {1}}
    """

    def __init__(self, graph_dict={}):
        """ initializes a graph object
        """
        self.__graph_dict = {}
        for vertex in graph_dict:
            self.add_vertex(vertex)
            for neighbor in graph_dict[vertex]:
                self.add_vertex(neighbor)
                if vertex != neighbor:
                    self.add_edge({vertex, neighbor})

    def vertices(self):
        return list(self.__graph_dict.keys())

    def edges(self):
        edges = []
        for vertex in self.__graph_dict:
            for neighbor in self.__graph_dict[vertex]:
                if {vertex, neighbor} not in edges:
                    edges.append({vertex, neighbor})
        return edges

    def add_vertex(self, vertex):
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = set()

    def add_edge(self, edge):
        """
        Assume edge is of type set, tuple or list;
        between two vertices can be multiple edges!
        """
        import pdb; pdb.set_trace()  # XXX BREAKPOINT
        v1, v2 = tuple(edge)
        if v1 in self.__graph_dict:
            self.__graph_dict[v1].add(v2)
        import pdb; pdb.set_trace()  # XXX BREAKPOINT
        else:
            self.__graph_dict[v1] = {v2}
        if v2 in self.__graph_dict:
            self.__graph_dict[v2].add(v1)
        else:
            self.__graph_dict[v2] = {v1}

    def __str__(self):
        res = "vertices: "
        for k in self.__graph_dict:
            res += str(k) + " "
        res += '\nedges: '
        for edge in self.edges():
            res += str(edge) + ' '
        return res

    def find_path(self, start_vertex, end_vertex, path=[]):
        """Find a path from start_vertex to end_vertex in graph"""
        graph = self.__graph_dict
        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return path
        if start_vertex not in graph:
            return None
        for vertex in graph[start_vertex]:
            if vertex not in path:
                extended_path = self.find_path(vertex, end_vertex, path)
                if extended_path:
                    return extended_path
        return None

    def find_all_paths(self, start_vertex, end_vertex, path=[]):
        """ find all paths from start_vertex to end_vertex in graph
        """
        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return [path]
        if start_vertex not in self.__graph_dict:
            return []
        paths = []
        for vertex in self.__graph_dict[start_vertex]:
            if vertex not in path:
                extended_paths = self.find_all_paths(vertex, end_vertex, path)
                for p in extended_paths:
                    paths.append(p)
        return paths

    def vertex_degree(self, vertex):
        return len(self.__graph_dict[vertex])

    def find_isolated_vertices(self):
        isolated = []
        for vertex in self.__graph_dict:
            if len(self.__graph_dict[vertex]) == 0:
                isolated.append(vertex)
        return isolated

    def min_degree(self):
        return self.degree_sequence()[-1]

    def max_degree(self):
        return self.degree_sequence()[0]

    def degree_sequence(self):
        """ calculate degree sequence
        """
        seq = [len(self.__graph_dict[vertex]) for vertex in self.__graph_dict]
        seq.sort(reverse=True)
        return seq

    def erdoes_gallai(self, dseq):
        """ checks if the condition of the Erdoes-Gallai inequality is fullfilled.
        A non-increasing sequence [d_1, ..., d_n] is the degree sequence of a simple graph if and only if the sum is even and for any $k \in \{1, ..., n\}$
        \[
        \sum_{i=1}^{k} d_i \le k(k-1) + \sum_{i=k+1}^{n} \min(d_i, k)
        \]
        """
        fullfilled = True
        dseq.sort(reverse=True)
        if sum(dseq) % 2 == 1:
            fullfilled = False
            return fullfilled
        n = len(dseq)
        for k in range(1, n + 1):
            if sum(dseq[:k]) > k * (k - 1) + sum(map(min, zip(dseq[k:], [k] * (n - k)))):
                fullfilled = False
                return fullfilled
        return fullfilled

    def density(self):
        V = len(self.__graph_dict.keys())
        E = len(self.edges())
        return 2.0 * E / (V * (V - 1))

    def is_connected(self):
        """ not concern efficiency
        """
        vertices = self.__graph_dict.keys()
        if len(vertices) < 2:
            return True
        met1 = {list(vertices)[0]}
        while True:
            met2 = met1
            for v in met1:
                met2 = met2.union(self.__graph_dict[v])
            if met1 == met2:
                break
            else:
                met1 = met2
                met2 = set({})
        return True if len(met1) == len(vertices) else False

    def diameter(self):
        v = self.__graph_dict.keys()
        pairs = [(v1, v2) for v1 in v for v2 in v if v1 < v2]
        return len(max([min(self.find_all_paths(s, e), key=len)
                   for (s, e) in pairs], key=len)) - 1


if __name__ == '__main__':
    g = {"a": ["c"],
         "b": ["c", "e"],
         "c": ["a", "b", "d", "e"],
         "d": ["c"],
         "e": ["c", "b"],
         "f": []
         }

    graph = SimpleGraph(g)

    print("Vertices of graph:")
    print(graph.vertices())
    import pdb
    pdb.set_trace()  # XXX BREAKPOINT

    print("Edges of graph:")
    print(graph.edges())

    print("Add vertex: 'z'")
    graph.add_vertex("z")
    print("Vertices of graph:")
    print(graph.vertices())

    print("Add an edge:")
    graph.add_edge({"a", "z"})

    print("Vertices of graph:")
    print(graph.vertices())

    print("Edges of graph:")
    print(graph.edges())

    print('Adding an edge {"x","y"} with new vertices:')
    graph.add_edge({"x", "y"})
    print("Vertices of graph:")
    print(graph.vertices())
    print("Edges of graph:")
    print(graph.edges())

    print("Path from 'a' to 'e':")
    print(graph.find_path('a', 'e'))

    print("All paths from 'a' to 'e':")
    print(graph.find_all_paths('a', 'e'))

    print("Degree of 'c':")
    print(graph.vertex_degree('c'))

    print("Isolated:")
    print(graph.vertices())
    print(graph.edges())
    print(graph.find_isolated_vertices())

    print("Min degree: ", graph.min_degree())
    print("Max degree: ", graph.max_degree())
    print("Degree sequence: ", graph.degree_sequence())

    print("Is d-seq: ", graph.erdoes_gallai(graph.degree_sequence()))

    complete_graph = {
        "a": ["b", "c"],
        "b": ["a", "c"],
        "c": ["a", "b"]
    }

    isolated_graph = {
        "a": [],
        "b": [],
        "c": []
    }

    gc = SimpleGraph(complete_graph)
    print("Density, complete graph: ", gc.density())

    gi = SimpleGraph(isolated_graph)
    print("Density, isolated graph: ", gi.density())

    print("Density: ", graph.density())

    print("Is connect? complete: ", gc.is_connected())
    print("Is connect? : ", graph.is_connected())
    print("Is connect? isolated: ", gi.is_connected())

    g = {"a": ["d"],
         "b": ["c"],
         "c": ["b", "c", "d", "e"],
         "d": ["a", "c"],
         "e": ["c"],
         "f": []
         }

    g2 = {"a": ["d", "f"],
          "b": ["c"],
          "c": ["b", "c", "d", "e"],
          "d": ["a", "c"],
          "e": ["c"],
          "f": ["a"]
          }

    g3 = {"a": ["d", "f"],
          "b": ["c", "b"],
          "c": ["b", "c", "d", "e"],
          "d": ["a", "c"],
          "e": ["c"],
          "f": ["a"]
          }

    graph = SimpleGraph(g)
    print(graph)
    print(graph.is_connected())

    graph = SimpleGraph(g2)
    print(graph)
    print(graph.is_connected())

    graph = SimpleGraph(g3)
    print(graph)
    print(graph.is_connected())

    g = {"a": ["c"],
         "b": ["c", "e", "f"],
         "c": ["a", "b", "d", "e"],
         "d": ["c"],
         "e": ["b", "c", "f"],
         "f": ["b", "e"]
         }

    graph = SimpleGraph(g)
    print(graph.diameter())
