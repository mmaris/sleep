import time
import threading
from pox.lib.recoco import Timer
from pox.core import core


log = core.getLogger()

# file names
datafile = "datafile.txt"
resultsfile = "resultsfile.txt"

# cycle and phase description
cycle_time = 50
phase_count = 5
phase_time = cycle_time/phase_count 
current_phase = 0
sleep_phase = 0

#network descriptors
link_bw = 100

# thresholds
sleep_th = 10


class data:
    def __init__(self, mean, mini, maxi, std):
        self.mean = mean
        self.mini = mini
        self.maxi = maxi
        self.std = std

#switch representation
#remembers data for each phase, switch-speciffic changes to be implemented, thresholds as well as switch changes depending on switch type
#table has the phase-wise data while switch_by_phase has switch information for each phase
#access phase-wise data with sw.table(phaseno) or sw.switch_by_phase(phaseno)
class switch:
    def __init__(self, dpid, th = [30,60]):
        #self.rate = rate
        #add a table of changes based on type.
        self.dpid = dpid
        self.table = []
        self.th = th
        self.switch_by_phase = {}
        #remove below
        self.switch_types = {30:1, 60:2, 100:3}
        #ports+adj

    def set_table(self,table):
        self.table = table

    def get_table(self,phaseno):
        return self.table[phaseno]

    def switch_by_phase(self,phaseno):
        return self_switch_by_phase[phaseno]

    def calculate_switch_by_phase(self):
        p = 0;
        for bw in self.table:
            for t in self.t:
                #use this if table contains data objects
                #if p.mean <= t:
                if bw <= t:
                    self.switch_by_phase[p]=self.switch_types[t]
                    break
                #check if last threshold and add default switch type
            p+=1

#link representation
#remembers data for each phase for a certain link
class link:
    def __init__(self, lid):
        #self.bandwidth = bandwidth
        # a better way to identify the link besides linkid should be made. Links are 2 way objects as well, so a link object could be used for the same physical link, which would cause a conflict in ID. Something like li-j could be used to identigy a link from si to sj.
        self.lid = lid
        self.table = [] # used to track means and other properties for each phase

    #maybe use inheritance to avoid extra code
    def set_table(self,table):
        self.table = table

    def get_table(self):
        return self.table



class table:
    def __init__(self):
        self.links = []
        self.switches = []

        # adj[i][j] will contain a link object with id lij - the link from si to sj
        # may be helpful
        #not implemented
        self.adj = []

    def add_link(self, link):
        #make a dictionary of {lid:linkobject}
        self.links.append(link)

    def add_switch(self, switch):
        #make it a dictionart of {dpid:switchobject}
        self.switches.append(switch)

    def calculate_means(self, arr):
        means = []
        start_index = 0
        end_time = arr[0][0] + phase_time

        for i in range(len(arr)):
            current_time = (arr[i][0])
            
            if end_time <= current_time or i == len(arr) - 1:
                means.append(self.get_means_for_phase(arr[start_index:i+1]))
                start_index = i
                end_time = arr[i][0] + phase_time + 1
            else:
                pass
                #remember data in array for each switch
        
        #problem here
        self.switches[0].set_table(means)
        

    def get_means_for_phase(self, phase):
        means = [0]*len[phase[0]]
        for i in range(len(phase)):
            for j in range(1,len(phase[0])):
                means[j] += phase[i][j]
                if i == len(phase)-1:
                    means[j]=means[j]/len(phase)
        return means

    

# prints array on a line, comma separated
# could print in separate files for each switch 
def print_to_file(arr):
    f = open(datafile,'a')
    arr.insert(0,time.time())

    joined = ','.join(map(str, arr))
    print('Printing ',joined)
    f.write(joined)
    f.close()

#works only for 1 switch
#returns an array of timestamp,bandwidth
#for multiple switches should return timestamp,dpid,bandwidth,lid,bandwidth,lid,bandwidth,... for each link going out from the switch
def read_from_file():
    """first element of returned array is a timestamp in some format
    """
    f = open(datafile, 'r+')
    content = f.readlines()
    f.truncate(0)
    f.close()

    return [float(x.strip().split(',')) for x in content]


#checks if the traffic is low enough during this phase
def available():
    #oprn file
    f = open(datafile,'rb')
    
    #read last line
    lines = f.realines()
    last = f[-1].decode()

    #check traffic against congestion threshold
    if last.split[1] > th: 
        return false
    else:
        return true


#schedule sleep after n seconds
def schedule_sleep(n):
    Timer(n, threading.Thread(target = _handle_sleep).start)

def get_switch(dpid):
    return switch_table.switches[dpid].switch_by_phase(current_phase)

#main sleeping function
def _handle_sleep():
    #get current time
    start_time = time.time()
    
    global current_phase
    log.info("Checking if sleep time")
    current_phase = (current_phase+1)%phase_count

    if current_phase != sleep_phase:
        log.info('Not the right phase')
        
    else:
        #not worried by this for now
        #if !available(): schedule_sleep(phase_time/10)

        #now = time.time()
        #while(time.time()<now+5):
        #    pass

        log.info("Starting sleeping sequence")
        #process
        switch_table.calculate_means(read_from_file())

        for sw in switch_table.switches:
            sw.calculate_switch_by_phase()
        
        log.info('Done Sleeping')

    log.info("Schedule next Sleep check in %i seconds"%phase_time)
    
    #get time and calculate time used processing. subtract from time to next sleep check
    end_time = time.time()
    schedule_sleep(phase_time-(end_time-start_time))

global switch_table
switch_table = table()
