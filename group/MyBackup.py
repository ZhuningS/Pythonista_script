#! python3
# coding: utf-8
'''
备份文件，并通过HTTP进行局域网分享

Modified By Nicked

https://t.me/nicked
'''

from http.server import SimpleHTTPRequestHandler, HTTPServer
import os, datetime, zipfile, console, sys, socket

PORT = 8080

# 被备份路径
p = '~/Documents'
backpath = os.path.expanduser(p)
# 备份文件存放路径
dstpath = os.path.expanduser('~/Documents/Downloads/Backup/')
# 垃圾桶路径
Trashpath = os.path.expanduser('~/Documents/.Trash')
# 排除垃圾箱文件
EXCLUDE_Trash = True

def get_ip_address():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('baidu.com', 80))
	ip_address = s.getsockname()[0]
	s.close()
	return ip_address

def backup(path = backpath, dst=dstpath):
	now = datetime.datetime.now()
	ymd = now.strftime('%Y-%m-%d')
	number = 1
	if not os.path.exists(dstpath):
		os.makedirs(dstpath)
	while True:
		basename = 'Backup' + ymd + '_' + str(number) + '.zip'
		zipFilename = os.path.join(dst + basename)
		if not os.path.exists(zipFilename):
			break
		number += 1
	a, b = 0, 0
	for f in os.listdir(path):
		if os.path.isdir(path+f):
			a += 1
		else:
			b += 1
	dispath = path.replace(os.path.expanduser('~'),'~')
	console.alert('备份{}'.format(dispath),'{}个文件夹和{}个文件,可能需要几秒钟'.format(a,b),'确定')
	backupzip = zipfile.ZipFile(zipFilename, 'w')
	n = 1
	for foldername, subfolders, filenames in os.walk(path):
		#console.hud_alert('备份第{}个文件夹'.format(n), '1')
		if Trashpath in foldername and EXCLUDE_Trash:
			continue
		#print('备份第{}个子文件夹:{}'.format(n,foldername.replace(os.path.expanduser('~'),'~'))+'\n')
		backupzip.write(foldername)
		n += 1
		for filename in filenames:
			if filename.startswith('Backup') and filename.endswith('.zip'):
				continue
			backupzip.write(os.path.join(foldername,filename))
	backupzip.close()
	console.hud_alert('备份完成！开始进行HTTP服务器部署...','3')
	
	os.chdir(dstpath)
	local_url = 'http://localhost:{}/{}'.format(PORT, os.path.basename(zipFilename))
	wifi_url = 'http://{}:{}/{}'.format(get_ip_address(), PORT, os.path.basename(zipFilename))
	server = HTTPServer(('', PORT), SimpleHTTPRequestHandler)
	console.clear()
	print('① 点击下面链接选择在Safari打开备份文件，再分享到其他App:')
	console.set_color(0,0,1)
	console.write_link(local_url + '\n', 'safari-' + local_url)
	console.set_color(1,1,1)
	print('\n② 如果想在局域网中其他设备访问该备份，请在其他设备中输入以下链接:')
	print(wifi_url)
	print('\n====\n完成分享后请在 console 中点停止.')
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		server.shutdown()
		server.socket.close()
		print('服务器终止')
	

if __name__ == '__main__':
	console.alert('当前备份路径', p, '确定')
	console.set_color(1,1,1)
	backup()
		
