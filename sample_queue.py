class NodeBitalino :
    time_slice_id = 0
    time_sampled = 0.0
    time_readed = 0.0
    next = None

head_bitalino = None
last_bitalino = None
sample_on_service = None
count = 0

def add (time):
    global head_bitalino, last_bitalino, count
    node = NodeBitalino()
    node.time_sampled = time
    if head_bitalino == None :
        head_bitalino = node
        last_bitalino = node
    else:
        last_bitalino.next = node
        last_bitalino = node
    count = count + 1

def pick_first ():
    global head_bitalino, last_bitalino, count
    if head_bitalino == None : raise Exception("Null Pointer head_bitalino")
    tmp = head_bitalino
    if head_bitalino.next == None :
        head_bitalino = None
        last_bitalino = None
    else:
        head_bitalino = head_bitalino.next
    count = count - 1
    return tmp

def can_first_be_serviced():
    global head_bitalino
    if not empty() : 
        return head_bitalino.time_slice_id > 0
    else:
        return False

def put_first_on_service():
    global sample_on_service
    sample_on_service = pick_first()

def end_service(time):
    global sample_on_service
    tmp = sample_on_service
    sample_on_service = None
    tmp.time_readed = time
    return tmp

def set_time_slice_id(time_slice_id):
    global head_bitalino
    tmp = head_bitalino
    while not tmp == None :
        if(tmp.time_slice_id == 0):
            tmp.time_slice_id = time_slice_id
        tmp = tmp.next
        
def empty():
    global head_bitalino
    return head_bitalino == None

def server_is_busy():
    global sample_on_service
    return not sample_on_service == None