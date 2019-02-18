import os
import exifread
import glob
import shutil
import time
import re


def comparefile(file1, file2):
    '''比较两个相同文件名的文件是否相同，根据文件最后修改日期和文件大小确定是否相同，返回True或Fales'''
    if os.stat(file1).st_mtime == os.stat(file2).st_mtime and os.stat(file1).st_size == os.stat(file2).st_size:
        return True
    else:
        return False


def renamefile(file, index):
    '''依照样式（filename_1.jpg）重命名文件，后缀为index'''
    path, filename = os.path.split(file)
    name, ext = os.path.splitext(filename)
    if index == 1:
        name = name + '_' + str(index)
    else:
        name = re.sub(r"_%s$" % (index - 1), "_%s" % index, name)
    newfilename = name + ext
    # print(newfilename)
    if newfilename == filename:
        raise Exception('file not rename')
    return os.path.join(path, newfilename)


def generatesubdir(file):
    '''根据EXIF信息或最后修改日期，生成子目录，如 “2019-02”'''
    pass


def getsubpaths(path):
    '''返回path目录下的所以子目录'''
    pass


class Wildcards(object):
    '''根据扩展名生成glob所需的通配符，如‘*.jpg’，返回通配符列表'''

    def __init__(self):
        self.exts = ['jpeg', 'jpg', 'mov', 'mp4']

    def appendext(self, newexts=[]):
        self.exts += newexts

    def getwildcards(self):
        return ['*.' + ext for ext in self.exts]



def backupfile(file, desdir):
    '''备份单个文件到指定的目录下'''
    pass


def bkuppath(surpath, despath):
    '''备份源目录下符合要求的文件到目的目录下相应子目录内'''
    pass


def wildcardst():
    w = Wildcards()
    w.appendext(['bmp', 'mpeg'])
    for e in w.getwildcards():
        print(e)



def renamefiletest():
    files = [('d:\\yjk\\owntest.jpg', 1), ('d:\\yjk\\owntest_1.jpg', 2), ('d:\\yjk\\owntest_2.jpg', 3),
             ('d:\\yjk\\owntest_3.jpg', 5)]
    for file, index in files:
        print('old ', file)
        try:
            print('new ', renamefile(file, index))
        except Exception as err:
            print(err)





if __name__ == '__main__':
    wildcardst()