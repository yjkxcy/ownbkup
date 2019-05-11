#coding:utf-8
import argparse
import os
import glob
import sys
import time
import shutil
import hashlib
try:
    import exifread
except ImportError:
    print("导入EXIFREAD模块错误，请运行pip install exifread安装，或访问https://pypi.org/project/ExifRead/获得帮助")
    exit()

if sys.version[0] == "3":
    raw_input = input
if sys.getdefaultencoding() != "utf-8":
    reload(sys)
    sys.setdefaultencoding("utf-8")




class BackupPath(object):
    def __init__(self, path):
        self.path = os.path.abspath(path)


    def copyFile(fileInfo):
        '''拷贝单个文件到备份目录下'''
        desFile = os.path.join(self.path, fileInfo.getSubDir(), fileInfo.getFileName().upper())
        index = 0  # 重命名时的参考编号
        while os.path.isfile(desFile):
            index += 1
            if fileInfo.getFileMd5() == getMd5(desFile):
                return False                           #文件已存在,没有进行复制步骤，返回False
            else:
                desFile = renamefile(desFile, index)   #文件大小不同，重新命名文件
        else:
            shutil.copy2(fileInfo.getFile(), desFile)
            return True                                #文件复制成功，返回True







def backupfile(srcfile, desdir):
    '''备份单个文件到指定的目录下'''
    despath = os.path.join(desdir, generatesubdir(srcfile))
    # print(despath)
    if not os.path.isdir(despath):
        os.mkdir(despath)
    filename = os.path.basename(srcfile).lower()
    #print(filename)
    desfile = os.path.join(despath, filename)
    # print(srcfile, desfile)
    index = 0  # 重命名时的参考编号
    while os.path.isfile(desfile):
        index += 1
        if comparefile(srcfile, desfile):
            print('{} is Exist, it is {}'.format(srcfile, desfile))
            # os.remove(srcfile)
            break
        else:
            desfile = renamefile(desfile, index)   #文件大小不同，重新命名文件
    else:
        shutil.copy2(srcfile, desfile)
        print('{} is backup OK, it is {}'.format(srcfile, desfile))







import os

def check_filename_available(filename):
    '''Python解决创建新文件时避免覆盖已有的同名文件问题'''
    n=[0]
    def check_meta(file_name):
        file_name_new=file_name
        if os.path.isfile(file_name):
            file_name_new=file_name[:file_name.rfind('.')]+'_'+str(n[0])+file_name[file_name.rfind('.'):]
            n[0]+=1
        if os.path.isfile(file_name_new):
            file_name_new=check_meta(file_name)
        return file_name_new
    return_name=check_meta(filename)
    return return_name
with open(check_filename_available('t.txt'),'w') as f:
    f.write('Checking func!')










    

        
