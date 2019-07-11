from tkinter import *
from tkinter import  filedialog
import  os
import SEA
from SEA import *
import RunLenCode
from RunLenCode import *
import twice_encode
from twice_encode import *

import _thread
import  threading
import  time

formWidth = 1000
formHeight = 700


class MainUI():
    def __init__(self,root,OceanWidth,OceanHeight,Starvetime):

        self.OceanWidth = OceanWidth
        self.OceanHeight = OceanHeight
        self.Starvetime = Starvetime
        self.sea = Sea(self.OceanWidth, self.OceanHeight, self.Starvetime)
        self.rlc = RLC()
        self.ted = Twice_encode()
        self.root = root

        global flag
        if  max(OceanHeight,OceanWidth) > 20 or OceanHeight < 6:
            flag = True
        else:
            flag = False

        if not flag:

            self.cellSize = int(480 / max(self.OceanWidth, self.OceanHeight)) if  int(480 / max(self.OceanWidth, self.OceanHeight))>0 else 1
            self.root.title("Shark and Fish vBeta 3.0")
            self.root.resizable(width=formWidth, height=self.OceanHeight)
            self.root.attributes('-alpha', 0.9)         #设置透明度
            size = '%dx%d' % (formWidth, formHeight)
            self.root.geometry(size)


            self.buttons = [[None for j in range(self.OceanWidth)] for i in range(self.OceanHeight)]
            self.units = [[SeaUnit(self, i, j) for j in range(self.OceanWidth)] for i in range(self.OceanHeight)]

            for i in range(self.OceanHeight):
                for j in range(self.OceanWidth):
                    self.buttons[i][j] = Button(self.root,
                                           bg='navy',
                                           activebackground='navy',
                                           bitmap="gray12",
                                           height=self.cellSize,
                                           width=self.cellSize,
                                           relief='raised',
                                           image=''
                                           )
                    self.buttons[i][j].bind("<Button-1>", self.units[i][j].left_click)
                    self.buttons[i][j].bind("<Button-3>", self.units[i][j].right_click)
                    self.buttons[i][j].grid(column=j, row=i, sticky=NW)# columnspan=self.OceanHeight-i, rowspan=self.OceanWidth-j)



            self.random = Button(self.root, bitmap='info', text='随机', height=self.cellSize*9/10, width=self.cellSize*3, relief='groove',state='normal', command=self.GetRandomSea,compound=LEFT)
            self.random.grid(column=self.OceanWidth+20, row=1,  sticky=W)
            self.start = Button(self.root, bitmap='info', text='开始', height=self.cellSize*9/10, width=self.cellSize*3, relief='groove',state='normal',command=self.Start,compound=LEFT)
            self.start.grid(column=self.OceanWidth+20, row=1+int(self.OceanHeight/5) ,  sticky=W)
            self.pause = Button(self.root, bitmap='info', text='暂停', height=self.cellSize*9/10, width=self.cellSize*3, relief='groove',state='disabled',command=self.Pause,compound=LEFT)
            self.pause.grid(column=self.OceanWidth+20, row=1+int(2*self.OceanHeight/5) , sticky=W)
            self.export = Button(self.root, bitmap='info', text='导出', height=self.cellSize*9/10, width=self.cellSize*3, relief='groove',state='normal',command=lambda:self.rlc.Export(self.sea),compound=LEFT)
            self.export.grid(column=self.OceanWidth+20, row=1+int(3*self.OceanHeight/5) , sticky=W)
            self.importb = Button(self.root, bitmap='info', text='导入', height=self.cellSize*9/10, width=self.cellSize*3, relief='groove',state='normal',command=self.importAndPrint,compound=LEFT)
            self.importb.grid(column=self.OceanWidth+20, row=1+int(4*self.OceanHeight/5) , sticky=W)

        else:
            self.cellSize = int(formHeight / max(self.OceanWidth, self.OceanHeight))
            self.root.title("Shark and Fish vBeta 3.0")
            self.root.resizable(width=formWidth+200, height=formHeight)
            self.root.attributes('-alpha', 0.9)  # 设置透明度
            size = '%dx%d' % (formWidth, formHeight)
            self.root.geometry(size)

            global canvas
            canvas = Canvas(self.root,bg='navy',width=self.cellSize*self.OceanWidth, height=self.cellSize*self.OceanHeight)
            canvas.grid(row=0,column=0,pady=0)

            for i in range(self.OceanHeight):
                for j in range(self.OceanWidth):
                    self.pos = '%d_%d' % (i,j)
                    canvas.create_rectangle(j*self.cellSize,i*self.cellSize,(j+1)*self.cellSize,(i+1)*self.cellSize,fill='navy',tags=('seaCell',self.pos))

            self.random = Button(self.root, text='随机', command=self.GetRandomSea,state='normal')
            self.random.grid(row=0, column=1, sticky=NW,pady=20,padx=50)
            self.start = Button(self.root, text='开始',command=self.Start,state='normal')
            self.start.grid(row=0, column=1, sticky=NW,pady=100,padx=50)
            self.pause = Button(self.root, text='暂停',command=self.Pause, state='disabled')
            self.pause.grid(row=0, column=1, sticky=NW, pady=180,padx=50)
            self.importb = Button(self.root, text='导入', command=self.importAndPrint, state='normal')
            self.importb.grid(row=0, column=1, sticky=NW,pady=260,padx=50)
            self.export = Button(self.root, text='导出', command=lambda :self.rlc.Export(self.sea), state='normal')
            self.export.grid(row=0, column=1, sticky=NW,pady=340,padx=50)



    def importAndPrint(self):
        self.s = self.ted.Tcode2Sea(self.rlc.Import())
        if self.s.length == self.sea.length and self.s.width == self.sea.width :
            self.sea = self.s
            self.Refresh()
        else:
            self.sea = self.s
            self.OceanWidth = self.s.length
            self.OceanHeight = self.s.width
            self.cellSize = int(formHeight / max(self.OceanWidth, self.OceanHeight))
            global  canvas
            canvas.delete()
            canvas = Canvas(self.root, bg='navy', width=self.cellSize * self.OceanWidth,
                            height=self.cellSize * self.OceanHeight)
            canvas.grid(row=0, column=0, pady=0)
            self.Refresh()




    def print(self,s,t,x,y):
        for i in range(s,x):
            for j in range(t,y):
                self.pos = '%d_%d' % (i, j)
                if self.sea.cells[i][j] == 2:
                    canvas.create_rectangle(j * self.cellSize, i * self.cellSize,  (j + 1) * self.cellSize,
                                            (i + 1) * self.cellSize,fill='red', tags=('seaCell', self.pos))
                elif self.sea.cells[i][j] == 1:
                    canvas.create_rectangle(j * self.cellSize, i * self.cellSize,  (j + 1) * self.cellSize,
                                            (i + 1) * self.cellSize,fill='green', tags=('seaCell', self.pos))
                else:
                    canvas.create_rectangle(j * self.cellSize, i * self.cellSize,  (j + 1) * self.cellSize,
                                            (i + 1) * self.cellSize,fill='navy', tags=('seaCell', self.pos))

    def Refresh(self):
        print("Refreshing")
        if not flag:
            for i in range(self.OceanHeight):
                for j in range(self.OceanWidth):
                    if self.sea.cells[i][j] == 2:
                        self.buttons[i][j].configure(bg='red')
                    elif self.sea.cells[i][j] == 1:
                        self.buttons[i][j].configure(bg='green')
                    else:
                        self.buttons[i][j].configure(bg='navy')
        else:
            try:
                for i in range(int(self.OceanHeight / 10)):
                    for j in range(int(self.OceanWidth / 10)):
                            _thread.start_new_thread(self.print,(i*10, j*10, i*10 + 10, j*10 + 10,))
                    if self.OceanWidth % 10 != 0:
                        _thread.start_new_thread(self.print, (i * 10, int(self.OceanWidth/10) * 10, i * 10 + 10, self.OceanWidth,))
                if self.OceanHeight % 10 != 0:
                    _thread.start_new_thread(self.print, (int(self.OceanHeight/10) * 10, 0, self.OceanHeight, self.OceanWidth,))
            except:
                print("create thread error")
                exit(0)




    def TimeLoop(self):
        self.sea.update()
        self.Refresh()
        global timer
        timer = threading.Timer(2,self.TimeLoop)
        timer.start()



    def Start(self):
        print('start')

        if self.start['state']=='normal':
            self.start['state'] = 'disabled'
            self.pause['state'] = 'normal'
            self.export['state'] = 'disabled'
            self.importb['state'] = 'disabled'

        global isStart,isActive
        isStart = False


        if not isStart:
            self.TimeLoop()
            isStart = True
            if not flag:
                self.random['state'] = 'disabled'

        else:
            timer.run()


    def Pause(self):
        print("pause")
        if self.pause['state'] == 'normal':
            self.start['state'] = 'normal'
            #self.pause['state'] = 'disabled'
            self.export['state'] = 'normal'
            self.importb['state'] = 'normal'
        for _ in threading.enumerate():timer.cancel()


    def GetRandomSea(self):
        self.sea.init_random()
        self.Refresh()




