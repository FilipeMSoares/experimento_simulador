import random
sample_rate = 100.0
#number_of_samples = 1
delta_gs_records = 1.0
write_delay = 0.0001
number_of_events = 10000

BEGIN = 0
SAMPLE_COLLECT = 1
SAMPLE_READ = 2
GS_READ = 3
GS_WRITTEN = 4

def sample_time():
    return 1/sample_rate

def download_time():
    return random.random()*0.021+0.005