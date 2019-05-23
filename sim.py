print("Hello world!")

class bitalino_simulator:
    rates = [1,10,100,1000]
    rate_index = -1
    mac_adress = "FF:FF:FF:FF:FF:FF"
    volt = 0
    timeout = None
    is_open = False
    def __init__ (self,rate_index,mac_adress,timeout = None):
        self.rate_index = rate_index
        self.mac_adress = mac_adress
        self.timeout = timeout
        self.is_open = True
    
    def battery(self, value = 0):
        if value < 0 or value > 63 :
            raise Exception("value should be between 0 and 63")
        self.volt = 3.4+0.4*value/63.0
    
    def close(self):
        print(self.mac_adress+" closed")
        self.is_open = False
    
    def pwn(self,pwmOutput = 100):
        if(pwmOutput < 0 or 255 < pwmOutput):
            raise Exception("pwmOutput should be between 0 and 255")
        