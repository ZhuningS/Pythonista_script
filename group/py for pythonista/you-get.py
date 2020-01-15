#!/usr/bin/env python3
from __future__ import unicode_literals
from ctypes import c_void_p, c_char_p, cdll, util
import re, appex, console, os
import clipboard
import sys
from you_get import common as you_get
# Load Objective-C runtime:
objc = cdll.LoadLibrary(util.find_library('objc'))
objc.sel_getName.restype = c_char_p
objc.sel_getName.argtypes = [c_void_p]
objc.sel_registerName.restype = c_void_p
objc.sel_registerName.argtypes = [c_char_p]
objc.objc_getClass.argtypes = [c_char_p]
objc.objc_getClass.restype = c_void_p

def msg(obj, restype, sel, argtypes=None, *args):
	if argtypes is None:
		argtypes = []
	objc.objc_msgSend.argtypes =  [c_void_p, c_void_p] + argtypes
	objc.objc_msgSend.restype = restype
	res = objc.objc_msgSend(obj, objc.sel_registerName(sel), *args)
	return res
	
def nsstr(s):
	return msg(objc.objc_getClass('NSString'), c_void_p, 'stringWithUTF8String:', [c_char_p], s)
	
def save_video(video_file):
	uikit = cdll.LoadLibrary(util.find_library('UIKit'))
	save_func = uikit.UISaveVideoAtPathToSavedPhotosAlbum
	save_func.argtypes = [c_void_p] * 4
	save_func(nsstr(video_file), None, None, None)

def my_hook(d):
	if d['status'] == 'finished':
		console.hide_output()
		chosen = console.alert('Download Finished', "Video is already in Pythonista.\nWaht else do you want to do with it?", 'Quick Look', 'Open in', 'Save to Album')
		if chosen == 1:
			console.quicklook(d['filename'])
		elif chosen == 2:
			console.open_in(d['filename'])
		elif chosen == 3:
			save_video(d['filename'].encode('utf-8'))
			
if appex.is_running_extension() and re.search('https*:\/\/[^\s]+', appex.get_attachments()[0]) is not None:
	url = appex.get_attachments()[0]
else:
	clip = re.search('https*:\/\/[^\s]+', clipboard.get())
	if clip is None:
		url = console.input_alert('URL Input')
	else:
		url = clipboard.get()

console.clear()

config = input('input config: ')
sys.argv=['you-get','%s'%config,'%s'%url]
you_get.main()
