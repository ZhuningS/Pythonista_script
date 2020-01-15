import paramiko

hostname = '172.16.1.200'   #linux主机IP地址
port = 22   #端口

username = ''   #用户名
password = ''    #密码

localdeb = r'foreca.py' #Windows下文件路径（需复制的文件）

debpath = '/home/pi/' #Linux目录
debname = 'foreca.py' #软件包完整名称

#连接Linux
transport=paramiko.Transport((hostname,port))
transport.connect(username=username, password=password)

#将本地文件传至Linux中
sftp = paramiko.SFTPClient.from_transport(transport)
sftp.put(localdeb, debpath + debname)

client= paramiko.SSHClient()
client._transport=transport

#列出Linux目录中的文件，以便检查是否传送成功
print('上传完成！' + debpath +' 下有如下文件：')
lscmd = 'ls -l ' + debpath;
stdin, stdout, stderr = client.exec_command(lscmd)
print(stdout.read().decode('utf-8'))
