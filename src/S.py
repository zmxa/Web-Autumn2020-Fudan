import socket
import threading
import mysql.connector
HOST = '127.0.0.1'  # 标准的回环地址 (localhost)
PORT = 65432        # 监听的端口 (非系统级的端口: 大于 1023)

#实际的数据库连接窗口
__cnx = mysql.connector.connect(user='root', password='123456',
                              host='127.0.0.1',
                              database='q')
COMMIT_COMMAND = bytes('commit','utf-8')
def log_and_lstrip(data,num):
    if(data.startswith('11')):
        data = data.lstrip('11');
        print("thread %d ask for %s." % (num,"search"))
        data = "select * from t"
    elif(data.startswith('12')):
        data = data.lstrip('12');
        print("thread %d ask for %s." % (num,"search"))
        data = "select * from t where "+data
    elif(data.startswith('2')):
        data = data.lstrip('2');
        print("thread %d ask for %s." % (num,"insert"))
        data = "insert into t values " + data
    elif(data.startswith('3')):
        data = data.lstrip('3');
        print("thread %d ask for %s." % (num,"delete"))
        data = "delete from t where " +data
    return data

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
                command = log_and_lstrip(data.decode(),num);
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



        
































