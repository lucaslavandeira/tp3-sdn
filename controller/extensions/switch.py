from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import IPAddr

log = core.getLogger()


class SwitchController:
    def __init__(self, dpid, connection, controller):
        self.dpid = dpid
        self.connection = connection
        # El SwitchController se agrega como handler de los eventos del switch
        self.connection.addListeners(self)
        self.controller = controller
        self.hosts = {}
        self.ports = {}

        self.cost = 0
        self.routes = []


    def add_link_port(self, switch_id, port):
        self.ports[port] = switch_id

    def remove_link_port(self,port):
        if port in self.ports.keys():
            self.ports.pop(port)

    def add_host(self, macaddr, port):
        self.host[port] = macaddr

    def clean_routes(self):
        self.routes = []

    def ports_adyascents(self):
        return self.ports.items()

    def hosts_adyascents(self):
        return self.hosts.items()

    def add_route(self, in_port, exit_port, eth_src, eth_dst, eth_type, ip_src, ip_dst, ip_type):
        self.routes.append([in_port, eth_src, eth_dst, eth_type, ip_src, ip_dst, ip_type, exit_port])
        # Aumentamos el costo de pasar por este switch en 1 para controlar
        # el trafico
        self.cost += 1

    def search_route(self,event,packet):

        for in_port, eth_src, eth_dst, eth_type, ip_src, ip_dst, ip_type, exit_port in self.routes:
            if (event.port == in_port and
                eth_src == packet.src and
                eth_dst == packet.dst and
                eth_type == packet.type and
                ip_src == packet.payload.srcip and
                ip_dst == packet.payload.dstip and
                ip_type == packet.payload.protocol):

                self.route_msg(in_port, exit_port, eth_src, eth_dst, eth_type, ip_src, ip_dst, ip_type, event.ofp)
                return True

        #No se encontro la ruta en las rutas existentes
        return False

    def route_msg(self, in_port, exit_port, eth_src, eth_dst, eth_type, ip_src, ip_dst, ip_type, data):
        msg = of.ofp_flow_mod()
        msg.data = data
        msg.command = of.OFPFC_ADD
        msg.match.dl_dst = eth_dst
        msg.match.dl_src = eth_src
        msg.match.in_port = in_port
        msg.match.dl_type = eth_type
        msg.match.nw_src = ip_src
        msg.match.nw_dst = ip_dst
        msg.match.nw_proto = ip_type

        msg.actions.append(of.ofp_action_output(port = exit_port))
        log.info("Sending to switch: %s from %s to %s port in: %s out: %s.", self.dpid, eth_src, eth_dst, in_port, exit_port)
        self.connection.send(msg)



    def _handle_PacketIn(self, event):
        """
        Esta funcion es llamada cada vez que el switch recibe un paquete
        y no encuentra en su tabla una regla para rutearlo
        """
        packet = event.parsed

        #Si un paquete arribo y no esta en la lista de puertos quiere decir
        #Que es un host perteneciente al switch
        if (event.port not in self.ports.keys()):
            self.hosts[event.port] = packet.src

        if packet.type != packet.IP_TYPE:  # Solo manejamos IPv4
            return

        ruteado = self.search_route(event, packet)
        if not ruteado:
            # Obtenemos y asignamos una ruta hacia el destino
            self.controller.assign_route(self.dpid, packet, event.port, event.ofp)
            self.search_route(event,packet)

