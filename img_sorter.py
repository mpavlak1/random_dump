# Built-ins
import os
import hashlib
from datetime import datetime
from shutil import copyfile

# Package
import __init__

# Additional Packages
from PIL import Image
from PIL import ExifTags
import dill as pickle

DATETAKENKEY = 'DateTimeOriginal'

def get_hash(img):
    return hashlib.sha1(img.tobytes()).hexdigest()

def read_meta(img):
    return {ExifTags.TAGS[k] : v for k,v in img._getexif().items() if k in ExifTags.TAGS}

def read_date(meta):
    if(DATETAKENKEY not in meta):
        return False

    date_str = meta[DATETAKENKEY]
    return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')

def date_to_path(outpath, date):
    return os.path.join(outpath,
                        str(date.year),
                        '{} - {}'.format(str(date.month).zfill(2),
                                         date_to_path.months[date.month]),
                        str(date.day).zfill(2))
date_to_path.months = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun',
                       7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}

def all_files(path, ftypes=['.jpg','.jpeg']):
    for r, d, f in os.walk(path):
        for file in f:
            if(os.path.splitext(file)[1].lower() in ftypes):
                yield os.path.join(r, file)

def organize_by_date(inpath, outpath, hashes_file=None, ftypes = ['.jpg', '.jpeg']):

    files = list(all_files(inpath, ftypes=ftypes))
    dupl_count,unso_count,copy_count  = 0,0,0

    if(not hashes_file):
        hashes_file = os.path.join(outpath, 'hashes.pickle')

    if(os.path.exists(hashes_file)):
        with open(hashes_file, mode='rb') as r:
            hashes = pickle.load(r)
    else: hashes = set()
    
    for i, file in enumerate(files):

        if(i % 100 == 0 and i>0):
            print('{} of {}, ({}%)'.format(i, len(files), 100* (i/len(files))))

        _img = Image.open(file)
        _hash = get_hash(_img)
        if(_hash in hashes):
            dupl_count+=1
            continue
        else: hashes.add(_hash)

        _meta = read_meta(_img)

        date = read_date(_meta)

        if(date):
            copy_count += 1
            outdir = date_to_path(outpath, date)
        else:
            unso_count += 1
            os.path.join(outpath, 'Unsorted')

        os.makedirs(outdir, exist_ok=True)

        filename = os.path.join(outdir, os.path.basename(file))
        _fname = filename
        dup_count = 0
        while(os.path.exists(filename)):
            _p = list(os.path.splitext(os.path.basename(_fname)))
            _p.insert(1,str(dup_count).zfill(3))
            filename = os.path.join(outdir, ''.join(_p))
            dup_count+=1
        #print(filename)
        copyfile(file, filename)

    with open(hashes_file, mode='wb') as w:
        pickle.dump(hashes, w)

    print('Duplicates :\t{}\t({}%)'.format(dupl_count, '{}'.format(100 * (dupl_count/len(files)))))
    print('Unsorted   :\t{}\t({}%)'.format(unso_count, '{}'.format(100 * (unso_count/len(files)))))
    print('Coppied    :\t{}\t({}%)'.format(copy_count, '{}'.format(100 * (copy_count/len(files)))))
    print('Total Count:\t{}'.format(len(files)))



infile = 'C:/Users/michael.pavlak/Desktop/'
outfile = 'C:/Users/michael.pavlak/Documents/test_qqq'

