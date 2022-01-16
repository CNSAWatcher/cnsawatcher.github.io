from PIL import Image
import os
def reshapeImg(directory, filename, thumbnail_dir, mywidth = 300, ):
    # try:
        img = Image.open(directory + '/' + filename)
        wpercent = (mywidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((mywidth,hsize), Image.ANTIALIAS)
        try:
            img.save(thumbnail_dir + '/' + filename)
        except:
            img = img.convert('RGB')
            img.save(thumbnail_dir + '/' + filename)
    # except:
    #     print('File transform error')

directory = '../images/zhurong/'
file_list = os.listdir(directory)
for ind, filename in enumerate(file_list):
    print(ind + 1, '/', len(file_list))
    if (os.path.isfile(directory + '/' + filename) and filename != '.DS_Store'):
        reshapeImg(directory, filename, directory + '/thumbnails/', mywidth = 300)
