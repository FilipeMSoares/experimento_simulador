import random
import contants as config
from event import Event
import heapq

class NodeBitalino :
    time_sampled = 0.0
    time_readed = 0.0
    next = None

class NodeGameState:
    time_readed = 0.0
    time_recorded = 0.0
    next = None

head_bitalino = None
last_bitalino = None
head_gamestate = None
last_gamestate = None

def add_queue1 (time):
    global head_bitalino, last_bitalino
    node = NodeBitalino()
    node.time_sampled = time
    if head_bitalino == None :
        head_bitalino = node
        last_bitalino = node
    else:
        last_bitalino.next = node
        last_bitalino = node

def remove_queue1 (time):
    global head_bitalino, last_bitalino
    if head_bitalino == None : raise Exception("Null Pointer head_bitalino")
    head_bitalino.time_readed = head_bitalino.time_readed + time
    if head_bitalino.next == None :
        head_bitalino = None
        last_bitalino = None
    else:
        head_bitalino = head_bitalino.next

def add_queue2 (time):
    global head_gamestate, last_gamestate
    node = NodeGameState()
    node.time_readed = time
    if head_gamestate == None :
        head_gamestate = node
        last_gamestate = node
    else:
        last_gamestate.next = node
        last_gamestate = node

def remove_queue2 (time):
    global head_gamestate, last_gamestate
    if head_gamestate == None : raise Exception("Null Pointer head_gamestate")
    head_gamestate.time_recorded = head_gamestate.time_recorded + time
    if head_gamestate.next == None :
        head_gamestate = None
        last_gamestate = None
    else:
        head_gamestate = head_gamestate.next

def add_wait_time2(time):
    global head_gamestate
    node = head_gamestate
    while node != None :
        node.time_recorded = node.time_recorded + time

def add_wait_time1(time):
    global head_bitalino
    node = head_bitalino
    while node != None :
        node.time_readed = node.time_readed + time

eid = 0
def geid():
    global eid
    eid = eid + 1
    return eid

event_queue = [Event(0.0,geid(),config.BEGIN)]
count = 0
while count < 100 :
    event_inst = heapq.heappop(event_queue)
    time = event_inst.time
    event_type = event_inst.event_type
    if event_type == config.BEGIN :
        time1 = time+config.sample_time()
        add_queue1(time1)
        time2 = time+config.delta_gs_records
        add_queue2(time2)
        heapq.heappush(event_queue,Event(time1,geid(),config.BITALINO_SAMPLE_COLLECT))
        heapq.heappush(event_queue,Event(time2,geid(),config.GS_READ))
    elif event_type == config.GS_READ :
        time2 = time+config.write_delay
        #heapq.heappush(event)
    elif event_type == config.GS_WRITTEN:
        remove_queue2(time2)
        add_wait_time2(config.write_delay)

