面向对象
类
封装
继承
多态
class Role(object):
	n=3  # 类变量
    def __init__(self,name,role,weapon,life_value=100,money=15000):
        self.name = name  #实例变量（静态属性），作用域就是实例本身
        self.role = role
        self.weapon = weapon
        self.__life_value = life_value #私有属性，只能在类里修改，实例后不能修改，定义一方法修改私有属性后，实例可以通过方法来修改
        self.money = money
 
    def shot(self):  #类的方法，功能，（动态属性）
        print("shooting...")
 
    def __got_shot(self):#私有方法
        print("ah...,I got shot...")
 
    def buy_gun(self,gun_name):
        print("just bought %s" %gun_name)
 
r1 = Role('Alex','police','AK47’) #生成一个角色

r1.name="陈龙" #重新赋值

r1.bullet_prove=True  #添加新的属性

del r1.weapon  # 删除属性

r2 = Role('Jack','terrorist','B22’)  #生成一个角色


print(Role.n)
print(r1.n)
#实例变量和类变量   

#析构函数：在实例释放的时候执行的，如关闭数据连接，文件关闭

def __del__(self):
	print("del done")

########################


#类的继承
#所有类继承object类
class Person(object):
	def sleep(self):
		print("a is sleep")

class Man(Person):

	def sleep(self) #方法重构，并用父类内容
		Person.sleep(self)
		print("B is sleep")		

###################################


class SchoolMember(object):
    members = 0 #初始学校人数为0
    def __init__(self,name,age):
        self.name = name
        self.age = age
 
    def  tell(self):
        pass
 
    def enroll(self):
        '''注册'''
        SchoolMember.members +=1
        print("\033[32;1mnew member [%s] is enrolled,now there are [%s] members.\033[0m " %(self.name,SchoolMember.members))
     
    def __del__(self):
        '''析构方法'''
        print("\033[31;1mmember [%s] is dead!\033[0m" %self.name)
class Teacher(SchoolMember):
    def __init__(self,name,age,course,salary):#析构函数的重构
        super(Teacher,self).__init__(name,age) 
        self.course = course
        self.salary = salary
        self.enroll()
 
 
    def teaching(self):
        '''讲课方法'''
        print("Teacher [%s] is teaching [%s] for class [%s]" %(self.name,self.course,'s12'))
 
    def tell(self):
        '''自我介绍方法'''
        msg = '''Hi, my name is [%s], works for [%s] as a [%s] teacher !''' %(self.name,'Oldboy', self.course)
        print(msg)
 
class Student(SchoolMember):
    def __init__(self, name,age,grade,sid):
        super(Student,self).__init__(name,age)
        self.grade = grade
        self.sid = sid
        self.enroll()
 
 
    def tell(self):
        '''自我介绍方法'''
        msg = '''Hi, my name is [%s], I'm studying [%s] in [%s]!''' %(self.name, self.grade,'Oldboy')
        print(msg)
 
if __name__ == '__main__':
    t1 = Teacher("Alex",22,'Python',20000)
    t2 = Teacher("TengLan",29,'Linux',3000)
 
    s1 = Student("Qinghua", 24,"Python S12",1483)
    s2 = Student("SanJiang", 26,"Python S12",1484)
 
    t1.teaching()
    t2.teaching()
    t1.tell()



#######################################
#多态

class Animal(object):
    def __init__(self, name):  # Constructor of the class
        self.name = name
 
    def talk(self):              # Abstract method, defined by convention only
        raise NotImplementedError("Subclass must implement abstract method")
 
 
class Cat(Animal):
    def talk(self):
        print('%s: 喵喵喵!' %self.name)
 
 
class Dog(Animal):
    def talk(self):
        print('%s: 汪！汪！汪！' %self.name)
 
 
 
def func(obj): #一个接口，多种形态
    obj.talk()
 
c1 = Cat('小晴')
d1 = Dog('李磊')
 
func(c1)
func(d1)




#############################
#静态方法
class Dog(object):
 
    def __init__(self,name):
        self.name = name
 
    @staticmethod #把eat方法变为静态方法，
    def eat(self):
        print("%s is eating" % self.name)
 
 
 
d = Dog("ChenRonghua")
d.eat()

#通过@staticmethod装饰器即可把其装饰的方法变为一个静态方法，什么是静态方法呢？其实不难理解，普通的方法，可以在实例化后直接调用，并且在方法里可以通过self.调用实例变量或类变量，但静态方法是不可以访问实例变量或类变量的，一个不能访问实例变量和类变量的方法，其实相当于跟类本身已经没什么关系了，它与类唯一的关联就是需要通过类名来调用这个方法


#类方法

class Dog(object):
    name = "我是类变量"
    def __init__(self,name):
        self.name = name
 
    @classmethod
    def eat(self):
        print("%s is eating" % self.name)
 
 
 
d = Dog("ChenRonghua")
d.eat()

# 类方法通过@classmethod装饰器实现，类方法和普通方法的区别是， 类方法只能访问类变量，不能访问实例变量

#属性方法

#属性方法的作用就是通过@property把一个方法变成一个静态属性
class Dog(object):
 
    def __init__(self,name):
        self.name = name
        self.__food=None
 
    @property
    def eat(self):
        print(" %s is eating %s" %self.name,self.__food)
    @eat.setter
    def eat(self,food)
    	print("set food",food)
    	self.__food=food
    @eat.deleter
    	def eat(self)
    		del self.__food
    		print("删完了")
 
 
d = Dog("ChenRonghua")
d.eat="baozi" #就会执行@eat.setter
d.eat
del d.eat   #就会执行@eat.deleter

#航班状态案例属性方法
class Flight(object):
    def __init__(self,name):
        self.flight_name = name


    def checking_status(self):
        print("checking flight %s status " % self.flight_name)
        return  1


    @property
    def flight_status(self):
        status = self.checking_status()
        if status == 0 :
            print("flight got canceled...")
        elif status == 1 :
            print("flight is arrived...")
        elif status == 2:
            print("flight has departured already...")
        else:
            print("cannot confirm the flight status...,please check later")
    
    @flight_status.setter #修改
    def flight_status(self,status):
        status_dic = {
            0 : "canceled",
            1 :"arrived",
            2 : "departured"
        }
        print("\033[31;1mHas changed the flight status to \033[0m",status_dic.get(status) )

    @flight_status.deleter  #删除
    def flight_status(self):
        print("status got removed...")

f = Flight("CA980")
f.flight_status
f.flight_status =  2 #触发@flight_status.setter 
del f.flight_status #触发@flight_status.deleter 


#########################################
#反射   通过字符串映射或修改程序运行时的状态、属性、方法, 有以下4个方法
#hasattr  getattr  setattr delattr
def  bluk(self):
	print("88888888888")
class Dog(object):
	def  __init__(self,name)
		self.name=name

	def eat(self)
		print("%s is eating",self.name)

d=Dog("black dog")

choice=input(">>:").strip()

if hasattr(d,choice)

   fun=getattr(d,choice)
   fun()
else
	setter(d,choice,bluk)
	fun=getattr(d,choice)
	fun(d)



####################################
网络七层模型osi
物理层
数据链路 MAC
网络  IP
传输
会话
表示
应用

TCP/IP 三次握手四次断开
syn --> ack/syn
			|
			|
			ack

#socket_client
import socket
client=socket.socket()#申明socker类型，同时生成socke连接对象
client.Connect(('localhost',6969))
while True:
	msg=input(">>").strip
	if len(msg):
		continu
	client.send(msg.encode("utf-8"))
	cmd_size=client.recv(1024)

	client.sendall("确认")#防止粘包
	
	received_size=0
	while received_size<cmd_size:
		  if cmd_size-received_sisz<1024
		  		data=client.recv(cmd_size-received_sisz)
		  data=client.recv(1024)
		  received_size+=len(data)

	print(data.decode())
client.close()

#socket_server
import socket
server=socket.socket()
server.bind(('localhost',6969))
server.listen()
while True:
	 
	conn,addr=server.accept()#准备等待电话进来
	#conn就是客户端到服务器端，服务器端为其生成的一个实例
	while True:
		data=conn.recv(1024)
		if not data
			break
			res=os.popen(data.decode()).read()
		if len(res)==0:
			res="cmd has no output"
		conn.sendall(str(len(res)).encode("utf-8"))
		
		conn.recv("ok")#防止粘包
		
		conn.sendall(res.encode("utf-8"))
server.close()







#SocketServer

#server side
import socketserver
 
class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.
 
    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
 
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())
 
if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
 
    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
 
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()



 #client side
 import socket
import sys
 
HOST, PORT = "localhost", 9999
data = " ".join(sys.argv[1:])
 
# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(bytes(data + "\n", "utf-8"))
 
    # Receive data from the server and shut down
    received = str(sock.recv(1024), "utf-8")
finally:
    sock.close()
 
print("Sent:     {}".format(data))
print("Received: {}".format(received))


#上面这个例子你会发现，依然不能实现多并发，哈哈，在server端做一下更改就可以了

把	
server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
改成	
server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)


