from SEA import *
import time
scale=1
stastic=[]
for i in range(7):
    l = [1,10,33,100,319,1000,3190]
    scale= l[i]
    s=Sea(scale,scale,3)
    s.init_random()
    start=time.time()

    s.update()

    end=time.time()
    stastic.append(end-start)
    print(stastic)

