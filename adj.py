from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from collections import defaultdict
from pox.openflow.discovery import Discovery
from pox.lib.util import dpid_to_str, str_to_bool
from pox.lib.util import dpidToStr
from pox.lib.recoco import Timer
import time
'''
This creates an adjacency matrix as follows:
the first index is for the first switch, the second index is for the adjacent switch,
the two ports that get appended each time are the ports on the first and second switches respectively that make up the link
e.g. 1{2:[3,1]} => switch1 has switch2 as an adjacent switch and they are connected via port3 (on switch1) and port1 (on switch2)

This component should be run alongside the openflow.discovery component
'''

#log = core.getLogger()

class adj(EventMixin):

    def __init__(self):
        self.adja = defaultdict(lambda: defaultdict(lambda: []))
        def startup():
            core.openflow.addListeners(self, priority=0)
            core.openflow_discovery.addListeners(self)
        core.call_when_ready(startup, ('openflow', 'openflow_discovery'))
        print "init over"

    def _handle_LinkEvent(self, event):
        #adj = defaultdict(lambda: defaultdict(lambda: []))
        li = event.link
        self.adja[li.dpid1][li.dpid2].append(li.port1)
        self.adja[li.dpid1][li.dpid2].append(li.port2)
        for i in self.adja:
          print i, dict(self.adja[i])


def launch():
  core.registerNew(adj)
