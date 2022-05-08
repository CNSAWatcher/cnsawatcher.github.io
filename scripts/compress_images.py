from PIL import Image
import os
from shutil import copyfile

# print('begin')
def batch_compress(directory):
    # directory = '../images/space_tiangong/'
    print("processing: " + directory)
    file_list = os.listdir(directory)
    for ind, filename in enumerate(file_list):
        print(ind + 1, '/', len(file_list), filename)
        if (os.path.isfile(directory + '/' + filename) and filename != '.DS_Store'):

            if filename[-3:].lower() == 'gif': #test whether gif is animated or not
                gif = Image.open(directory + filename)
                try:
                    gif.seek(1)
                except EOFError:
                    #isanimated = False
                    pass
                else:
                    #isanimated = True
                    copyfile(directory + filename, directory + '/compressed/' + filename)
                    continue;

            try:
                foo = Image.open(directory + filename).convert('RGB')
                dotPos = filename.rfind('.')
                path_name = directory + '/compressed/' + filename[:dotPos] + '.jpeg'
                if os.path.exists(path_name):
                    print("    file exits, skipped")
                    continue
                foo.save(path_name, optimize=True, quality=70)
            except:
                path_name = directory + filename, directory + '/compressed/' + filename
                if os.path.exists(path_name):
                    print("    file exits, skipped")
                    continue
                copyfile(path_name)
                          
batch_compress('../images/space_tiangong/')
batch_compress('../images/zhurong/')
batch_compress('../images/yutu/')