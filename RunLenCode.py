from SEA import *
from twice_encode import  *
from tkinter import  filedialog
import re
import os
import  copy
class RLC:

    def Export(self,s):       #将转换后的str传入，并写成文本文件，注意后缀
        self.ted = Twice_encode()
        self.default_dir = r"C:\Users\薛文杰\Desktop\鲨鱼与鱼\RunLenCode"
        self.file_path = filedialog.asksaveasfilename(title=u'保存游程编码文件',
                                                      defaultextension='.rlc',
                                                      initialdir=(os.path.expanduser(self.default_dir)),
                                                      filetypes=[('runlencode', '*.rlc')])
        self.rlc = self.ted.Sea2Tcode(s)
        try:
            with open(self.file_path, 'w') as f:
                f.write(self.rlc)
        except:
            pass


    def Import(self):
        self.default_dir = r"C:\Users\薛文杰\Desktop\鲨鱼与鱼\RunLenCode"
        self.file_path = filedialog.askopenfilename(title=u'选择游程编码文件',
                                                    initialdir=(os.path.expanduser(self.default_dir)),
                                                    filetypes=[('runlencode', '*.rlc')])
        try:
            with open(self.file_path, 'r') as f:
                self.rlc = f.readline()
        except FileNotFoundError:
            pass
        return  self.rlc

    def Sea2Code(self,s):
        cell1d = [_ for i in s.cells for _ in i]  # 转化为一维
        for i in range(cell1d.__len__()):  # 将其替换成为Fish,Shark,None的首字母
            if cell1d[i] == 1:
                cell1d[i] = 'F'
            if cell1d[i] == 2:
                cell1d[i] = 'S'
            if cell1d[i] == 0:
                cell1d[i] = 'N'

        result=''+str(s.stavetime)+' '      #‘ ’将长宽分开
        result+=str(s.length)+' '
        result+=str(s.width)+' '
        last=-1
        num=1

        for i in cell1d:
            if i!=last:

                if last!=-1:
                    result+=str(num)
                    num=1
                result += i
                last = i

            else:
                num+=1
        result+=str(num)+' '+"".join([str(i)  for item in s.stave for i in item if i!=0])
        return result

    def Code2Sea(self,str):

        stavetime,length,width,code,stave=str.split(' ')
        s=Sea(int(length),int(width),int(stavetime))
        array=[]
        seq = re.findall(r'[N,F,S]+|\d{1,10}', code)
        for i in seq:
            if i=='F':
                species=1
            elif i=='S':
                species=2
            elif i=='N':
                species=0
            else:
               array+=[species for _ in range(int(i))]
        array=[array[i*int(length):(i+1)*int(length)]for i in range(int(width))]
        s.cells=copy.deepcopy(array)
        s.stave=copy.deepcopy(array)
        last=0
        for i in range(s.width):
            for j in range(s.length):
                if s.cells[i][j]==2:
                    s.stave[i][j]=int(stave[last])
                    last+=1
                else:
                    s.stave[i][j]=0
        return s                    #返回一个实例的海洋

