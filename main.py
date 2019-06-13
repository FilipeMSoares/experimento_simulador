import random
import contants as config
from event import Event
import sample_queue as sq
import gamestate_queue as gsq
import heapq
from collections import defaultdict

time_slice_id = 0
def gtime_slice_id():
    global time_slice_id
    time_slice_id = time_slice_id + 1
    return time_slice_id

eid = 0
def geid():
    global eid
    eid = eid + 1
    return eid

#mudei essa linha

times = [0.0]
count_samples_on_queue = 0
counts_samples_on_queue = [0]

timeslice_gamestate_dict = {}
timeslice_samples_dict = defaultdict(list)

event_queue = [Event(0.0,0,config.BEGIN)]
count = 0
count_thing = 0
last_event_type = -1
while count < config.number_of_events :
    event_inst = heapq.heappop(event_queue)
    time = event_inst.time
    event_type = event_inst.event_type
    count = count + 1
    #if(count < 20): print(str(event_type)+","+str(time))
    if event_type == config.BEGIN :
        #coloca primeira amostra do bitalino na fila
        time1 = time+config.sample_time()
        heapq.heappush(event_queue,Event(time1,geid(),config.SAMPLE_COLLECT))
        #coloca primeira escrita do gamestate na fila
        time2 = time+config.delta_gs_records
        gsq.add(time2)
        heapq.heappush(event_queue,Event(time2,geid(),config.GS_READ))
    elif event_type == config.GS_READ :
        #gera evento do proximo gamestate
        new_time = time+config.delta_gs_records
        heapq.heappush(event_queue,Event(new_time,geid(),config.GS_READ))
        #coloca gamestate na fila
        gsq.add(time)
        #se nenhum gamestate esta sendo servido
        if not gsq.server_is_busy() :
            #coloca o gamestate que acabou de chegar em servico
            gsq.put_first_on_service()
            #adiciona evento do fim de servico
            new_time = time + config.write_delay
            heapq.heappush(event_queue,Event(new_time,geid(),config.GS_WRITTEN))
        #senao coloca pacote na fila de espera
        #como o pacote já foi colocado na fila, não escrevemos o else no codigo
    elif event_type == config.GS_WRITTEN :
        #termina servico do gamestate atual
        gamestate = gsq.end_service(time)
        gamestate.time_slice_id = gtime_slice_id()
        sq.set_time_slice_id(gamestate.time_slice_id)

        timeslice_gamestate_dict[gamestate.time_slice_id] = gamestate        

        #se existem amostras na fila
        if not sq.empty() and not sq.server_is_busy() :
            #coloca o primeiro sample em servico
            sq.put_first_on_service()
            #coloca o evento de fim de servico
            new_time = time + config.download_time()
            heapq.heappush(event_queue, Event(new_time,geid(),config.SAMPLE_READ))
        #se existem gamestates na fila
        if not gsq.empty() :
            #coloca o gamestate do inicio da fila em servico
            gsq.put_first_on_service()
            #gera evento de fim de servico
            new_time = time + config.write_delay
            heapq.heappush(event_queue,Event(new_time,geid(),config.GS_WRITTEN))
    elif event_type == config.SAMPLE_COLLECT :
        times.append(time)
        count_samples_on_queue = count_samples_on_queue + 1
        counts_samples_on_queue.append(count_samples_on_queue)
        #gera evento da proxima amostra
        new_time = time+config.sample_time()
        heapq.heappush(event_queue,Event(new_time,geid(),config.SAMPLE_COLLECT))
        #coloca sample na fila
        sq.add(time)
    elif event_type == config.SAMPLE_READ :
        times.append(time)
        count_samples_on_queue = count_samples_on_queue - 1
        counts_samples_on_queue.append(count_samples_on_queue)
        #termina servico
        sample = sq.end_service(time)

        #if not sample.time_slice_id in timeslice_samples_dict :
            #timeslice_samples_dict[sample.time_slice_id] = []
        timeslice_samples_dict[sample.time_slice_id].append(sample)

        #se a proxima amostra pode ser servida
        if sq.can_first_be_serviced():
            #coloca a primeira sample enm servico
            sq.put_first_on_service()
            #coloca o evento de fim de servico
            new_time = time + config.download_time()
            heapq.heappush(event_queue, Event(new_time,geid(),config.SAMPLE_READ))

print("before")
print(time_slice_id)

import matplotlib.pyplot as plt

def get_value_if_exists_from(vet,on=0,otherwise = 0):
    if(len(vet) > 0): return vet[on].time_sampled
    return otherwise

x = [i for i in range(1,time_slice_id) ]
y = [len(timeslice_samples_dict[i]) for i in x]
y1 = [ get_value_if_exists_from(timeslice_samples_dict[i],on=0,otherwise=0) for i in x]
y2 = [ get_value_if_exists_from(timeslice_samples_dict[i],on=-1,otherwise=0) for i in x]

#print(y1)
#print(y2)

print("after")

plt.plot(x,y1)
plt.plot(x,y2)
plt.show()

plt.plot(x,y)
plt.show()

plt.plot(times,counts_samples_on_queue)
plt.show()