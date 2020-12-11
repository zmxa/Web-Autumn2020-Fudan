from tkinter import *
from tkinter.ttk import *
from tkinter.font import *
import tkinter.messagebox
from PIL import Image,ImageTk

import re,time,os,socket
import mysql.connector

class remote_connection():
    def __init__(self,host,port):
            self._s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._s.connect((host,port))
            
    
    #用于数据库操作传递
    def send(self,msg):
        self._s.settimeout(10)
        #sendall : TypeError -->a bytes-like object is required, not 'str'
        try:
            self._s.sendall(bytes(msg,encoding='utf-8'))
        except ConnectionError as e:
            #print("Connection Lost: " +str(e))
            raise AssertionError("Connection Lost: " +str(e))
        result_string = ''
        while True:
            data = self._s.recv(10000)
            data = data.decode()
            if not data:
                break
            elif data.endswith('#'):
                result_string+=data
                break
            result_string+=data
        pat_error = re.compile(r"[0-9]+ \([0-9]+\):.+")
        if pat_error.findall(result_string) != []:
            raise AssertionError(result_string)
            #return None
        else:
            pat_result = re.compile(r'''\(["', \-\.\w\u4e00-\u9fa5]+\)''')
            li = pat_result.findall(result_string)
            
            self._s.settimeout(3600)
            return [eval(r) for r in li]
    
    #用于数据库的增删操作后提交
    def commit(self):        
        #对本机超时限制
        self._s.settimeout(10)
        #在服务端区分操作实质
        self._s.sendall(b"commit")
        
        while True:
            data = self._s.recv(10000)
            data = data.decode()
            if not data:
                break
            elif data.endswith('#'):
                break
        self._s.settimeout(3600)
        
    def close(self):
        self._s.close()
        
