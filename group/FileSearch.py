#!python3
#coding:utf8
#@wind.m
import ui, dialogs, io
from os import *
from os.path import *
from console import quicklook, hud_alert, open_in
from editor import open_file
from shutil import move
from sound import play_effect
from threading import Thread
from time import time

#####显示设置#####
#启用文件信息(布尔值)
FILE_INFO_VIEW = True
#启用文件类型图标显示(布尔值)
FILE_ICON_VIEW = True
#忽略垃圾桶及库文件夹
FILTER_DIR = True

def make_index():
	global status, index_data
	status = '正在建立文件索引...'
	root_dir = expanduser('~/Documents')
	index_data = {}
	video_file = 'avi,wmv,mpeg,mp4,mov,mkv,flv,f4v,m4v,rmvb,rm,3gp,dat,ts,mts,vob,m3u8'
	audio_file = 'mp3,aac,wav,wma,cda,flav,m4a,mid,mka,mp2,mpa,mpc,ape,ogg,ra,wv,ac3,dts'
	image_file = 'jpg,bmp,gif,mif,miff,png,tif,tiff,svg,wmf,jpe,jpeg,pic,webp'
	text_file = 'txt,md,log,doc,csv,xls,ppt,docx,xlsx,pptx,wps,wpt,dot,rtf,dps,dpt,pot,pps,et,ett,xlt,json'
	script_file = 'py,js,html,htm,php,xml,sh'
	zip_file = 'bin,img,iso,mds,nrg,zip,rar,7z,jar,cab,tar,tar.gz,tar.tgz,gz,tgz'
	for root, dirs, files in walk(root_dir):
		for file in files:
			file_path = join(root,file)
			if FILTER_DIR and (expanduser('~/Documents/.Trash') in file_path or expanduser('~/Documents/site-packages') in file_path):
				continue
			file_size = getsize(file_path)
			if file_size <1000:
				size = '{}B'.format(file_size)
			elif file_size >= 1000 and file_size/1000 < 1000:
				size = '{:.1f}KB'.format(file_size/1000)
			else:
				size = '{:.1f}MB'.format(file_size/1000/1000)
			file_ext = splitext(file)[-1].strip('.').lower()
			if file_ext in script_file:
				icon =  'iob:code_32'
			elif  file_ext in image_file:
				icon = 'iob:ios7_camera_32'
			elif file_ext in video_file:
				icon = 'iob:social_youtube_32'
			elif file_ext in text_file:
				icon = 'iob:document_text_32'
			elif file_ext in audio_file:
				icon = 'iob:ios7_musical_notes_32'
			elif file_ext in zip_file:
				icon =  'iob:ios7_briefcase_32'
			else:
				icon = 'iob:social_apple_32'
			index_data[file_path] = {'size':size,'icon':icon}
	search()
	update_status()
	refresh_button.enabled = True
	rename_button.enabled = True

	
def search (keywords=''):
	global res_file
	res_file = [file for file in index_data.keys() if keywords.lower() in basename(file).lower()]
	res_file = sorted(res_file,reverse=True)
	return res_file


def clear_keywords (sender): 
	play_effect('ui:switch33')
	textfield.text = ''
	search()
	update_status()


def del_index (item):
	file_name = basename(item)
	name = splitext(file_name)[0]
	ext = splitext(file_name)[-1]
	trash = expanduser('~/Documents/.Trash')
	remove_path = join(trash,file_name)
	if not isdir(trash):
		mkdir(trash)
	num = 0
	while isfile(remove_path):
		num += 1
		new_file_name = '{}{}{}'.format(name,num,ext)
		remove_path = join(trash,new_file_name)
	move(item,remove_path)
	res_file.remove(item)
	del index_data[item]
	update_status()
	play_effect('rpg:BookFlip2')
	

def update_status():
	global status
	if textfield.text:
		status = '搜索到{}个符合条件的文件'.format(len(res_file))
		tableview.reload_data()
	else:
		status = '{}个文件'.format(len(index_data))
		tableview.reload_data()
		

def rename_file (sender):
	global res_file, status
	if '重名文件' in status:
		play_effect('digital:PhaserUp2')
		exit()
	name_list = [basename(file) for file in res_file]
	new_name_list = ['{}|||{}'.format(val,idx) for idx,val in enumerate(name_list)]
	new_name_list.sort(reverse=True)
	refile_list = []
	rename_list = []
	for name in new_name_list:
		val = name.split('|||')[0]
		idx = int(name.split('|||')[-1])
		if name_list.count(val)>1:
			refile_list.append(res_file[idx])
			rename_list.append(val)
	rename_count = len(set(rename_list))
	status = '当前列表有{}组重名文件'.format(rename_count)
	res_file = refile_list
	tableview.reload_data()


def share (sender):
	open_in(share_item)


