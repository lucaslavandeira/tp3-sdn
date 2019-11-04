from mininet.topo import Topo


class FatTreeTopology(Topo):
    def __init__(self, size=2, **opts):
        Topo.__init__(self, **opts)
        print("Reading args! {}".format(size))

        self._init_root_node()

        if size < 2:
            return

        leaf_switches = self._init_tree_switches(size)

        self._init_leaf_nodes(leaf_switches)

    def _init_leaf_nodes(self, leaf_switches):
        host_count = 0
        for switch in leaf_switches:
            host_count += 1
            name = 'h{}'.format(host_count)
            self.addHost(name)
            self.addLink(switch, name)

    def _init_tree_switches(self, size):
        parent_switches = ['sw0']
        switch_count = 0
        for level in range(2, size + 1):
            nodes = 2 ** (level - 1)
            new_switches = []

            # Creamos los switch de este nivel y los linkeamos a los padres
            for _ in range(nodes):
                switch_count += 1
                new_switch_id = 'sw{}'.format(switch_count)
                self.addSwitch(new_switch_id)
                for switch in parent_switches:
                    self.addLink(switch, new_switch_id)
                new_switches.append(new_switch_id)

            parent_switches = new_switches
        return parent_switches

    def _init_root_node(self):
        self.addHost('cl1')
        self.addHost('cl2')
        self.addHost('cl3')
        self.addSwitch('sw0')
        self.addLink('cl1', 'sw0')
        self.addLink('cl2', 'sw0')
        self.addLink('cl3', 'sw0')


topos = {'fat_tree': FatTreeTopology}
