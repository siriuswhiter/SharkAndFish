from random import randint
import copy


class Sea:

    cells=[[]]
    stave=[[]]#每条鲨鱼的stavetime
    stavetime=3
    length=0
    width=0

    def __init__(self,length,width,stavetime):
        self.cells=[[0]*length for _ in range(width)]
        #数据结构需单独改写
        self.length=length
        self.width=width
        self.stavetime=stavetime
        self.stave=self.cells
        pass

    def init_by_coding(self,coding):
        pass

    def init_random(self):
        #30%为鱼，60%为空 10%为鲨鱼
        ran_ind=[0,0,0,0,0,0,0,1,1,2]
        self.cells=[[ran_ind[randint(0,9)] for _ in range(self.length) ]for _ in range(self.width)]
        self.stave=[[self.stavetime*(i//2) for i  in _  ]for _ in self.cells]
        pass

    def Get_Nearby_4Cell(self,i,j):
        #返回顺序为上下左右
        neighbor4=[]
        neighbor4.append(self.cells[i-1][j%self.length])
        neighbor4.append(self.cells[(i+1)%self.width][j%self.length])
        neighbor4.append(self.cells[i][j-1])
        neighbor4.append(self.cells[i][(j+1)%self.length])
        return neighbor4
        pass

    def Get_Nearby_8Cell(self,i,j):
        #返回顺序为左上到右下角
        neighbor8=[]
        neighbor8.append(self.cells[i-1][j-1])
        neighbor8.append(self.cells[i-1][j%self.length])
        neighbor8.append(self.cells[i-1][(j+1)%self.length])
        neighbor8.append(self.cells[i][j - 1])
        neighbor8.append(self.cells[i][(j+1)%self.length])
        neighbor8.append(self.cells[(i+1)%self.width][j-1])
        neighbor8.append(self.cells[(i+1)%self.width][j%self.length])
        neighbor8.append(self.cells[(i+1)%self.width][(j+1)%self.length])
        return neighbor8
        pass

    def get_cells(self,i,j):
        return self.cells[i][j]

    def update(self):

        next_cells=copy.deepcopy(self.cells)
        next_stave=copy.deepcopy(self.stave)
        for i in range(self.width):
            for j in range(self.length):
                neigh4 = self.Get_Nearby_4Cell(i, j)
                neigh8 = self.Get_Nearby_8Cell(i, j)
                if self.cells[i][j]==2:#如果cell为鲨鱼，以下情况
                    # 如果邻居有鱼，将饥饿度加满
                    if 1 in neigh8 :
                        next_stave[i][j]=self.stavetime
                    else:
                        next_stave[i][j]=self.stave[i][j]-1
                    '''else:
                        pos = randint(0,3)
                        while(1):
                            if(pos==0):
                                if(next_cells[i-1][j]==0):
                                    next_cells[i-1][j]=2
                                    next_stave[i-1][j]=next_stave[i][j]
                                    next_cells[i][j]=0
                                else:
                                    break
                            elif(pos==1):
                                if (next_cells[i][j - 1] == 0):
                                    next_cells[i][j - 1 ] = 2
                                    next_stave[i][j - 1]=next_stave[i][j]
                                    next_cells[i][j] = 0
                                else:
                                    break
                            elif (pos == 2):
                                if (next_cells[i][(j + 1) % self.length] == 0):
                                    next_cells[i][(j + 1) % self.length] = 2
                                    next_stave[i][(j + 1) % self.length]=next_stave[i][j]
                                    next_cells[i][j] = 0
                                else:
                                    break
                            elif (pos == 3):
                                if (next_cells[(i+1)%self.width][j] == 0):
                                    next_cells[(i+1)%self.width][j] = 2
                                    next_stave[(i+1)%self.width][j]=next_stave[i][j]
                                    next_cells[i][j] = 0
                                else:
                                    break
                            else:
                                break'''
                    if next_stave[i][j]<0:#下一轮饥饿度小于0即死亡
                            next_cells[i][j]=0

                elif self.cells[i][j]==1:
                    #如果为鱼，以下情况
                    if 2 in neigh8:
                        next_cells[i][j]=0
                    if sum([i*i*i*i for i in neigh8 ])>=32:
                    #如果邻居有两条鲨鱼则会变成鲨鱼
                        next_cells[i][j]=2
                        next_stave[i][j]=self.stavetime

                else:
                    #如果为空地，以下情况
                    if sum([i  for i in neigh8 if i!=2]) >= 2 and sum([i*i*i*i for i in neigh8 ])< 24:
                        next_cells[i][j]=1
                    if sum([i  for i in neigh8 if i!=2]) >= 2 and sum([i * i * i * i for i in neigh8]) >= 32:
                        next_cells[i][j]=2
                        next_stave[i][j]=self.stavetime

        self.cells=next_cells[:]
        self.stave=next_stave[:]

'''
    def update_small(self,x,y,s,t):
        #print(threading.enumerate())
        for i in range(x,s):
            for j in range(y,t):
                neigh4 = self.Get_Nearby_4Cell(i, j)
                neigh8 = self.Get_Nearby_8Cell(i, j)
                if self.cells[i][j] == 2:  # 如果cell为鲨鱼，以下情况
                    # 如果邻居有鱼，将饥饿度加满
                    if 1 in neigh4:
                        self.next_stave[i][j] = self.stavetime
                    else:
                        self.next_stave[i][j] = self.stave[i][j] - 1
                        if self.next_stave[i][j] < 0:  # 下一轮饥饿度小于0即死亡
                            self.next_cells[i][j] = 0

                elif self.cells[i][j] == 1:
                    # 如果为鱼，以下情况
                    if 2 in neigh8:
                        self.next_cells[i][j] = 0
                    if sum([i * i * i * i for i in neigh4]) >= 32:
                        # 如果邻居有两条鲨鱼则会变成鲨鱼
                        self.next_cells[i][j] = 2
                        self.next_stave[i][j] = self.stavetime

                else:
                    # 如果为空地，以下情况
                    if sum([i * i * i * i for i in neigh8]) >= 2 and sum([i * i * i * i for i in neigh8]) < 16:
                        self.next_cells[i][j] = 1
                    if sum([i for i in neigh8 if i != 2]) >= 2 and sum([i * i * i * i for i in neigh8]) >= 32:
                        self.next_cells[i][j] = 2
                        self.next_stave[i][j] = self.stavetime

    def update2(self):
        self.next_cells = copy.deepcopy(self.cells)
        self.next_stave = copy.deepcopy(self.stave)
        try:
            for i in range(int(self.width / 100)):
                for j in range(int(self.length / 100)):
                    _thread.start_new_thread(self.update_small, (i * 100, j * 100,(i+1) * 100, (j+1) * 100,))
                if self.length % 100 != 0:
                    _thread.start_new_thread(self.update_small,(i * 100, int(self.length / 100) * 100,(i+1) * 100, self.length,))
            if self.width % 100 != 0:
                _thread.start_new_thread(self.update_small,(int(self.width / 100) * 100, 0,self.width,self.length,))
        except:
            print("create thread error")
            exit(0)

        time.sleep(0.5)
        self.cells=copy.deepcopy(self.next_cells)
        self.stave=copy.deepcopy(self.next_stave)


'''