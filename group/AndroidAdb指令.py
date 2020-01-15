# 根据需要调整模块调入的函数
from ctypes import *
import subprocess as sub
import glob
import os
import aircv
import time

kernel32 = windll.kernel32
user32 = windll.User32
ws2_32 = windll.ws2_32

def getstr_left(cs_string, cs_findstr, cs_return=""):
    """
 取文本左边_正找：从左边开始寻找参数二
    :param cs_string: str;欲被取的文本
    :param cs_findstr: str;被索引的文本
    :param cs_return: str;失败后可以返回的文本，可空
    :return: str；参数一的右边文本（不包括参数一）
    """
    jb_site = str(cs_string).find(str(cs_findstr))
    if jb_site != -1 and str(cs_findstr) != '':
        return str(cs_string)[0:jb_site]
    return cs_return

def getstr_right_r(cs_string='', cs_findstr='', cs_return=""):
    """
取文本右边_倒找:从右边开始寻找参数二
    :param cs_string: str;欲被取的文本
    :param cs_findstr: str;被索引的文本
    :param cs_return: str;失败后可以返回的文本，可空
    :return: str;参数一的右边文本（不包括参数一）
    """
    jb_site = cs_string.rfind(cs_findstr)
    if jb_site != -1 and cs_findstr != '':
        return cs_string[jb_site + len(cs_findstr):]
    return cs_return

def getstr_centre(cs_string, cs_before, cs_after, cs_return=""):
    """
炫黑_取文本中间：从左边开始寻找参数二；基于参数二位置左边开始寻找参数三
    :param cs_string: str;欲被取的文本
    :param cs_before: str;被索引的前文本
    :param cs_after:  str;被索引的后文本
    :param cs_return: str;失败后可以返回的文本，可空
    :return: str;参数二和参数三的中间文本（不包括参数一，参数二）
    """
    jb_beforeSite = str(cs_string).find(cs_before)
    if jb_beforeSite != -1 and str(cs_before) != '':
        jb_afterSite = str(cs_string).find(str(cs_after), jb_beforeSite + 1)
        if jb_afterSite != -1 and str(cs_after) != '':
            return str(cs_string)[jb_beforeSite + len(str(cs_before)):jb_afterSite]
    return cs_return

def getstr_centre_r1(cs_string, cs_before, cs_after, cs_return=""):
    """
取文本中间_倒找1：从右边开始寻找参数二；基于参数二位置从左边开始寻找参数三
    :param cs_string: str;欲被取的文本
    :param cs_before: str;被索引的前文本
    :param cs_after: str;被索引的后文本
    :param cs_return: str;失败后可以返回的文本，可空
    :return: str;参数二和参数三的中间文本（不包括参数一，参数二）
    """
    jb_beforeSite = str(cs_string).rfind(str(cs_before))
    if jb_beforeSite != -1 and str(cs_before) != '':
        jb_afterSite = str(cs_string).find(str(cs_after), jb_beforeSite + 1)
        if jb_afterSite != -1 and str(cs_after) != '':
            return str(cs_string)[jb_beforeSite + len(str(cs_before)):jb_afterSite]
    return cs_return

def findPng(Dimg,Simg,con=0.1):
        Dimg = aircv.imread(Dimg)
        Simg = aircv.imread(Simg)
        result = aircv.find_template(Dimg,Simg,con)
        if result != None:
            return result['result']
        else:
            return (-1,-1)

def runDosStr(dosStr=''):
    return sub.getoutput(dosStr)

