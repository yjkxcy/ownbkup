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

latestmd5 = set()



def generatewildcard(extlist):
    '''根据扩展名列表生成glob所需的通配符，如‘*.[JjMm][PpOo][GgV4v]’'''
    allext = [s.lower() for s in extlist] + [s.upper() for s in extlist]
    wlist = [''.join(set(x)) for x in zip(*allext)]
    #print(wlist)
    return ("*." + "[{}]" * len(wlist)).format(*wlist)


def wildcards(exts):
    '''根据不同长度的扩展名，生成相应规则的通配符，返回通配符的列表'''
    lenlist = [len(ext) for ext in exts]
    lenmin = min(lenlist)
    lenmax = max(lenlist) + 1
    extdict = {}
    for i in range(lenmin, lenmax):  # 扩展名长度2-4个字符
        extdict[i] = [ext for ext in exts if len(ext) == i]
    return [generatewildcard(extdict[key]) for key in extdict]


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



def getfilemd5(filename):
    '''生成文件的MD5码'''
    def read_chunks(fh):
        fh.seek(0)
        chunk = fh.read(8096)
        while chunk:
            yield chunk
            chunk = fh.read(8096)
        else:
            fh.seek(0)
    m = hashlib.md5()
    with open(filename, 'rb') as fh:
        for chunk in read_chunks(fh):
            m.update(chunk)
    return m.hexdigest()


def md5compare(srcfile, desfile):
    '''通过建立一个存储最近生成的MD5码的集合，快速判断文件是否存在'''
    global latestmd5
    srcfilemd5 = getfilemd5(srcfile)
    if srcfilemd5 in latestmd5:
        return True
    else:
        desfilemd5 = getfilemd5(desfile)
        latestmd5.add(desfilemd5)
        if srcfilemd5 == desfilemd5:
            return True
        else:
            return False
        


def comparefile(srcfile, desfile):
    '''比较两个相同文件名的文件是否相同，根据文件大小、MD5确定是否相同，返回True或Fales'''
    if os.stat(srcfile).st_size == os.stat(desfile).st_size and md5compare(srcfile, desfile):
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


def askyesorno(info):
    '''判断用户输入的是 'Y'还是 'N'   '''
    answer =  raw_input(info).lower()
    while answer not in ["yes", "y", "no", "n"]:
        answer =  raw_input(info).lower()
    else:
        if answer in ["yes", "y"]:
            return(True)
        else:
            return(False)

if __name__ == '__main__':
    helps = {
        "description":"一个备份工具，主要用于对日常拍摄的照片按照拍摄日期或最后修改日期整理到对应的目录中",
        "srcpath":"需备份的目录,默认为当前目录",
        "bkuppath":"备份到的目录，默认为当前目录的父目录下的backup下",
        "exts":"需要备份的文件扩展名列表，如：jpg, mov等，默认['jpg', 'jpeg']"
        }
    srcdir = os.getcwd()
    bkupdir =  os.path.join(os.path.dirname(srcdir), 'backup')
    jpgfile = ["jpg", "jpeg"]
    parser =  argparse.ArgumentParser(description = helps["description"])
    parser.add_argument("--src", dest="srcpath", default=srcdir, help=helps["srcpath"])
    parser.add_argument("--bkup", dest="bkuppath", default=bkupdir, help=helps["bkuppath"])
    parser.add_argument("--ext", dest="exts", nargs="+", default=jpgfile, help=helps["exts"])
    args = parser.parse_args()
    if not (os.path.isdir(args.srcpath) and os.path.isdir(args.bkuppath)):
        print("目录不存在，程序中止运行")
        sys.exit()
    print("备份的源目录和目标目录为：srcpath = {}, bkuppath = {} ".format(args.srcpath, args.bkuppath))
    print("你准备备份的文件类型有：" + ("{} " * len(args.exts)).format(*args.exts))
    if askyesorno("请输入（Y/N）确认或退出："):
        wildcardlist = wildcards(args.exts)
        for wildcard in wildcardlist:
            for subdir in getsubpaths(args.srcpath):
                for srcfile in glob.glob(os.path.join(subdir, wildcard)):
                    backupfile(srcfile, args.bkuppath)
        #print(wildcardlist)
        print("备份完成")
    else:
        print("我要退出了Bye-bye")
    