#paramiko
import paramiko
  
# 创建SSH对象
ssh = paramiko.SSHClient()
# 允许连接不在know_hosts文件中的主机
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 连接服务器
ssh.connect(hostname='c1.salt.com', port=22, username='wupeiqi', password='123')
  
# 执行命令
stdin, stdout, stderr = ssh.exec_command('df')
# 获取命令结果
result = stdout.read()
  
# 关闭连接
ssh.close()


#############################3
import paramiko

transport = paramiko.Transport(('hostname', 22))
transport.connect(username='wupeiqi', password='123')

ssh = paramiko.SSHClient()
ssh._transport = transport

stdin, stdout, stderr = ssh.exec_command('df')
print stdout.read()

transport.close()



基于公钥密钥连接：

import paramiko
 
private_key = paramiko.RSAKey.from_private_key_file('/home/auto/.ssh/id_rsa')
 
# 创建SSH对象
ssh = paramiko.SSHClient()
# 允许连接不在know_hosts文件中的主机
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 连接服务器
ssh.connect(hostname='c1.salt.com', port=22, username='wupeiqi', key=private_key)
 
# 执行命令
stdin, stdout, stderr = ssh.exec_command('df')
# 获取命令结果
result = stdout.read()
 
# 关闭连接
ssh.close()

