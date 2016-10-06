""" A class representing non-oriented graph
based on implementation from here [ python-course.eu/graphs_python.php ]
"""


class Graph(object):

    def __init__(self):
        self._graph_dict = {}

    @property
    def vertices(self):
        """
        :return: the vertices of a graph
        """
        return list(self._graph_dict.keys())

    @property
    def edges(self):
        """
        :return: the edges of a graph
        """
        return self.__generate_edges()

    @property
    def size(self):
        """
        :return: number of vertices
        """
        return len(self._graph_dict)

    def add_vertex(self, vertex):
        """
        If the vertex "vertex" is not in
        self._graph_dict, a key "vertex" with an empty
        list as a value is added to the dictionary.
        Otherwise nothing has to be done.
        """
        if vertex not in self._graph_dict:
            self._graph_dict[vertex] = set()

    def add_edge(self, edge: tuple):
        """
        assumes that edge is of type set;
        between two vertices can be only one edge!
        """
        assert (len(edge) == 2)
        vertex1 = edge[0]
        vertex2 = edge[1]
        if vertex1 not in self._graph_dict:
            self._graph_dict[vertex1] = {vertex2}
        else:
            self._graph_dict[vertex1].add(vertex2)
        if vertex2 not in self._graph_dict:
            self._graph_dict[vertex2] = {vertex1}
        else:
            self._graph_dict[vertex2].add(vertex1)

    def __generate_edges(self):
        """
        :return: list of edges
        """
        edges = []
        for vertex in self._graph_dict:
            for neighbour in self._graph_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    def __str__(self):
        res = "vertices: "
        for k in self._graph_dict:
            res += "\n\t" + str(k)
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += "\n\t" + str(edge)
        return res
"""
    def find_isolated_vertices(self):
        graph = self._graph_dict
        isolated = []
        for vertex in graph:
            print(isolated, vertex)
            if not graph[vertex]:
                isolated += [vertex]
        return isolated

    def find_path(self, start_vertex, end_vertex, path=[]):
        graph = self._graph_dict
        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return path
        if start_vertex not in graph:
            return None
        for vertex in graph[start_vertex]:
            if vertex not in path:
                extended_path = self.find_path(vertex,
                                               end_vertex,
                                               path)
                if extended_path:
                    return extended_path
        return None

    def find_all_paths(self, start_vertex, end_vertex, path=[]):
        graph = self._graph_dict
        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return [path]
        if start_vertex not in graph:
            return []
        paths = []
        for vertex in graph[start_vertex]:
            if vertex not in path:
                extended_paths = self.find_all_paths(vertex,
                                                     end_vertex,
                                                     path)
                for p in extended_paths:
                    paths.append(p)
        return paths"""
