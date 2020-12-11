# Web实验报告 
### 实验选题
设计类HTTP协议
***
### 实验环境
本实验在python 3.7.0下编写，后端数据存放在MySQL Workbench。运行需额外安装`mysql-connector`，可在命令行中通过[`pip install mysql-connector-python`][1]安装。实验的UI使用`tkinter`，原[教程][2]现不能访问。

[1]: https://dev.mysql.com/doc/connector-python/en/connector-python-installation.html 'mysql-connector文档'
[2]: http://effbot.org/tkinterbook/tkinter-hello-again.htm 'tkinter参考教程'

***

### 文件结构
请先打开服务端S.py，再启动maimn.pyw。
同时您应当具有相同的服务器登录方式：
```
user='root', password='123456', host='127.0.0.1', database='q'
```
MySQL Branch的数据库Q中，应至少有下列模式的表：
```
create table t(     |   create table c(
t_n varchar(14),    |   c_n varchar(14),
tname varchar(10),  |   cname varchar(10),
tcall varchar(10),  |   t_n varchar(14),
depart varchar(4),  |   ccredit varchar(3),
other varchar(10),  |   cother varchar(10), 
primary key(t_n)    |   primary key(c_n),
);                  |   foreign key(t_n) references t(t_n)
                    |   );
```
```
src
├── img             //图片文件夹
├── maimn.pyw       //主入口
├── README.md       //
├── rFrame.py       //
├── S.py            //服务端
└── urp_box.py      //
```
***
### 实验截图
截图将另附文件夹上传

***
### 可做改进
1. UI设计相关仍可继续优化，例如通过Treeview上的交互进行查询。
2. 所有互动局发生在同一窗体，可以在新窗口展示详细信息
3. 关系型数据库可提供更多表的建立，更多数据的加入
4. 预留了flag标签，可用于登录窗体建立。

***

### 程序代码与实现分析
`maimn.pyw`

```python
from urp_box import *


urp_box_window=Tk()
try:
    b=urp_box(urp_box_window,True)
    urp_box_window.protocol('WM_DELETE_WINDOW', b.close)
    mainloop()
except TclError:
    print("I guess you didn't open S.py")
except AssertionError:
    pass
```
作为入口函数，maimn提供Tk()窗口并传递给内层窗口类。因后端未连接导致的关闭交由异常处理解决。详细内容后述。  

***

`urp_box.py`  
class urp_box实质是承载查询界面的窗口，可日后拓展其他的查询。`def __init__(self,master,flag):`内的样式初始化如下。
```python
#可以日后延伸作为登录标志
self.__flag__=flag

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
......
```
\_\_init\_\_内左部菜单与右部展示图  
```python
#左框--labelframe1
self._labelframe1=LabelFrame(self._window,text="暂时可用功能",width=101,height=400)
self._bm1=Button(self._labelframe1,text="学生信息",command=lambda:func1())
self._bm1.place(x=5,y=0)
self._labelframe1.place(relx=20/1200,rely=50/420)

#右框--labelframe2--欢迎面
self._labelframe2=LabelFrame(self._window,text="欢迎",width=490+149+400,height=400)
self._image=PhotoImage(file=r'img\image.gif')
self._limage=Label(self._labelframe2,image=self._image,width=1030)
self._limage.place(x=2,y=0)
self._labelframe2.place(relx=151/1200,rely=50/420)
```  
左框中包含按钮用于选择功能。点击后显示查询页面。
```python
def func1():
#载入数据查询页面
    self._obj_func1._window.place(relx=151/1200,rely=50/420)
```
实际的加载由class rFrame在init中进行。
```python
#预载入
self._obj_func1=rFrame.c1(self._window,flag)
```
当用户主动关闭窗体时，由`urp_box_window.protocol('WM_DELETE_WINDOW', b.close)`捕获动作，触发关闭动作。此时urp_box尝试关闭内层连接，并在发生任何错误时关闭窗体。
```python
def close(self):
        try:
            self._obj_func1.close_socket()
        except BaseException as e:
            print(e)
        finally:
            self._window.destroy()
```
***
`rFrame.py`  
`class c1`是查询窗口的UI界面，`def __init__(self,master,flag)`按下列顺序进行初始化。
```python
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
```
数据库链接时要防止连接错误，任何能被异常处理捕获的错误都将导致窗口退出，触发最外层的退出，以免在窗口继续触发更多错误。
```python
try:
    self._rdatabase = remote_connection('127.0.0.1', 65432)
except ConnectionError as e:
    print(e)
    self._rootwindow.destroy()
    return
```
其他相关部件
```python
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

#看照片用的按钮 
self._b4=Button(self._window,text="照片",command=lambda:self.b_detailsearch(),width=4)
self._b4.place(x=135,y=290)
```
关于查询页面的初始照片展示，使用`try_to_open`函数尝试在实验路径与设定路径进行一次搜索，都找不到就报错退出。使用`open` --> `Image.open` --> `ImageTk.PhotoImage` --> `Label.configure` --> `close`的方法可以重复使用相同图片，避免在文件系统不能重复打开导致的错误。
```python
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
```
上述尝试打开函数。
```PY
#尝试打开照片
def try_to_open(self,userpath):
    WORKING_PATH = os.getcwd()
    try:
        fp = open(userpath,'rb')
        return fp
    except FileNotFoundError:
        pass
    try:
        fp = open(WORKING_PATH+'\\'+userpath,'rb')
        return fp
    except FileNotFoundError:
        pass
    try:
        fp = open(WORKING_PATH+'\\img\\'+userpath,'rb')
        return fp
    except FileNotFoundError:
        pass
    try:
        return open(r'----此处删去----','rb')
    except FileNotFoundError:
        raise AssertionError(r'未找到 ----此处删去----','rb')
```
查询的主要展示窗口使用一个Treeview。
```PY
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
#查询信息填充
self.b_search()
```
在查询展示窗口右侧提供用于展示错误信息的窗口，对数据库操作导致的添加时主键重复等、删除时尚有外键引用等、用户自定义错误、远程连接超时等提供显示支持，避免内部错误导致整体退出。
```PY
#返回信息窗口
    self._lfr=LabelFrame(self._window,width=150,height=290,text="上一条返回信息")
    self._lr1=Label(self._lfr,text=' ',width=94,foreground="red",wraplength=90)
    self._lr1.place(x=15,y=5)
    self._lfr.place(x=865,y=19)
```
错误处理函数
```PY
def lr1_errhandle(self,currenterror):
    global master
    self.currenterror=str(currenterror)
    self._lr1.configure(text=self.currenterror)
    if self.currenterror.startswith("Conn"):
        self.quitall()
    print(currenterror)
def quitall(self):
    time.sleep(1)
    #释放连接
    self.close_socket()
    #关闭窗口
    self._window.destroy()
    self._rootwindow.destroy()
def close_socket(self):
    self._rdatabase.close()
```
对于数据库的查、删、增操作,其流程可以大致为：
1. 若无延续问题则清空故障信息
2. 准备查询信息
3. 向远程数据库发送请求并等待反馈
4. 若无故障，对于增加、删除操作进行事务提交
5. 若无故障，清空当前数据展示窗口并重新填充
6. 若有故障，交由故障处理函数解决。

