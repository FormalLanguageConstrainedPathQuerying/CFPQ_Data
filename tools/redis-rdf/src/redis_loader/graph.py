import redisgraph


class Graph(redisgraph.Graph):
    def __init__(self, name, redis_con):
        super().__init__(name, redis_con)

    def commit_edges(self):
        """
        Create edges with existing nodes.
        """
        if len(self.nodes) == 0 and len(self.edges) == 0:
            return None

        query = 'MATCH '
        for _, node in self.nodes.items():
            query += str(node) + ','

        # Discard leading comma.
        if query[-1] is ',':
            query = query[:-1]

        query += ' CREATE '

        query += ','.join([str(edge) for edge in self.edges])

        # Discard leading comma.
        if query[-1] is ',':
            query = query[:-1]

        return self.query(query)

    def flush_edges(self):
        """
        Commit the edges and reset the edges and nodes to zero length
        """
        self.commit_edges()
        self.nodes = {}
        self.edges = []
