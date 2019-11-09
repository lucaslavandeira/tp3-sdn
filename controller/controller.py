from pox.core import core
import pox.openflow.discovery
import pox.openflow.spanning_tree
import pox.forwarding.l2_learning
from pox.lib.util import dpid_to_str

from extensions.graph import Graph
from extensions.switch import SwitchController

log = core.getLogger()


class Controller:
    def __init__(self):
        self.connections = set()
        self.switches = Graph()  # "Grafo" de adyacencias
        self.links = {}  # Mapeo de dpids a direcciones ethernet
        # Esperando que los modulos openflow y openflow_discovery esten listos
        core.call_when_ready(self.startup, ('openflow', 'openflow_discovery'))

    def startup(self):
        """
        Esta funcion se encarga de inicializar el controller
        Agrega el controller como event handler para los eventos de
        openflow y openflow_discovery
        """
        core.openflow.addListeners(self)
        core.openflow_discovery.addListeners(self)
        log.info('Controller initialized')

    def _handle_ConnectionUp(self, event):
        """
        Esta funcion es llamada cada vez que un nuevo switch establece conexion
        Se encarga de crear un nuevo switch controller para manejar los eventos de cada switch
        """
        log.info("Switch %s has come up.", dpid_to_str(event.dpid))
        self.links[event.dpid] = event.connection.eth_addr
        if (event.connection not in self.connections):
            self.connections.add(event.connection)
            SwitchController(event.dpid, event.connection, self.switches)

    def _handle_LinkEvent(self, event):
        """
        Esta funcion es llamada cada vez que openflow_discovery descubre un nuevo enlace
        """
        link = event.link
        ### posiblemente haya que mapear los ethernet internos del switch, todas los puertos tienen un eth tambien
        log.info("Link has been discovered from %s,%s to %s,%s", dpid_to_str(link.dpid1), link.port1,
                 dpid_to_str(link.dpid2), link.port2)
        self.switches.add_link(self.links[link.dpid1], link.port1, self.links[link.dpid2], link.port2)

def launch():
    # Inicializando el modulo openflow_discovery
    pox.openflow.discovery.launch()

    # Registrando el Controller en pox.core para que sea ejecutado
    core.registerNew(Controller)