另外，通过`图片`按钮进行的查询仅在结果唯一时更新照片，若结果为空或结果数目多于2，则展示预设定的图片。
```python
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
```
用于清空Treeview。
```py
def clear_tree(self):
    i=0
    if self._lastitemcount ==9999:
        return
    while i<=self._lastitemcount:
        self._tree.delete(i)
        i+=1
    self._lastitemcount ==9999
```
***
`S.py`
数据库连接
```py
__cnx = mysql.connector.connect(user='root', password='123456', host='127.0.0.1', database='q')
```
远程服务器使用Thread模块进行简单的多线程并发，由于SQL server对事务的锁机制，以及客户端在收到回答后尽快进行提交，服务器端可以进行简单的互斥数据管理。
```PY
index = 0

if __name__ == "__main__":
    print("Server is starting")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))  # 配置soket，绑定IP地址和端口号
    s.listen(5)  # 设置最大允许连接数，各连接和server的通信遵循FIFO原则
    s.settimeout(600)
    print( "Server is listenting port 65432, with max connection 5")
    
    while True:  # 循环轮询socket状态，等待访问
        try:
            conn, addr = s.accept()
        except TimeoutError:
            s.close()
            print("晚安！")
            break
        index += 1
        # 当获取一个新连接时，启动一个新线程来处理这个连接
        print('thread %d starting.'% index)
        tempt = threading.Thread(target=child_connection,args = (index, s, conn))
        tempt.start()
        if index > 7:
            break
    s.close()
```
其中的`child_connection`作为线程需调用的函数，对所有客户端发来的命令进行处理。
```PY
COMMIT_COMMAND = bytes('commit','utf-8')
#头部信息解码并在服务端记录
def log_and_lstrip(data,num):
    if(data.startswith('1')):
        data = data.lstrip('1');
        print("thread %d ask for %s." % (num,"search"))
    elif(data.startswith('2')):
        data = data.lstrip('2');
        print("thread %d ask for %s." % (num,"insert"))
    elif(data.startswith('3')):
        data = data.lstrip('3');
        print("thread %d ask for %s." % (num,"delete"))
    return data

#使用线程解决客户端请求
def child_connection(num, s, conn):
    print('Connected by', addr)
    try:
        conn.settimeout(60)
        while True:
            try:
                data = conn.recv(10000)
            except TimeoutError as e:
                print("thread %d wait too long" % num)
                raise TimeoutError                
            if not data:
                break
            if data.startswith(COMMIT_COMMAND):
                __cnx.commit()
                conn.sendall(bytes('#',encoding = 'utf-8'))
            else:
                command = log_and_lstrip(data.decode(),num)
                temp_cur = __cnx.cursor()
                
                try:
                    temp_cur.execute(command)
                    for item in temp_cur:
                        conn.send(bytes(str(item),encoding = 'utf-8'))
                except BaseException as e:
                    print("thread %d" % num,end='')
                    print(e)
                    conn.send(bytes(str(e),encoding = 'utf-8'))
                finally:
                    conn.sendall(bytes(str('#'),encoding = 'utf-8'))
    except TimeoutError:
        print('time out thread %d'% num)
    except BaseException as e:
        print("thread %d" % num,end='')
        print(e)
    finally:
        print("closing connection %d" % num)# 当一个连接监听循环退出后，连接可以关掉
        global index
        index -=1
        conn.close()
```
内层的异常处理块保证从数据库方向传来的错误一定能发送给客户端，同时本地也提供记录。而对于外层的异常处理块，不论发送时超时或是接受时超时，线程一定会关闭再退出。
***
