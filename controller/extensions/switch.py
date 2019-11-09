from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import IPAddr

log = core.getLogger()


class SwitchController:
    def __init__(self, dpid, connection, switches):
        self.dpid = dpid
        self.connection = connection
        # El SwitchController se agrega como handler de los eventos del switch
        self.connection.addListeners(self)
        self.switches = switches

    def _handle_PacketIn(self, event):
        """
        Esta funcion es llamada cada vez que el switch recibe un paquete
        y no encuentra en su tabla una regla para rutearlo
        """

        packet = event.parsed
        path = self.switches.resolve_path(self.connection.eth_addr, packet)
        log.info("Path encontrado {}".format(path))
        if not path:
            return
        # SRC IP = packet.payload.srcip
        # DST IP = packet.payload.dstip
        # SRC PORT = packet.payload.payload.srcport
        # DST PORT = packet.payload.payload.dstport

        import pdb; pdb.set_trace()
        if packet.type != packet.IP_TYPE:  # Solo manejamos IPv4
            return

        if event.port == 1:
            out_port = 2
        else:
            out_port = 1

        msg = of.ofp_flow_mod()
        msg.data = event.ofp
        msg.priority = of.OFP_DEFAULT_PRIORITY
        msg.match.dl_type = 0x800
        msg.match.nw_dst = packet.payload.dstip
        msg.actions.append(of.ofp_action_output(port=out_port))
        self.connection.send(msg)
