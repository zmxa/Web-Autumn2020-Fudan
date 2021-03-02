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
MySQL WorkBranch的数据库Q中，应至少有下列模式的表：
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
### 远程传递细节
使用SQL语言在服务端查询，客户端负责传递头部与详细参数
```
客户端发送       -->     服务端处理
"11"            -->     select * from table  
"12 ..."        -->     select * from table where ... and ...  
"2(a,b,...)"    -->     insert into table values (a, b, ...)  
"3 ..."         -->     delete from table where ...  
```
***
