from PIL import Image
import os
from shutil import copyfile

# print('begin')
directory = '../images/zhurong/'
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
            foo.save(directory + '/compressed/' + filename[:dotPos] + '.jpeg', optimize=True, quality=70)
        except:
            copyfile(directory + filename, directory + '/compressed/' + filename)