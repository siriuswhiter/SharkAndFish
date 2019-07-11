from RunLenCode import *
from SEA import *
from twice_encode import *
scale=1
stastic=[]
stastic_2=[]
for i in range(6):
    l = [10, 33, 100, 319, 1000, 3190]
    scale = l[i]
    s=Sea(scale,scale,3)
    s.init_random()
    r=RLC()
    code=r.Sea2Code(s)
    stastic.append(len(code)/(2*scale*scale))
    t=Twice_encode()
    code_2=t.Sea2Tcode(s)
    stastic_2.append(len(code_2)/(2*scale*scale))
    print(stastic)
    print(stastic_2)