##########################
import paramiko

private_key = paramiko.RSAKey.from_private_key_file('/home/auto/.ssh/id_rsa')

transport = paramiko.Transport(('hostname', 22))
transport.connect(username='wupeiqi', pkey=private_key)

ssh = paramiko.SSHClient()
ssh._transport = transport

stdin, stdout, stderr = ssh.exec_command('df')

transport.close()



#SFTPClient
import paramiko
 
transport = paramiko.Transport(('hostname',22))
transport.connect(username='wupeiqi',password='123')
 
sftp = paramiko.SFTPClient.from_transport(transport)
# 将location.py 上传至服务器 /tmp/test.py
sftp.put('/tmp/location.py', '/tmp/test.py')
# 将remove_path 下载到本地 local_path
sftp.get('remove_path', 'local_path')
 
transport.close()



##############################
#线程与进程  the
#线程是操作系统能够进行运算调度的最小单位。它被包含在进程之中，是进程中的实际运作单位。一条线程指的是进程中一个单一顺序的控制流，一个进程中可以并发多个线程，每条线程并行执行不同的任务


#程序并不能单独运行，只有将程序装载到内存中，系统为它分配资源才能运行，而这种执行的程序就称之为进程。程序和进程的区别就在于：程序是指令的集合，它是进程运行的静态描述文本；进程是程序的一次执行活动，属于动态概念。

#在多道编程中，我们允许多个程序同时加载到内存中，在操作系统的调度下，可以实现并发地执行。这是这样的设计，大大提高了CPU的利用率。进程的出现让每个用户感觉到自己独享CPU，因此，进程就是为了在CPU上实现多道编程而提出的


import threading

def run(n):
	print("hello",n)

for x in xrange(1,10):
	t=threading.Thread(target=run,args=("s%",x),)
	t.setDaemon(True)#设置为守护线程，在start之前
	t.start()
#等待thread运行使用join，如t.join()