class SeaUnit:
    def __init__(self,ui_,i,j):
        self.ui = ui_
        self.i , self.j = i, j

    def left_click(self,argv):

        if self.ui.sea.cells[self.i][self.j] == 1:
            self.ui.sea.cells[self.i][self.j] = 0
            self.ui.buttons[self.i][self.j].configure(bg='navy')
        else:
            self.ui.sea.cells[self.i][self.j] = 1
            self.ui.buttons[self.i][self.j].configure(bg='green')
            #self.ui.buttons[self.i][self.j].configure(image='fish.gif')


    def right_click(self,argv):

        if self.ui.sea.cells[self.i][self.j] == 2:
            self.ui.sea.cells[self.i][self.j] = 0
            self.ui.buttons[self.i][self.j].configure(bg='navy')
        else:
            self.ui.sea.cells[self.i][self.j] = 2
            self.ui.buttons[self.i][self.j].configure(bg='red')
            #self.ui.buttons[self.i][self.j].configure(image=shark)


# 初始化时的界面显示
class ConfigUI:
    def __init__(self, root):
        self.root = root
        self.frame = Frame(self.root)
        self.vars = [StringVar() for i in range(4)]
        self.OceanWidth = Entry(self.frame, textvariable=self.vars[0])
        self.OceanHeight = Entry(self.frame, textvariable=self.vars[1])
        self.Starvetime = Entry(self.frame, textvariable=self.vars[2])

        self.OceanWidth.insert(0, "20")
        self.OceanHeight.insert(0, "20")
        self.Starvetime.insert(0,"3")
        
        Label(self.frame, text="海洋宽度").grid(row=0, column=0)
        Label(self.frame, text="海洋高度").grid(row=1, column=0)
        Label(self.frame, text="鲨鱼饥饿度").grid(row=2, column=0)

        self.OceanWidth.grid(row=0, column=1)
        self.OceanHeight.grid(row=1, column=1)
        self.Starvetime.grid(row=2, column=1)

        Button(self.frame,
               text='开始',
               command=lambda: (self.frame.destroy(),
                                MainUI(self.root,OceanWidth=int(self.vars[0].get()),OceanHeight=int(self.vars[1].get()),Starvetime=int(self.vars[2].get()))))\
            .grid(row=5, columnspan=3, sticky=W+E)

        self.frame.grid()



if __name__ == '__main__':
    root = Tk()
    root.title("setting...")

    cui = ConfigUI(root)


    cui.root.mainloop()


