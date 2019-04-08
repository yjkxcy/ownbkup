#coding:utf-8
import argparse
import os
import sys
try:
    import exifread
except ImportError:
    print("导入EXIFREAD模块错误，请运行pip install exifread安装，或访问https://pypi.org/project/ExifRead/获得帮助")

if sys.version[0] == "3":
    raw_input = input
if sys.getdefaultencoding() != "utf-8":
    reload(sys)
    sys.setdefaultencoding("utf-8")
    
    

def askyesorno(info):   
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
        print("我将继续执行程序")
    else:
        print("我要退出了Bye-bye")
    