threading.crrent_thread  #当前线程
threading.active_thread  #当前活跃的线程


#守护线程

#线程锁
lock=threading.lock()
#lock=threading.Rlock()递归锁
def run(n):
	lock.acquire()
	gloabal num
	num+=1
	lock.release()
#信号量
#semaphore=threading.BondeSemaphore(5)
#最多允许5个线程同时运行
#用法和锁一样

#Events
#通过Event来实现两个或多个线程间的交互，下面是一个红绿灯的例子，即起动一个线程做交通指挥灯，生成几个线程做车辆，车辆行驶按红灯停，绿灯行的规则。

import threading,time
import random
def light():
    if not event.isSet():
        event.set() #wait就不阻塞 #绿灯状态
    count = 0
    while True:
        if count < 10:
            print('\033[42;1m--green light on---\033[0m')
        elif count <13:
            print('\033[43;1m--yellow light on---\033[0m')
        elif count <20:
            if event.isSet():
                event.clear()
            print('\033[41;1m--red light on---\033[0m')
        else:
            count = 0
            event.set() #打开绿灯
        time.sleep(1)
        count +=1
def car(n):
    while 1:
        time.sleep(random.randrange(10))
        if  event.isSet(): #绿灯
            print("car [%s] is running.." % n)
        else:
            print("car [%s] is waiting for the red light.." %n)
if __name__ == '__main__':
    event = threading.Event()
    Light = threading.Thread(target=light)
    Light.start()
    for i in range(3):
        t = threading.Thread(target=car,args=(i,))
        t.start()


#队列 Queue

import queue
q=queue.Queue()
q.put("data")#放数据

q.get() #取数据

#进程

import multiprocessing

def run(name):
	print("hello",name)

p=multiprocessing.Process(target=run,args=("alex",))
p.start()

os.getppid 父进程id
os.getpid 进程id
#进程queue,实现不同进程之间的数据传递
import Queue
def f(q):
	q.put("s")

q=Queue()
p=Process(target=f,args=(q,))
p.start()

#管道pipes，两个进程之间数据传递

from multiprocessing import Process, Pipe
 
def f(conn):
    conn.send([42, None, 'hello'])
    conn.close()
 
if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(child_conn,))
    p.start()
    print(parent_conn.recv())   # prints "[42, None, 'hello']"
    p.join()


#Managers 两个进程之间的数据共享

from multiprocessing import Process, Manager
 
def f(d, l):
    d[1] = '1'
    d['2'] = 2
    d[0.25] = None
    l.append(1)
    print(l)
 
if __name__ == '__main__':
    with Manager() as manager:
        d = manager.dict()
 
        l = manager.list(range(5))
        p_list = []
        for i in range(10):
            p = Process(target=f, args=(d, l))
            p.start()
            p_list.append(p)
        for res in p_list:
            res.join()
 
        print(d)
        print(l)


#进程锁
from multiprocessing import Process, Lock
 
def f(l, i):
    l.acquire()
    try:
        print('hello world', i)
    finally:
        l.release()
 
if __name__ == '__main__':
    lock = Lock()
 
    for num in range(10):
        Process(target=f, args=(lock, num)).start()


#进程池

from  multiprocessing import Process,Pool
import time
 
def Foo(i):
    time.sleep(2)
    return i+100
 
def Bar(arg):
    print('-->exec done:',arg)
 
pool = Pool(5)
 
for i in range(10):
    pool.apply_async(func=Foo, args=(i,),callback=Bar)#并行
    #callback()在FOO执行完成后执行，每个进程FOO执行完都会执行Bar，callback是父进程发起
    #pool.apply(func=Foo, args=(i,))  串行
 
print('end')
pool.close()
pool.join()#进程池中进程执行完毕后再关闭，如果注释，那么程序直接关闭。

#协程
#使用yield实现协程
import time
import queue
def consumer(name):
    print("--->starting eating baozi...")
    while True:
        new_baozi = yield
        print("[%s] is eating baozi %s" % (name,new_baozi))
        #time.sleep(1)
 
