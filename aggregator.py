from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.recoco import Timer
from collections import defaultdict
from pox.openflow.discovery import Discovery
from pox.lib.util import dpid_to_str
import time
import sleep
'''
Pox Component to query OpenFlow-enabled switches every 10s for aggregated statistics.

'''


class aggregateStats(EventMixin):
    def __init__(self, interval=10):
        self.aggregateActiveCount = {}
        self.interval = interval
        self.previous = 0
        core.openflow.addListeners(self)

    def _handle_ConnectionUp(self, event):
        print "Switch %s has connected" % event.dpid
        sleep.switch_table.add_switch(sleep.switch(event.dpid))
        self.sendAggregateStatsRequest(event)

    def _handle_AggregateFlowStatsReceived(self, event):
        sw = 's%s' % event.dpid
        self.aggregateActiveCount[sw] = event.stats
        print "AggregateStatsReceived"
        
        self.bits = self.aggregateActiveCount[sw].byte_count

        self.since_last = self.bits - self.previous
        print sw, " Total Byte Count:", self.bits, 'and diff', self.since_last
        
        # add dpid, lid, linkbw to array
        sleep.print_to_file([self.since_last])
        
        #for each port arr += [lid,lbw] then print

        self.previous = self.bits

        Timer(self.interval, self.sendAggregateStatsRequest, args=[event])

    def sendAggregateStatsRequest(self, event):
        sr = of.ofp_stats_request()
        sr.type = of.OFPST_AGGREGATE
        sr.body = of.ofp_aggregate_stats_request()

        event.connection.send(sr)
        print "Sending aggregate stat request message to Switch %s " % event.dpid


def launch(interval='2'):
    interval = int(interval)
    core.registerNew(aggregateStats, interval)
