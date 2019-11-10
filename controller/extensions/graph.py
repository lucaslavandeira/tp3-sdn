

class Graph(object):

    def __init__(self):
        self.nodes = {}
        self.hosts = {}

    def add_link(self, node_src, src_port, node_dst, dst_port):
        self.nodes.setdefault(node_src, {})[node_dst] = src_port
        self.nodes.setdefault(node_dst, {})[node_src] = dst_port

    def add_host(self,host_src, host_port):
        self.hosts[host_src] = host_port

    def resolve_path(self, _from, packet):
        print(packet)
        return self.find_path(_from, packet.dst)

    def find_path(self, source, destination, visited=None):

        if source == destination:
            return [destination]

        if visited is None:
            visited = {source}


        #Evita errores paquetes iniciales
        if source in self.nodes.keys():
            for adj in self.nodes[source]:
                if adj in visited:
                    continue
                visited.add(adj)
                subpath = self.find_path(adj, destination, visited=visited)
                if subpath is not None:
                    return [source] + subpath

    def find_host(self,packet):
        if packet.dst in self.hosts.keys():
            return self.hosts[packet.dst]


    def find_switchs(self):
        print('hola')
        s = set(self.hosts.keys())
        switchs = [x for x in self.nodes.keys() if x not in s]
        print(switchs)
        return self.nodes[switchs[0]]