def producer():
 
    r = con.__next__()
    r = con2.__next__()
    n = 0
    while n < 5:
        n +=1
        con.send(n)
        con2.send(n)
        print("\033[32;1m[producer]\033[0m is making baozi %s" %n )
 
 
if __name__ == '__main__':
    con = consumer("c1")
    con2 = consumer("c2")
    p = producer()
#greenlet,手动切换
from greenlet import greenlet
 
 
def test1():
    print(12)
    gr2.switch()
    print(34)
    gr2.switch()
 
 
def test2():
    print(56)
    gr1.switch()
    print(78)
 
 
gr1 = greenlet(test1)
gr2 = greenlet(test2)
gr1.switch()

#Gevent

import gevent
 
def func1():
    print('\033[31;1m李闯在跟海涛搞...\033[0m')
    gevent.sleep(2)
    print('\033[31;1m李闯又回去跟继续跟海涛搞...\033[0m')
 
def func2():
    print('\033[32;1m李闯切换到了跟海龙搞...\033[0m')
    gevent.sleep(1)
    print('\033[32;1m李闯搞完了海涛，回来继续跟海龙搞...\033[0m')
 
 
gevent.joinall([
    gevent.spawn(func1),
    gevent.spawn(func2),
    #gevent.spawn(func3),
])

#IO多路复用
#select 多并发socket 例子
#server端
import select
import socket
import sys
import queue


server = socket.socket()
server.setblocking(0)

server_addr = ('localhost',10000)

print('starting up on %s port %s' % server_addr)
server.bind(server_addr)

server.listen(5)


inputs = [server, ] #自己也要监测呀,因为server本身也是个fd
outputs = []

message_queues = {}

while True:
    print("waiting for next event...")

    readable, writeable, exeptional = select.select(inputs,outputs,inputs) #如果没有任何fd就绪,那程序就会一直阻塞在这里

    for s in readable: #每个s就是一个socket

        if s is server: #别忘记,上面我们server自己也当做一个fd放在了inputs列表里,传给了select,如果这个s是server,代表server这个fd就绪了,
            #就是有活动了, 什么情况下它才有活动? 当然 是有新连接进来的时候 呀
            #新连接进来了,接受这个连接
            conn, client_addr = s.accept()
            print("new connection from",client_addr)
            conn.setblocking(0)
            inputs.append(conn) #为了不阻塞整个程序,我们不会立刻在这里开始接收客户端发来的数据, 把它放到inputs里, 下一次loop时,这个新连接
            #就会被交给select去监听,如果这个连接的客户端发来了数据 ,那这个连接的fd在server端就会变成就续的,select就会把这个连接返回,返回到
            #readable 列表里,然后你就可以loop readable列表,取出这个连接,开始接收数据了, 下面就是这么干 的

            message_queues[conn] = queue.Queue() #接收到客户端的数据后,不立刻返回 ,暂存在队列里,以后发送

        else: #s不是server的话,那就只能是一个 与客户端建立的连接的fd了
            #客户端的数据过来了,在这接收
            data = s.recv(1024)
            if data:
                print("收到来自[%s]的数据:" % s.getpeername()[0], data)
                message_queues[s].put(data) #收到的数据先放到queue里,一会返回给客户端
                if s not  in outputs:
                    outputs.append(s) #为了不影响处理与其它客户端的连接 , 这里不立刻返回数据给客户端


            else:#如果收不到data代表什么呢? 代表客户端断开了呀
                print("客户端断开了",s)

                if s in outputs:
                    outputs.remove(s) #清理已断开的连接

                inputs.remove(s) #清理已断开的连接

                del message_queues[s] ##清理已断开的连接


    for s in writeable:
        try :
            next_msg = message_queues[s].get_nowait()

        except queue.Empty:
            print("client [%s]" %s.getpeername()[0], "queue is empty..")
            outputs.remove(s)

        else:
            print("sending msg to [%s]"%s.getpeername()[0], next_msg)
            s.send(next_msg.upper())


    for s in exeptional:
        print("handling exception for ",s.getpeername())
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()

        del message_queues[s]

#client端
import socket
import sys

messages = [ b'This is the message. ',
             b'It will be sent ',
             b'in parts.',
             ]
