from tkinter import *
from tkinter.ttk import *
from tkinter.font import *
from PIL import Image,ImageTk
import time,os


import rFrame

import mysql.connector

class urp_box:
    '''登陆后的主页面'''

    def __init__(self,master,flag):
        #登录标志
        #数据库连接(数据库连接已改为远端)
        self.__flag__=flag
        '''self.__cnx = mysql.connector.connect(user='root', password='123456',
                              host='127.0.0.1',
                              database='q')'''

        #窗口定义
        self._window=master
        master.geometry("%dx%d+%d+%d" %(1200,500,25,25))
        master.attributes("-topmost",0)
        master.resizable(0,0)

        #字体与形式定义（Font,Style）
        self._font_welcome=Font(self._window,family="Aa语文老师的字",size=12)
        self._font_default=Font(self._window,family='Aa语文老师的字',size=20)
        Style().configure("Tbutton",font=self._font_default)

        
        #介绍文字
        if flag:
            tbd="欢迎您，本次登陆时间"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        else:
            tbd="您当前还没有登录"
        self._label1=Label(self._window,text=tbd,font=self._font_welcome)
        self._label1.place(relx=0.025*800/1200,rely=25/420)


        #左框--labelframe1
        self._labelframe1=LabelFrame(self._window,text="暂时可用功能",width=101,height=400)
        self._bm1=Button(self._labelframe1,text="学生信息",command=lambda:func1())
        self._bm1.place(x=5,y=0)
        self._labelframe1.place(relx=20/1200,rely=50/420)
        
        #右框--labelframe2--欢迎面
        self._labelframe2=LabelFrame(self._window,text="欢迎",width=490+149+400,height=400)

        fp = self.try_to_open(r'image.gif')
        tempimg = Image.open(fp,)
        ppp = ImageTk.PhotoImage(tempimg)
        lp1=Label(self._window,image=ppp)
        self._image=ImageTk.PhotoImage(tempimg)
        self._limage=Label(self._labelframe2,image=self._image,width=1030)
        self._limage.place(x=2,y=0)
        self._labelframe2.place(relx=151/1200,rely=50/420)
        fp.close()
        #预载入
        self._obj_func1=rFrame.c1(self._window,flag)
        
        def func1():
            #载入数据查询页面
            self._obj_func1._window.place(relx=151/1200,rely=50/420)

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
        
    def close(self):
        try:
            self._obj_func1.close_socket()
        except BaseException as e:
            print(e)
        finally:
            self._window.destroy()
            
if __name__=="__main__":
    urp_box_window=Tk()
    b=urp_box(urp_box_window,1)
    pass

