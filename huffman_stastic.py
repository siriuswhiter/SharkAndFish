from SEA import *
from RunLenCode import *
import re
import matplotlib.pyplot as plt
result=''
for t in range(3,6):
    for i in range(10,15):
        s=Sea(i,i,t)
        r=RLC()
        s.init_random()
        count=0
        while(not s.isOver() and  count!=100):

            result+=r.Sea2Code(s).split(' ')[3]
            s.update()
            count+=1

result=re.findall(r'[N,F,S]+\d{1,10}', result)

frequency={}
for i in set(result):
    frequency[i] = result.count(i)

frelist=sorted(frequency.items(),key=lambda item :item[1],reverse=True)
frequency={}
for i in frelist[0:20]:
    frequency[i[0]]=i[1]


code=list(frequency.keys())
fre=list((frequency.values()))

p1=plt.bar(code,fre)
print(code)
plt.show()

