class NodeGameState:
    time_slice_id = 0
    time_readed = 0.0
    time_recorded = 0.0
    next = None

head_gamestate = None
last_gamestate = None
gamestate_on_service = None

def add (time):
    global head_gamestate, last_gamestate
    node = NodeGameState()
    node.time_readed = time
    if head_gamestate == None :
        head_gamestate = node
        last_gamestate = node
    else:
        last_gamestate.next = node
        last_gamestate = node

def pick_first():
    global head_gamestate, last_gamestate
    if head_gamestate == None : raise Exception("Null Pointer head_gamestate")
    tmp = head_gamestate
    if head_gamestate.next == None :
        head_gamestate = None
        last_gamestate = None
    else:
        head_gamestate = head_gamestate.next
    return tmp

def put_first_on_service():
    global gamestate_on_service
    gamestate_on_service = pick_first()

def end_service(time):
    global gamestate_on_service
    tmp = gamestate_on_service
    gamestate_on_service = None
    tmp.time_recorded = time
    return tmp

def empty():
    global head_gamestate
    return head_gamestate == None

def server_is_busy():
    global gamestate_on_service
    return not gamestate_on_service == None