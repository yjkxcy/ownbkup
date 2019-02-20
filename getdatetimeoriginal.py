import exifread



def getdatetimeoriginal(file):
    with open(file, 'rb') as f:        # Open image file for reading (binary mode)
        tags = exifread.process_file(f, details=False, stop_tag='EXIF DateTimeOriginal')     # Return Exif tags
    return (tags['EXIF DateTimeOriginal'])

    #for tag in tags.keys():
        #if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
        #print("Key: %s, value %s" % (tag, tags[tag]))


if __name__ == '__main__':
    file = "D:\\ownbkup\\IMG_20171023_095825.jpg"
    date = getdatetimeoriginal(file)
    print(type(str(date)))