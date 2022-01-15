import os
import re
import json

from deep_translator import GoogleTranslator
print(GoogleTranslator('auto','en').translate('祝融号火星车!'))

filenameToSave = './yutu_gallery_preModify.json'
directory_rel = '/images/yutu/'
directory = '../images/yutu/'
file_list = os.listdir(directory)
file_compressed_list = os.listdir(directory + 'compressed')

data = []

for ind, filename in enumerate(file_list):
    print(ind + 1, '/', len(file_list))
    if os.path.isfile(directory  + filename) and filename != '.DS_Store':
        date, title = filename.split('-')
        title_zh = title.split('.')[0]
        title = GoogleTranslator('auto','en').translate(title_zh)
        if filename in file_compressed_list: #this comes from compress_images.py, which changes images to .jpeg files or leave animated gif unchanged
            filename_compressed = filename
        else: #this comes from compress_images.py, which changes images to .jpeg files or leave animated gif unchanged
            dotPos = filename.rfind('.')
            filename_compressed = filename[:dotPos] + '.jpeg'
        data.append({'date': date,
                     'title': title,
                     'href': directory_rel + filename,
                     'href_avatar': directory_rel + 'thumbnails/' + filename,
                     'href_compressed': directory_rel + 'compressed/' + filename_compressed,
                     })

data.sort(key = lambda x: x['date'], reverse = True)
with open(filenameToSave, 'w') as f:
    json.dump(data , f, ensure_ascii=False)

# with codecs.open(outputfile, 'w', encoding='utf-8') as f:
#     json.dump(datafile, f, ensure_ascii=False)
