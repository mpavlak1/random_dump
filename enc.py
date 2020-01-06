# Built-ins
import os
import hashlib
from datetime import datetime

# Package
import __init__

# Additional
from cryptography.fernet import Fernet

KEYDIR  = './keys'
ENTRIES = './entries'

os.makedirs(KEYDIR, exist_ok=True)
os.makedirs(ENTRIES, exist_ok=True)

def new_key(): return Fernet.generate_key()

def write_key(key, keypath):
    with open(keypath, mode='wb') as w:
        w.write(key)

def read_key(keypath):
    with open(keypath, mode='rb') as r:
        return r.read()

def encrypt_file(filepath, key, outpath = None, remove=True):

    if(not outpath): outpath = filepath
   
    with open(filepath, mode='rb') as r:
        data = r.read()

    cipher = Fernet(key)
    with open(outpath, mode='wb') as w:
        w.write(cipher.encrypt(data))
        del data

    if(remove or filepath != outpath):
        os.remove(filepath)

def decrypt_file(filepath, key, outpath = None):

    if(not outpath):
        outpath = filepath

    with open(filepath, mode='rb') as r:
        data = r.read()

    cipher = Fernet(key)
    with open(outpath, mode='wb') as w:
        w.write(cipher.decrypt(data))

def today():
    return (lambda x: '{}{}{}'.format(str(x.month).zfill(2),
                                      str(x.day).zfill(2),
                                      x.year))(datetime.now())

def new_entry(daystr = today()):
    keyfile = os.path.join(KEYDIR, '{}.key'.format(daystr))
    f_ = os.path.join(ENTRIES, '{}.txt'.format(daystr))

    if(not os.path.exists(f_)):
        with open(f_, mode='w'): pass
    write_key(new_key(), keyfile)

def lock():
    for file in os.listdir(ENTRIES):
        file = os.path.join(ENTRIES, file)
        if(os.path.splitext(file)[-1] != '.enc'):
            b_ = os.path.splitext(os.path.basename(file))[0]
            efile = os.path.join(ENTRIES, '{}.enc'.format(b_))
            encrypt_file(file,
                         read_key(os.path.join(KEYDIR, '{}.key'.format(b_))),
                         outpath=efile, remove=True)
    
def unlock(daystr = today()):
    efile = os.path.join(ENTRIES, '{}.enc'.format(daystr))
    keyfile = os.path.join(KEYDIR, '{}.key'.format(daystr))
    outfile = os.path.join(ENTRIES, '{}.txt'.format(daystr))

    if(os.path.exists(efile)):
        decrypt_file(efile, read_key(keyfile), outpath=outfile)  