def read_zip (item):
	global share_item
	share_item = item
	import zipfile
	zip = zipfile.ZipFile(item,'r').infolist()
	name = [basename(i.filename) for i in zip if i.file_size >0]
	size = [i.file_size for i in zip if i.file_size >0]
	size_format = []
	for i in size:
		if i < 1000:
			size_format.append('{}B'.format(i))
		elif i >1000 and i/1000 <1000:
			size_format.append('{:.2f}KB'.format(i/1000))
		else:
			size_format.append('{:.2f}MB'.format(i/1000/1000))
	info = ['{} | {}'.format(x,y) for x in name for y in size_format]
	title = '{} | {}个文件'.format(basename(item),len(name))
	view = ui.TableView()
	view.name = title
	view.data_source = ui.ListDataSource(info)
	button = ui.ButtonItem()
	button.image = ui.Image.named('iob:ios7_upload_outline_32')
	button.action = share
	view.right_button_items = [button]
	view.present()

	
def read_text (item):
	global  share_item
	share_item = item
	with io.open(item,'r',encoding='utf8') as file:
		content = file.read()
	
	view = ui.TextView()
	view.name = basename(item)
	view.text = content
	view.font = ('<System>',14)
	view.editable = False
	button = ui.ButtonItem()
	button.image = ui.Image.named('iob:ios7_upload_outline_32')
	button.action = share
	view.right_button_items = [button]
	view.present()

		
class TextfieldDelegate (object):
	
	def textfield_did_change(self,textfield):
		if textfield.text:
			play_effect('ui:switch3')
			search(textfield.text)
			update_status()
		else:
			clear_keywords(True)


class TableViewDataSource (object):
	
	def tableview_number_of_rows(self, tableview, section):
		return len(res_file)
	
	def tableview_title_for_header(self, tableview, section):
		return status
		
	def tableview_can_delete(self,tableview,section,row):
		return True
	
	def tableview_delete(self,tableview,section,row):
		item = res_file[row]
		del_index(item)
		tableview.reload_data()
			
	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell('subtitle')
		cell.border_width = 1
		cell.border_color = 'white'
		cell.text_label.text = basename(res_file[row])
		file_info = index_data[res_file[row]]
		if FILE_INFO_VIEW:
			file_detail = '【{}】 ~{}'.format(file_info['size'],res_file[row].replace(expanduser('~/Documents'),'').replace(basename(res_file[row]),''))
			cell.detail_text_label.text = file_detail
			cell.detail_text_label.text_color = '#008923'
			cell.alpha = 0.0
		if FILE_ICON_VIEW:
			cell.image_view.image = ui.Image.named(file_info['icon'])
		cell.accessory_type = 'detail_button'
		return cell
		

class TableviewDelegate (object):
	
	def tableview_did_select(self, tableview, section, row):
		item = res_file[row]
		play_effect('ui:switch1')
		open_file(item)
		v.close()
		
	def tableview_accessory_button_tapped(self, tableview, section, row):
		item = res_file[row]
		play_effect('ui:switch32')
		if index_data[item]['icon'] == 'iob:ios7_briefcase_32' and getsize(item)/1000/1000 < 10:
			read_zip(item)
		elif not quicklook(item) and getsize(item)/1000/1000 < 5:
			try:
				read_text(item)
			except:
				play_effect('digital:ZapThreeToneDown')
				hud_alert('不支持的文件类型','error',1),


if __name__ == '__main__':
	
	Thread(target=make_index).start()
	res_file = []
	
	w,h = ui.get_screen_size()
	v = ui.View()
	v.frame = (0,0,w,h)
	v.flex = 'WH'
	v.background_color = 'white'
	v.name = '文件搜索'

	imageview = ui.ImageView()
	imageview.frame = (4,3,37,37)
	imageview.image = ui.Image.named('iob:ios7_search_strong_32')
	v.add_subview(imageview)

	textfield = ui.TextField()
	textfield.placeholder = '搜索关键字...'
	textfield.frame = (45,3,200,37)
	textfield.delegate = TextfieldDelegate()
	v.add_subview(textfield)

	refresh_button = ui.Button()
	refresh_button.image = ui.Image.named('iob:ios7_refresh_32')
	refresh_button.tint_color = '#21dc57'
	refresh_button.frame = (250,3,37,37)
	refresh_button.action = clear_keywords
	refresh_button.enabled = False
	v.add_subview(refresh_button)
	
	rename_button = ui.Button()
	rename_button.title = '重名文件'
	rename_button.font = ('<System-Bold>',14)
	rename_button.tint_color = '#000000'
	rename_button.frame = (295,5,70,33)
	rename_button.bg_color = '#e6e6e6'
	rename_button.action = rename_file
	rename_button.enabled = False
	v.add_subview(rename_button)

	tableview = ui.TableView()
	tableview.frame = (0,48,w,h)
	tableview.flex = 'WH'
	tableview.allows_selection = True
	tableview.data_source = TableViewDataSource()
	tableview.delegate = TableviewDelegate()
	v.add_subview(tableview)

	v.present()
	
