#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @File    : ppcxydow4m3u8.py
# @Author  : loli
# @Date    : 2018-03-16
# @Version : v1.1
# @Contact : https://t.me/weep_x
# @tg group: https://t.me/pythonista3dalaoqun

'''
下载m3u8直链并合并文件，支持手动合并
后续将支持断点续传
'''

import os
import sys
import contextlib
import uuid
import urllib.request, urllib.error, urllib.parse
import shutil
import appex, clipboard, re, console

save_dir = os.path.expanduser('~/Documents/ppcxy_downloads/m3u8')
if not os.path.exists(save_dir):
    os.makedirs(save_dir)


def rm_file(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)
    elif os.path.exists(file_path):
        shutil.rmtree(file_path)


def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def download(target_file, url):
    try:
        with contextlib.closing(urllib.request.urlopen(url)) as rs:
            handle = open(target_file, 'wb')
            handle.write(rs.read())
            handle.close()
            redirect_url = rs.geturl()
            return redirect_url
    except:
        print('资源连接失败，请检查链接有效性。')

    return url


READ_SIZE = 1024


def join_file(base_path, target_file):
    output = open(target_file, 'wb')
    files = os.listdir(base_path)
    files.sort()
    for file_name in files:
        file_path = os.path.join(base_path, str(file_name))
        file_obj = open(file_path, 'rb')
        while 1:
            file_bytes = file_obj.read(READ_SIZE)
            if not file_bytes:
                break
            output.write(file_bytes)
        file_obj.close()
    output.close()


def download_m3u8(m3u8_url):
    current_m3u8 = str(uuid.uuid1());
    # 生成m3u8文件，采用uuid命名处理并发下载
    m3u8_file = '%s%s' % (current_m3u8, '.m3u8.tmp')
    logfile = '%s%s' % (current_m3u8, 'm3u8.log')
    rm_file(m3u8_file)
    print('正在解析m3u8资源: %s' % m3u8_url)
    redirect_next_url = download(m3u8_file, m3u8_url)

    if not os.path.exists(m3u8_file):
        return ''
    tem_ts_path = '%s%s' % (current_m3u8, 'ts')
    
    #http://vip.okokbo.com/ppvod/8A0910F51B58C20F3715BDD82C350942.m3u8
    sum_ts = len(open(m3u8_file,'rU').readlines())
    
    with open(m3u8_file) as source:
        ts_index = 1
        
        mkdir(tem_ts_path)

        with open(logfile, 'w') as log:
            for line in source:

                _ts_url = line.strip()
                if _ts_url and len(_ts_url) > 1 and not _ts_url.startswith('#'):
                    ts_name = ('%s%s%04d.ts' % (tem_ts_path, os.sep, ts_index))
                    log.write(ts_name)
                    log.write('\n')
                    ts_url = urllib.parse.urljoin(redirect_next_url, _ts_url)
                    print('开始下载啊ts %d / %d文件资源: %s' % (ts_index, sum_ts, _ts_url))
                    download(ts_name, ts_url)
                    ts_index += 1
                else:
                    log.write(line)


    print('下载完成，正在合并.........')
    join_file(tem_ts_path, current_m3u8+'.ts')
    print('合并完成,执行文件清理.........')
    rm_file(m3u8_file)
    rm_file(tem_ts_path)
    rm_file(logfile)
    new_file_name = console.input_alert('处理完毕，是否修改文件名？(不修改直接确定)：','',current_m3u8)
    if new_file_name != '':
        os.rename(current_m3u8+'.ts',os.path.join(save_dir,new_file_name+'.ts'))
    return new_file_name

def main():
    # 三种入口方式
    if appex.is_running_extension() and re.search('http*:\/\/[^\s]+', appex.get_attachments()[0]) is not None:
        url = appex.get_attachments()[0]
    else:
        clip = re.search('http*:\/\/[^\s]+', clipboard.get())

        if clip is None:
            url = console.input_alert('请输入m3u8资源地址：')
        else:
            url = clipboard.get()


    new_file_name=download_m3u8(url)
    if new_file_name != '':
        print('================================')
        print('下载完毕，存储为 this phone/ppcxy_download/m3u8目录\n文件名:')
        print(new_file_name+'.ts')
        print('请使用支持ts格式播放器播放')
        print('================================')

if __name__ == "__main__":
    if len(sys.argv) >=2 and sys.argv[1] != '':
        m3u8_file = '%s%s' % (sys.argv[1], '.m3u8.tmp')
        logfile = '%s%s' % (sys.argv[1], 'm3u8.log')
        tem_ts_path = '%s%s' % (sys.argv[1], 'ts')
        print('手动合并，正在合并.........')
        join_file(tem_ts_path, sys.argv[1]+'.ts')
        print('合并完成,执行文件清理.........')
        rm_file(m3u8_file)
        rm_file(tem_ts_path)
        rm_file(logfile)
        new_file_name = console.input_alert('处理完毕，是否修改文件名？(不修改直接确定)：','',sys.argv[1])
        if new_file_name != '':
            os.rename(sys.argv[1]+'.ts',new_file_name+'.ts')
    else:
        main()

