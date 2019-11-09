

class Graph(object):

    def __init__(self):
        self.nodes = {}

    def add_link(self, node_src, src_port, node_dst, dst_port):
        self.nodes.setdefault(node_src, {})[node_dst] = src_port
        self.nodes.setdefault(node_dst, {})[node_src] = dst_port

    def resolve_path(self, _from, packet):
        import pdb; pdb.set_trace()
        return self.find_path(_from, packet.dst)

    def find_path(self, source, destination, visited=None):
        if source == destination:
            return [destination]

        if visited is None:
            visited = {source}

        for adj in self.nodes[source]:
            if adj in visited:
                continue
            visited.add(adj)
            subpath = self.find_path(adj, destination, visited=visited)
            if subpath is not None:
                return [source] + subpath
