import time
start_time = time.time()

l = [range(10000)]
s = {range(10000)}

#list_max = max(l)
set_max = max(s)

print("--- %s seconds ---" % (time.time() - start_time))

