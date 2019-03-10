import os
import exifread
import glob
import shutil
import time
import re
import platform


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


def getdatetimeoriginal(file):
    '''返回EXIF信息的拍摄日期，日期格式为time.struct_time'''
    with open(file, 'rb') as f:
        tags = exifread.process_file(f, details=False, stop_tag='EXIF DateTimeOriginal', strict=True)
    tmp = str(tags['EXIF DateTimeOriginal'])[:19]
    return time.strptime(tmp, '%Y:%m:%d %H:%M:%S')


def generatesubdir(file):
    '''根据EXIF信息或最后修改日期，生成子目录，如 “2019-02”'''
    try:
        date = getdatetimeoriginal(file)
    except KeyError:
        date = time.localtime(os.stat(file).st_mtime)
    return time.strftime('%Y-%m', date)


def getsubpaths(path):
    '''返回path目录下的所有子目录'''
    yield path
    stack = []
    stack.append(path)
    while len(stack) != 0:
        dirpath = stack.pop()
        try:
            filelist = os.listdir(dirpath)
        except PermissionError as err:
            print(err)
            continue
        else:
            for filename in filelist:
                fileabs = os.path.join(dirpath, filename)
                if os.path.isdir(fileabs):
                    stack.append(fileabs)
                    yield fileabs


def generatewildcard(extlist):
    '''根据扩展名生成glob所需的通配符，如‘*.[JjMm][PpOo][GgV4v]’'''
    allext = [s.lower() for s in extlist] + [s.upper() for s in extlist]
    wlist = [''.join(set(x)) for x in zip(*allext)]
    #print(wlist)
    return ("*." + "[{}]" * len(wlist)).format(*wlist)


def wildcards(exts):
    lenlist = [len(ext) for ext in exts]
    lenmin = min(lenlist)
    lenmax = max(lenlist) + 1
    extdict = {}
    for i in range(lenmin, lenmax):  # 扩展名长度2-4个字符
        extdict[i] = [ex for ex in exts if len(ex) == i]
    return [generatewildcard(extdict[key]) for key in extdict]


def backupfile(srcfile, desdir):
    '''备份单个文件到指定的目录下'''
    despath = os.path.join(desdir, generatesubdir(srcfile))
    # print(despath)
    if not os.path.isdir(despath):
        os.mkdir(despath)
    desfile = os.path.join(despath, os.path.basename(srcfile))
    # print(srcfile, desfile)
    index = 0  # 重命名时的参考编号
    while os.path.isfile(desfile):
        index += 1
        if comparefile(srcfile, desfile):
            print('{} is Exist, it is {}'.format(srcfile, desfile))
            # os.remove(srcfile)
            break
        else:
            desfile = renamefile(desfile, index)
    else:
        #shutil.copy2(srcfile, desfile)
        print('{} is backup OK, it is {}'.format(srcfile, desfile))


def bkuppath(srcpath, despath, fileextlist):
    '''备份源目录下指定扩展名的文件到目的目录下相应子目录内'''
    wildcardlist = wildcards(fileextlist)
    for wil in wildcardlist:
        for subdir in getsubpaths(srcpath):
            for srcfile in glob.glob(os.path.join(subdir, wil)):
                backupfile(srcfile, despath)


def generatewildcardt():
    extlist = ['jpg', 'MOV', 'mp4']  # ['rm']  #['jpeg', 'mpeg']
    print(generatewildcard(extlist))


def wildcardst():
    exts = input('请输入需要增加的文件扩展名（以空格分隔）:')
    t = []
    t.extend(exts.split())
    print(t)
    print(wildcards(t))


def renamefiletest():
    files = [('d:\\yjk\\owntest.jpg', 1), ('d:\\yjk\\owntest_1.jpg', 2), ('d:\\yjk\\owntest_2.jpg', 3),
             ('d:\\yjk\\owntest_3.jpg', 5)]
    for file, index in files:
        print('old ', file)
        try:
            print('new ', renamefile(file, index))
        except Exception as err:
            print(err)


def getsubpathst():
    srcpath = "C:\\"  # 201811newidea
    for p in getsubpaths(srcpath):
        print(p)


def generatesubdirt():
    path = "D:\\20170706apple6"
    for dir in getsubpaths(path):
        for file in glob.glob(os.path.join(dir, '*.mov')):
            print(generatesubdir(file))


def backupfilet():
    despath = "D:\\backup\\tb"
    path = "D:\\backup\photos\\2016-02"
    for dir in getsubpaths(path):
        for file in glob.glob(os.path.join(dir, '*.txt')):
            backupfile(file, despath)


def mainforwin():
    srcpath = os.getcwd()
    despath = os.path.join(os.path.abspath(os.path.dirname(srcpath)), 'backup\photos')
    fileextlist = ['jpg', 'jpeg', 'mov', 'mp4']
    msg = ('请输入需要增加的文件扩展名（以空格分隔，默认' + ' {} '* len(fileextlist) + ')').format(*fileextlist)
    strtmp = input(msg)
    fileextlist.extend(strtmp.split())
    #print(fileextlist)
    print('srcpath = {}, despath = {}, fileextlist = {}'.format(srcpath, despath, fileextlist))
    input('按回车健继续...')
    if not os.path.isdir(despath):
        os.mkdir(despath)
    bkuppath(srcpath, despath, fileextlist)


if __name__ == '__main__':
    systemver = platform.system()
    print(systemver)
    pythonver = platform.python_version()
    print(pythonver)
    if systemver == 'Windows':
        print('it is windows')
        mainforwin()
    elif systemver == 'Linux':
        print('it is linux')
    else:
        print('不支持当前系统，windows下需python3，linux下需python2.7')