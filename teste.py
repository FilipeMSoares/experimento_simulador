import time
start_time = time.time()
f = open("i_got_it.txt","w+")
f.write("algum texto")
f.close()
elapsed_time = time.time()-start_time
print(elapsed_time)