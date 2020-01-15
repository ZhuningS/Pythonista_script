#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @File    : ui_widget_setter.py
# @Author  : loli
# @Date    : 2018-03-15
# @Version : 1.0
# @Contact : https://t.me/weep_x
# @tg group: https://t.me/pythonista3dalaoqun

import common
import os
import shutil
import ui
import console
from utils import py_utils,file_picker
import css_color_selector,icon_selector

config  = py_utils.load_config(os.path.join(py_utils.load_base_dir(False),'config.json'))

def color_callback(color):
    scrv['color'].text=color

def icon_callback(icon):
    scrv['icon'].text=icon


def selecter(sender):
    w,h = ui.get_screen_size()
    
    if w >490:
        w=324
        h=260
    else:
        h=h-318
        w=w-23
    selecter_v = scrv['selecter_v']
    if sender.name=='btn_color':   
        f = (0, 0, w, h)
        mc = css_color_selector.ColorClass(name='颜色选择器', frame=f, bg_color='white',callback=color_callback)
    else:
        f = (0, 0, w, h)
        mc = icon_selector.IconClass(name='图标选择器', frame=f, bg_color='white',callback=icon_callback)
    #selecter.present('sheet', animated=False)
    selecter_v.add_subview(mc)

def tcc_action(sender):
    if sender.name=='tcquxiao':
        pass
    else:
        global py_files
        title = scrv['title'].text if scrv['title'] !='' else py_files.split('/')[-1]
        color = scrv['color'].text if scrv['color'].text != '' else '#4900ff'
        icon = scrv['icon'].text if scrv['icon'].text != '' else 'typb:Relocate'
        if scrv['icon_iob']==0:
            icon='iow:'+icon
        else:
            icon='iob:'+icon
        
        btn = {'title': title, 'id': py_files.split('/')[-1], 'oper': 'open_script', 'oper_param': '', 'color': color, 'icon': icon}
        btn['oper_param']=os.path.join('ex',py_files.split('/')[-1])
        
        tv.data_source.items.append(btn)
    scrv['title'].text=''
    scrv['color'].text=''
    scrv['icon'].text = ''
    scrv.alpha=0
    py_files=None
    
    

def edit(sender):
    tv.editing=not tv.editing

def save_config(sender):
    config['btn-h']=int(v['rh'].text)
    config['btn-c']=int(v['cc'].text)
    
    config['ibtns']=tv.data_source.items
    py_utils.save_config(config,os.path.join(py_utils.load_base_dir(False),'config.json'))
    console.alert('通知','保存配置成功.','确定',hide_cancel_button=True)
    v.close()


def add_local(sender):
    global py_files
    py_files = file_picker.file_picker_dialog('请选择文件', multiple=False, select_dirs=False, file_pattern=r'^.*\.py$')

    if py_files != None:
        scrv.alpha=1
        shutil.copyfile(py_files,os.path.join(py_utils.load_base_dir(False),'ex',py_files.split('/')[-1]))
        
        
        
        
py_files=None
    
v = ui.load_view()
tv = v['data_table']
scrv = v['scrv']
tv.data_source.items.clear()
tv.data_source.items.extend(config['ibtns'])
v['rh'].text = str(config['btn-h'])
v['cc'].text = str(config['btn-c'])

v.present('sheet')



