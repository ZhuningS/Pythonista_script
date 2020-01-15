# 2018-10-18 更新		by Final Fantasy
# 支持解析导入har文件并下载第一个请求
# 下载的文件保存在脚本所在文件夹的video文件夹内

import os
import appex, dialogs

def Downloader(url,outDir,filename=None,headers=None,stream=True):	# 文件下载 stream=True 不立即下载文件到内存，防止文件过大，内存不足
	import requests,os
	retry=0
	while True:
		if retry!=3:
			res=requests.get(url,headers=headers,stream=stream)
			filesize=int(res.headers['Content-Length'])
			if not filename and 'Content-Disposition' in res.headers:
				import re
				#input(res.headers['Content-Disposition'])
				m_filename=re.findall('(?<=filename=")[^"]+',res.headers['Content-Disposition'])
				if m_filename:
					filename=m_filename[0]
				else:
					filename='file'
			outfile_path=os.path.join(outDir,filename)
				#Content-Disposition: attachment; filename="635924308942-blobs-all.zip"
			if res.status_code==200:
				with open(outfile_path,'wb') as f_out:
					print(url)
					#print('正在下载...',end='')
					for chunk in res.iter_content(chunk_size=512):	# 一块一块的下载内容
						if chunk:
							f_out.write(chunk)
					
					try:
						print('\t',outfile_path)
					except UnicodeEncodeError:
						print('\t特殊字符无法显示！')
					f_out.close()
				if(os.path.getsize(outfile_path)==filesize):
					print('\t下载完成。')
					return outfile_path
				else:
					retry+=1
					print('\t文件大小错误，开始第 %s 次重试。' % retry)
			else:
				print('\t错误：%s' % res.status_code)
				print('\t开始第 %s 次重试。' % retry)
		else:
			print('\t下载失败！')
			return False

save_dir='./video'
if not os.path.exists(save_dir):
	os.makedirs(save_dir)

url=''
headers={}
if not appex.is_running_extension():
	import clipboard	
	url=dialogs.input_alert('请输入链接地址：')

else:
	filepath=appex.get_attachments()[0]
	
	if '.har'==filepath[-4:]:
		import json
		with open(filepath,'r') as f:
		#f=open(filepath,'r')
			#print('test')
			r=json.loads(f.readline())['log']['entries'][0]['request']
			#print(r)
			f.close()
			url=r['url']
			
			for h in r['headers']:
				if not h['name'] in ['Content-Length','Connection','Host','Content-Type','If-Modified-Since','Range','Connection']:
					headers[h['name']]=h['value']
	elif 'http'==filepath[:4]:
		url=filepath
			
	
#url=input('\n请输入url:')
if url!='':
	name=dialogs.input_alert('保存文件名 :')

	ext=url.split('?')[0].split('.')[-1]
	fn=name+'.'+ext
	Downloader(url,save_dir,fn,headers)
		
		
else:
	print('url为空')
