"""
Tasks:
- method for creating a file and it's meta file
"""
from pathlib import path
from yaml import dump
from time import strftime, gmtime
from cv2 import imwrite
from uuid import uuid4

# TODO add error checking for functions
#########################################################
# data control layer
#########################################################

_SESSION_ID = None
def initialize_session():
    # Session ID is only for csv data, which is attributed to a singular session
    _SESSION_ID = str(uuid4())
    # directories

def path_existence_check(path):
    if not path.exists():
        try:
            path.mkdir()
        except FileExistsError as e:
            raise e

def create_directories(dirs):
    for dir in dirs():
        try:
            path_existence_check(dir)
        except FileExistsError:
            pass

def create_metadata(dirs):
    for dir in dirs():
        _create_metadata(dir,_SESSION_ID)

def write_data2csv(data,path):
    _write_data2csv(data,path,_SESSION_ID)
    return _SESSION_ID

def _write_data2image(image,path):
    id = str(uuid4())
    _write_data2image(image,path,id)
    return id


#########################################################
# data layer
#########################################################

def _create_metadata(path,uuid):
    with open(path / f"{uuid}.yaml",'w') as file:
        dump(file,{"uuid":uuid,"time":strftime("%d %b %Y %H:%M:%S", gmtime())})

def _write_data2csv(data_it, path,uuid):
    # check if path exists
    path_existence_check(path)
    
    # create csv 
    
    

def _write_data2image(image,path,uuid,):
    # check if path exists
    path_existence_check(path)
    # create csv 
    imwrite(path / f"{uuid}.jpg",image)