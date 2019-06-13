import time
start_time = time.time()
f = open("i_got_it.txt","w+")
f.write("algum texto")
f.close()
elapsed_time = time.time()-start_time
print(elapsed_time)

import random

class Node:
    next = None

    def __init__(self,next):
        self.value = random.random()*10
        self.next = next

a = Node(None)
b = Node(a)
c = Node(b)

tmp = c
while tmp != None :
    print(tmp.value)
    tmp = tmp.next