#教师信息
class c1():
    
    def __init__(self,master,flag):
        #主窗口
        self._rootwindow = master
        #True
        self.__flag=flag
        #数据库
        #self.__cnx=cnx
        #更新数据长度
        self._lastitemcount=9999
        #当前根窗口，即urpbox内的rframe
        self._window=LabelFrame(master,text="学生信息",width=1039,height=400)
        #字体路径
        self._font1=Font(self._window,family="Aa语文老师的字",size=11)
        
        #远程连接数据库---------------------------------------------------------
        try:
            self._rdatabase = remote_connection('127.0.0.1', 65432)
        except ConnectionError as e:
            print(e)
            self._rootwindow.destroy()
            return
        
        #左侧的搜索框
        self._l1=Label(self._window,font=self._font1,text="学号",anchor=W)
        self._e1=Entry(self._window,width=16)
        self._l2=Label(self._window,font=self._font1,text="姓名",anchor=W)
        self._e2=Entry(self._window,width=16)
        self._l3=Label(self._window,font=self._font1,text="电话",anchor=W)
        self._e3=Entry(self._window,width=16)
        self._l4=Label(self._window,font=self._font1,text="院系",anchor=W)
        self._e4=Entry(self._window,width=16)
        self._l5=Label(self._window,font=self._font1,text="备注",anchor=W)
        self._e5=Entry(self._window,width=16)
        self._l6=Label(self._window,font=self._font1,text="照片",anchor=W)
        self._e6=Entry(self._window,width=16)
        #self._e1.insert(INSERT,"") 默认值
        
        #左侧搜索框定位显示
        self._le=[self._l1,self._e1,self._l2,self._e2,self._l3,self._e3,self._l4,self._e4,self._l5,self._e5,self._l6,self._e6]
        temp=-18
        for item in self._le:
            temp+=23
            item.place(x=15,y=temp)

        #左下角的仨按钮
        self._b1=Button(self._window,text="查找",command=lambda:self.b_search(),width=4)
        self._b1.place(x=15,y=290)
        self._b2=Button(self._window,text="添加",command=lambda:self.b_add(),width=4)
        self._b2.place(x=55,y=290)
        self._b3=Button(self._window,text="删除",command=lambda:self.b_delete(),width=4)
        self._b3.place(x=95,y=290)

        #看照片用的按钮 TODO()!!
        self._b4=Button(self._window,text="照片",command=lambda:self.b_detailsearch(),width=4)
        self._b4.place(x=135,y=290)
        
        #初始展示照片
        #0.png  -->初始照片
        #1.png  -->唯一的查询结果没有照片
        #2.png  -->查询结果个数>1
        #13.png -->结果个数为0
        #14.png -->完全找不到照片
        #调用try_to_open -->优先绝对路径（但是绝对路径会因为字符串问题报错！），再相对查找，最后打开既定照片。
        fp = self.try_to_open(r'00.png')
        tempimg = Image.open(fp,)
        ppp = ImageTk.PhotoImage(tempimg)
        lp1=Label(self._window,image=ppp)
        self._p1=ImageTk.PhotoImage(tempimg)
        self._lp1=Label(self._window,image=self._p1,)
        self._lp1.place(x=665+(190-self._p1.width())/2,y=28)
        del tempimg
        fp.close()
        
        #主要查询窗口
        self._lt=Label(self._window,font=self._font1,text="查询结果")
        self._lt.place(x=160,y=5)
        self._tree=Treeview(self._window,show="headings")
        self.__temp=("学号","姓名","电话","院系","备注","照片位置")
        self.__temp2=("t_n","tname","tcall","depart","other","photo")
        self._tree["columns"]=("t_n","tname","tcall","depart","other","photo")
        for item in range(2):
            self._tree.column(self.__temp2[item],width=60)
            self._tree.heading(self.__temp2[item],text=self.__temp[item])
        for item in range(2,4):
            self._tree.column(self.__temp2[item],width=100)
            self._tree.heading(self.__temp2[item],text=self.__temp[item])
        for item in range(4,6):
            self._tree.column(self.__temp2[item],width=90)
            self._tree.heading(self.__temp2[item],text=self.__temp[item])
        self._tree.place(x=160,y=28)

        #返回信息窗口
        self._lfr=LabelFrame(self._window,width=150,height=290,text="上一条返回信息")
        self._lr1=Label(self._lfr,text=' ',width=94,foreground="red",wraplength=90)
        self._lr1.place(x=15,y=5)
        self._lfr.place(x=865,y=19)
        
        #查询信息填充
        self.b_search()
    def lr1_errhandle(self,currenterror):
        global master
        self.currenterror=str(currenterror)
        self._lr1.configure(text=self.currenterror)
        if self.currenterror.startswith("Conn"):
            self.quitall()
        print(currenterror)
    def quitall(self):
        time.sleep(1)
        self.close_socket()
        self._window.destroy()
        self._rootwindow.destroy()
        
    #连接数据库并返回结果
    def b_search(self,errlr = ""):
        self._lr1.configure(text=errlr)
        self.tempcur=[]
        self.templist=[]
        self.tempe=self._le[1:6:2]
        i=0
        for item in self.tempe:
            if item.get()!='':
                self.templist.append(""+self.__temp2[i]+"='"+item.get()+"'")
            i+=1
        if self.templist==[]:
            try:
                self.tempcur = self._rdatabase.send("1select * from t")
            except TimeoutError as currenterror:
                self.lr1_errhandle(currenterror)
            except AssertionError as currenterror:
                self.lr1_errhandle(currenterror)
        else:
            try:
                self.tempcur = self._rdatabase.send("1select * from t where "+' and '.join(self.templist))
            except TimeoutError as currenterror:
                self.lr1_errhandle(currenterror)
            except AssertionError as currenterror:
                self.lr1_errhandle(currenterror)
        i=0
        self.clear_tree()
        for item in self.tempcur:
            #q = (*item[0:4],item[5])
            self._tree.insert("",i,text=str(i),iid=i,values=item)
            i+=1
        self._lastitemcount=i-1
        del self.tempcur,self.templist,self.tempe,i
        
    #增加操作 
    def b_add(self):
        errtext = ''
        self._lr1.configure(text=" ")
        self.tempcur=[]
        self.templist=[];
        self.tempe=self._le[1::2]
        
        for item in self.tempe:
            self.templist.append("\""+item.get()+"\"")
        if self.templist[0]=='""' or self.templist[1]=='""':
            self._lr1.configure(text="姓名与学号不能为空")
            return
        try:
            self.tempcur = self._rdatabase.send("2insert into t values (%s,%s,%s,%s,%s,%s)" % tuple(self.templist))
            self._rdatabase.commit()
            
        except TimeoutError as currenterror:
            self.lr1_errhandle(currenterror)
            errtext = currenterror
        except AssertionError as currenterror:
            self.lr1_errhandle(currenterror)
            errtext = currenterror
        for item in self.tempe:
            item.delete(0,END)
        del self.tempcur,self.templist,self.tempe
        self.b_search(errlr = errtext)
        
    #删除操作  
    def b_delete(self):
        errtext = ''
        self._lr1.configure(text=" ")
        self.tempcur=[]
        self.templist=[]
        self.tempe=self._le[1::2]
        i=0
        for item in self.tempe:
            if item.get()!='':
                self.templist.append(""+self.__temp2[i]+"='"+item.get()+"'")
            i+=1
        if self.templist==[]:
            self._lr1.configure(text="不能无条件全部删除")
            return
        else:
            try:
                self.tempcur = self._rdatabase.send("3delete from t where "+' and '.join(self.templist))
                self._rdatabase.commit()
                
            except TimeoutError as currenterror:
                self.lr1_errhandle(currenterror)
                errtext = currenterror
            except AssertionError as currenterror:
                self.lr1_errhandle(currenterror)
                errtext = currenterror
        for item in self.tempe:
            item.delete(0,END)
        del self.tempcur,self.templist,self.tempe
        self.b_search(errlr=errtext)
    
    #尝试打开照片
    def try_to_open(self,userpath):
        WORKING_PATH = os.getcwd()
        try:
            print(userpath)
            fp = open(userpath,'rb')
            return fp
        except FileNotFoundError:
            pass
        try:
            print(WORKING_PATH+'\\'+userpath)
            fp = open(WORKING_PATH+'\\'+userpath,'rb')
            return fp
        except FileNotFoundError:
            pass
        try:
            print(WORKING_PATH+'\\img\\'+userpath)
            fp = open(WORKING_PATH+'\\img\\'+userpath,'rb')
            return fp
        except FileNotFoundError:
            pass
        try:
            return open(r'E:\复旦小学的资料\第七学期\计算机网络\实验\实验5\img\14.png','rb')
        except FileNotFoundError:
            raise AssertionError(r'未找到 E:\复旦小学的资料\第七学期\计算机网络\实验\实验5\img\14.png','rb')
                                 
    #对唯一结果显示照片
    def b_detailsearch(self):
        self._lr1.configure(text="")
        self.tempcur=[]
        self.templist=[]
        self.tempe=self._le[1:6:2]
        i=0
        for item in self.tempe:
            if item.get()!='':
                self.templist.append(""+self.__temp2[i]+"='"+item.get()+"'")
            i+=1
        if self.templist==[]:
            try:
                self.tempcur = self._rdatabase.send("1select * from t")
            except TimeoutError as currenterror:
                self.lr1_errhandle(currenterror)
            except AssertionError as currenterror:
                self.lr1_errhandle(currenterror)
        else:
            try:
                self.tempcur = self._rdatabase.send("1select * from t where "+' and '.join(self.templist))
            except TimeoutError as currenterror:
                self.lr1_errhandle(currenterror)
            except AssertionError as currenterror:
                self.lr1_errhandle(currenterror)
        i=0
        self.clear_tree()
        temp_record = 0
        for item in self.tempcur:
            self._tree.insert("",i,text=str(i),iid=i,values=item)
            if(i==0): temp_record = item
            i+=1
        #仅有一个结果时查看相应的照片
        
        if i==1:
            if temp_record[-1]!= None and temp_record[-1]!='':
                fp = self.try_to_open(temp_record[-1])
                tempimg = Image.open(fp)
                self._p1=ImageTk.PhotoImage(tempimg)
                self._lp1.configure(image=self._p1,)
                del tempimg
                fp.close()
            else:
                fp = self.try_to_open('01.png')
                self._lr1.configure(text="查询结果没有照片！")
                tempimg = Image.open(fp)
                self._p1=ImageTk.PhotoImage(tempimg)
                self._lp1.configure(image=self._p1,)
                del tempimg
                fp.close()
        elif i>1:
            fp = self.try_to_open('02.png')
            self._lr1.configure(text="查询结果多于一个！请更精确查询！")
            tempimg = Image.open(fp)
            self._p1=ImageTk.PhotoImage(tempimg)
            self._lp1.configure(image=self._p1,)
            del tempimg
            fp.close()
        else:
            fp = self.try_to_open('13.png')
            self._lr1.configure(text="没有结果！")
            tempimg = Image.open(fp)
            self._p1=ImageTk.PhotoImage(tempimg)
            self._lp1.configure(image=self._p1,)
            del tempimg
            fp.close()
        
        self._lastitemcount=i-1
        del self.tempcur,self.templist,self.tempe,i
    
    def clear_tree(self):
        i=0
        if self._lastitemcount ==9999:
            return
        while i<=self._lastitemcount:
            self._tree.delete(i)
            i+=1
        self._lastitemcount ==9999
    def close_socket(self):
        self._rdatabase.close()
if __name__ == '__main__':
    from urp_box import *
    urp_box_window=Tk()
    b=urp_box(urp_box_window,True)
    mainloop()