server_address = ('localhost', 10000)

# Create a TCP/IP socket
socks = [ socket.socket(socket.AF_INET, socket.SOCK_STREAM),
          socket.socket(socket.AF_INET, socket.SOCK_STREAM),
          ]

# Connect the socket to the port where the server is listening
print('connecting to %s port %s' % server_address)
for s in socks:
    s.connect(server_address)

for message in messages:

    # Send messages on both sockets
    for s in socks:
        print('%s: sending "%s"' % (s.getsockname(), message) )
        s.send(message)

    # Read responses on both sockets
    for s in socks:
        data = s.recv(1024)
        print( '%s: received "%s"' % (s.getsockname(), data) )
        if not data:
            print(sys.stderr, 'closing socket', s.getsockname() )


#selectors
import selectors
import socket
 
sel = selectors.DefaultSelector()
 
def accept(sock, mask):
    conn, addr = sock.accept()  # Should be ready
    print('accepted', conn, 'from', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)
 
def read(conn, mask):
    data = conn.recv(1000)  # Should be ready
    if data:
        print('echoing', repr(data), 'to', conn)
        conn.send(data)  # Hope it won't block
    else:
        print('closing', conn)
        sel.unregister(conn)
        conn.close()
 
sock = socket.socket()
sock.bind(('localhost', 10000))
sock.listen(100)
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)
 
while True:
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)







import select
import socket
import queue
server=socket.socket()
server.bind(('l0calhost',9000))
server.listen(1000)
server.setblocking(False) #
msg_dic={}
inputs=[server,]
outputs=[]
while True：
	readable,writeable,exceptional=select.select(inputs,outputs,inputs)
	for r in readable:
		if r is server:
			conn,addr=server.accept()#来新的连接
			inputs.append(conn)
			msg_dic[conn]=queue.Queue()
		else:
			data=r.recv(1024)
			msg_dic[r].put(data)

			outputs.append(r)
	for w in writeable:
		data_to_client=msg_dic[w].get()	
		w.sendall(data_to_client)

		outputs.remove(w)

	for e in exceptional:
		if e in outputs
			outputs.remove(e)

		inputs.remove(e)	


#消息队列Rabbit MQ
#Full code for send.py:
#The simplest thing that does something
#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()

#Full receive.py code:
#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()


*************************************************
#Distributing tasks among workers (the competing consumers pattern) 
#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
print(" [x] Sent %r" % message)
connection.close()



#!/usr/bin/env python
import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='task_queue')

channel.start_consuming()
********************************************************

#Sending messages to many consumers at once 


import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World!"
channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message)
print(" [x] Sent %r" % message)
connection.close()



#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs',
                   queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()

****************************************************************

#Receiving messages selectively 
#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs',
                         exchange_type='direct')

severity = sys.argv[1] if len(sys.argv) > 2 else 'info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'
channel.basic_publish(exchange='direct_logs',
                      routing_key=severity,
                      body=message)
print(" [x] Sent %r:%r" % (severity, message))
connection.close()



#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs',
                         exchange_type='direct')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

severities = sys.argv[1:]
if not severities:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)

for severity in severities:
    channel.queue_bind(exchange='direct_logs',
                       queue=queue_name,
                       routing_key=severity)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

#Receiving messages based on a pattern (topics) 
#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs',
                         exchange_type='topic')

routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'
channel.basic_publish(exchange='topic_logs',
                      routing_key=routing_key,
                      body=message)
print(" [x] Sent %r:%r" % (routing_key, message))
connection.close()



#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs',
                         exchange_type='topic')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(exchange='topic_logs',
                       queue=queue_name,
                       routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()

￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥

#Request/reply pattern example
#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def on_request(ch, method, props, body):
    n = int(body)

    print(" [.] fib(%s)" % n)
    response = fib(n)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

print(" [x] Awaiting RPC requests")
channel.start_consuming()


#!/usr/bin/env python
import pika
import uuid

class FibonacciRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)

fibonacci_rpc = FibonacciRpcClient()

print(" [x] Requesting fib(30)")
response = fibonacci_rpc.call(30)
print(" [.] Got %r" % response)



































































































































































