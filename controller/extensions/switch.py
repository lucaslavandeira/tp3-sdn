from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import IPAddr

log = core.getLogger()


class SwitchController:
    def __init__(self, dpid, connection):
        self.dpid = dpid
        self.connection = connection
        # El SwitchController se agrega como handler de los eventos del switch
        self.connection.addListeners(self)

    def _handle_PacketIn(self, event):
        """
        Esta funcion es llamada cada vez que el switch recibe un paquete
        y no encuentra en su tabla una regla para rutearlo
        """

        packet = event.parsed

        # SRC IP = packet.payload.srcip
        # DST IP = packet.payload.dstip
        # SRC PORT = packet.payload.payload.srcport
        # DST PORT = packet.payload.payload.dstport
        log.info("Packet arrived to switch %s from %s to %s",
                 self.dpid, packet.payload.srcip, packet.payload.dstip)

        if packet.payload.v != 4:
            return
        if packet.payload.dstip.toStr() == of.IPAddr('10.0.0.1').toStr():
            out_port = 1
        else:
            out_port = 2

        msg = of.ofp_flow_mod()
        msg.priority = 42
        msg.match.dl_type = 0x800
        msg.match.nw_dst = packet.payload.dstip
        msg.actions.append(of.ofp_action_output(port=out_port))
        self.connection.send(msg)

