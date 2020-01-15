import appex, console, shutil
from os import path

# 文件保存路径
save_dir = path.expanduser('~/Documents')

def simple_import():

	if appex.is_running_extension():
		get_path = appex.get_file_path()
		file_name = path.basename(get_path)
		dstpath = path.join(save_dir, file_name)
		file_pure_name = path.splitext(file_name)[0]
		file_ext = path.splitext(file_name)[-1]
		if file_ext == '.py':
			new_file_name = ''
			number = 1
			while(path.exists(dstpath)):
				new_file_name = file_pure_name + str(number) + file_ext
				dstpath = path.join(save_dir, new_file_name)
				number += 1
			if new_file_name:
				try:
					while True:
						newname = console.input_alert('文件名已存在', '重命名如下？',new_file_name,'确认', hide_cancel_button=False)
						if not path.exists(path.join(save_dir, newname)):
							break
				except:
					exit()
			else:
				try:
					newname = console.input_alert('确认', '文件名',file_name,'确认', hide_cancel_button=False)
				except:
					exit()
			dstpath = path.join(save_dir, newname)
			try:
				shutil.copy(get_path, dstpath)
				console.hud_alert('导入成功！','',1)
			except Exception as eer:
				print(eer)
				console.hud_alert('导入失败！','error',1)
		else:
			console.hud_alert('非py文件无法导入', 'error', 2)
	else:
		console.hud_alert('请在分享扩展中打开本脚本','error',2)

if __name__ == '__main__':
	simple_import()
