# Copyright 2012 James McCauley
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Turns your complex OpenFlow switches into stupid hubs.
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpidToStr
from pox.lib.recoco import Timer
import time
import threading

log = core.getLogger()

def _handle_sleep():
  log.info("Checking if sleep time")
  #Always sleep time in this implementation
  #read file and process work. Add wakeup check at 1 minute
  time.sleep(5)
  log.info("Done Sleeping. Schedule next Sleep check in 30 seconds")

  Timer(10, threading.Thread(target = _handle_sleep).start)

def _handle_ConnectionUp (event):
  msg = of.ofp_flow_mod()
  msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
  msg.actions.append(of.ofp_action_output(port = of.OFPP_CONTROLLER))

  event.connection.send(msg)
  Timer(10, threading.Thread(target = _handle_sleep).start)
  log.info("Hubifying %s", dpidToStr(event.dpid))

def launch ():
  core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)

  log.info("Hub running.")
