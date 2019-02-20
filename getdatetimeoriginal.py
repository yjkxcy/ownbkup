import exifread
import time
import os


def getdatetimeoriginal(file):
    '''返回JPG文件EXIF信息中的拍摄日期，日期格式为time.struct_time'''
    with open(file, 'rb') as f:        # Open image file for reading (binary mode)
        tags = exifread.process_file(f, details=False, stop_tag='EXIF DateTimeOriginal')     # Return Exif tags
    tmp = str(tags['EXIF DateTimeOriginal'])[:19]
    return time.strptime(tmp, '%Y:%m:%d %H:%M:%S')

    #for tag in tags.keys():
        #if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
            #print("Key: %s, value %s" % (tag, tags[tag]))


if __name__ == '__main__':
    file = "D:\\ownbkup\\yjk.txt"   #IMG_20151019_170213.jpg"
    date = getdatetimeoriginal(file)
    print(type(date))
    print(date)
    print('\n')
    tmp = time.strftime('%Y-%m', date)
    print(type(tmp))
    print(tmp)
    print('\n')
    mdate = time.localtime(os.stat(file).st_mtime)
    print(type(mdate))
    print(mdate)