def comparefile(file1, file2):
    '''比较两个相同文件名的文件是否相同，根据文件最后修改日期和文件大小确定是否相同，返回True或Fales'''
    return True


def renamefile(file, index):
    '''依照样式（filename_1.jpg）重命名文件，后缀为index'''
    pass


def generatesubdir(file):
    '''根据EXIF信息或最后修改日期，生成子目录，如 “2019-02”'''
    pass


def getsubpaths(path):
    '''返回path目录下的所以子目录'''
    pass


class Wildcards(object):
    '''根据扩展名生成glob所需的通配符，如‘*.jpg’，返回通配符列表'''

    def __init__(self, exts=['jpg', 'jpeg', 'mov', 'mp4']):
        self.exts = exts

    def getwildcards(self):
        return ['*.' + ext for ext in self.exts]


def backupfile(file, desdir):
    '''备份单个文件到指定的目录下'''
    pass


def bkuppath(surpath, despath):
    '''备份源目录下符合要求的文件到目的目录下相应子目录内'''
    pass


if __name__ == '__main__':
    pass
