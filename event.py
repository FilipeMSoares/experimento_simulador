class Event:
    time = 0.0
    eid = 0
    event_type = 0
    
    def __init__(self,time,eid,event_type):
        self.time = time
        self.eid = eid
        self.event_type = event_type