class AndroidAdb():
    def __init__(self,path=''):
        self.path=''
        for x in glob.glob(path+'\\*.exe'):
            if x.find('adb.exe') != -1:
                # print(sub.getstatusoutput(path + '\\adb version'))
                if sub.getstatusoutput(path + '\\adb version')[0] == 0 :
                    self.path = path+'\\'
                    break

    def getDevices(self):
        if self.path != '':
            # print(self.path)
            devices = runDosStr(self.path + 'adb devices')
            devicesList = devices.split('\n')
            resultDict = dict()
            for x in devicesList:
                if x.find('\t') != -1 :
                    resultDict[getstr_left(x,'\t')] = getstr_right_r(x,'\t')
            return resultDict

    def getEvent(self,device):
        if self.path!='':
            txt = runDosStr(self.path+'adb -s '+device+' shell getevent -p ')
            # print(txt)
            txtWide= getstr_centre(txt,'0035  :','resolution',0)
            txtWide = int(getstr_centre(txtWide,'max ',',',0)) - int(getstr_centre(txtWide,'min ',',',0))
            txtHigh = getstr_centre(txt,'0036  :','resolution',0)
            txtHigh = int(getstr_centre(txtHigh , 'max ', ',',0)) - int(getstr_centre(txtHigh , 'min ', ',',0))
            return [txtWide,txtHigh]

    def getPng(self,device,pngPath='',file=''):
        if pngPath == '':
            pngPath = os.path.abspath('.')
        if file == '':
            file = 'xhyk.png'
        print(runDosStr(self.path + 'adb -s %s shell /system/bin/screencap -p /sdcard/%s' % (device, file)))
        if sub.getstatusoutput(self.path + 'adb -s %s shell /system/bin/screencap -p /sdcard/%s'%(device,file))[0] ==0:
            if runDosStr('adb -s %s pull /sdcard/%s %s'%(device,file,pngPath)) != '':   # 把图片复制到电脑当前目录
                return '%s\\%s'%(pngPath,file)  # 这个文件名并不影响复制过来后的文件名
        else:
            return -1

    def click(self,device,x=0,y=0):
        return sub.getstatusoutput(self.path + "adb  -s  %s  shell input tap  %s  %s "%(device,x,y))[0]

    def clickMove(self,device,x1=0,y1=0,x2=0,y2=0):
        return sub.getstatusoutput(self.path + "adb  -s  %s  shell input swipe  %s  %s  %s  %s " % (device, x1, y1,x2,y2))[0]
         # adb shell input swipe <X1> <Y1> <X2> <Y2>

    def getApkPackageName(self,device):
        allpackage = runDosStr(self.path + 'adb -s %s shell pm list package -f '%device).split('\n')
        # print(sub.getstatusoutput('adb -s %s shell pm list package -f ' % device))
        result = dict()
        for package in allpackage:
            if package !='':
                result[getstr_right_r(package,'=')] = getstr_centre_r1(package,'/','=')
        return result

    def getDataPacket(self,device,path='',file=''):
        if path == '':
            path = os.path.abspath('.')
        if file == '':
            file = 'xhyk.png'
        runDosStr(self.path+"adb shell tcpdump -i eth0 -s 0 -w /data/eth0_test.pcap ")
        runDosStr(self.path + "adb pull data/eth0_test.pcap %s"%path)

if __name__ == '__main__':
    a = AndroidAdb(r'D:\ANZHUOMINIQI\Microvirt\MEmu')
    print(a.getDevices())
    device = '127.0.0.1:21503'
    # print(a.getEvent(device))
    print(a.getPng('127.0.0.1:21503','','1.png'))
    # print(a.click('127.0.0.1:21503',580,20))
    # print(a.clickMove('127.0.0.1:21503',30,120,310,310))
    # print(a.clickMove('127.0.0.1:21503',553.5,465.5,310,310))
    # print(a.getApkPackageName(device))
    # a.getDataPacket(device)
    x,y = findPng('1.png','2.png')
    print(x,y)
    # a.click(device,x,y)
    # print(a.clickMove('127.0.0.1:21503',62,243.5,310,310))
    # print(a.clickMove('127.0.0.1:21503',x,y,310,310))
    print(a.click('127.0.0.1:21503',x,y))
