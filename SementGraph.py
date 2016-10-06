from Graph import Graph
from Segment import Segment


class SegmentGraph(Graph):

    def __init__(self):
        super().__init__()

    def __str__(self):
        res = "vertices: "
        for k in self._graph_dict:
            res += "\n\t" + str(k) + ': ' + k.print_points()
        res += "\nedges: "
        for edge in self._Graph__generate_edges():
            res += "\n\t" + str(edge)
        return res

    def unite_vertices(self, first: Segment, second: Segment):
        """
        Uniting two vertices 'first' and 'second'
        and save result as 'first'
        'second' will be deleted
        :param first: this segment will contain result
        :param second: this segment will be deleted
        :return: None
        """

        # move all points from 'second' to 'first'
        first.points = first.points | second.points

        if first in self._graph_dict[second]:
            self._graph_dict[second].remove(first)
        if second in self._graph_dict[first]:
            self._graph_dict[first].remove(second)

        # replace all occurrences of 'second' by 'first'
        for vertex in self._graph_dict:
            if second in self._graph_dict[vertex]:
                self._graph_dict[vertex].remove(second)
                if vertex not in (first, second):
                    self._graph_dict[vertex].add(first)

        # merge all 'second' edges with 'first' edges
        self._graph_dict[first] = self._graph_dict[first] | self._graph_dict[second]

        # done! we don't need 'second' anymore
        self._graph_dict.pop(second)
        del second
