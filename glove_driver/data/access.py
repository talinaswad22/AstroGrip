"""
Tasks:
- method for creating a file and it's meta file
"""
from pathlib import Path
from yaml import dump
from time import strftime, gmtime
from cv2 import imwrite
from uuid import uuid4
import csv

# TODO add error checking for functions
#########################################################
# data control layer
#########################################################

_SESSION_ID = None
_SUBDIR = "sensor_data"

def initialize_session(directories, metadata_dirs):
    global _SESSION_ID
    # Session ID is only for csv data, which is attributed to a singular session
    _SESSION_ID = str(uuid4())
    # directories
    #TODO implement directory check
    create_directories(directories)
    #TODO implement creation of metadata
    create_metadata(metadata_dirs)

# I wrote this so that I would have an abstraction from accessing files
# though not realy good, it is not called that often
def create_access_path(dir, uuid,filetype):
    return rf"./{_SUBDIR}/{dir}/{uuid}.{filetype}"

def path_existence_check(potential_path):
    path = Path(potential_path)
    if not path.exists():
        try:
            path.mkdir(parents=True)
        except FileExistsError as e:
            raise e

def create_directories(dirs):
    for dir in dirs:
        try:
            path_existence_check(rf"./{_SUBDIR}/{dir}/")
        except FileExistsError:
            pass

def create_metadata(dirs):
    for dir in dirs:
        _create_metadata(rf"./{_SUBDIR}/{dir}",_SESSION_ID)

def write_data2csv(data,path):
    # path is a directory name
    _write_data2csv(iter(data),rf"./{_SUBDIR}/{path}",_SESSION_ID)
    return _SESSION_ID

def write_data2image(image,path):
    id = str(uuid4())
    _write_data2image(image,rf"./{_SUBDIR}/{path}",id)
    return id


#########################################################
# data layer
#########################################################

def _create_metadata(path,uuid):
    with open(rf"{path}/{uuid}.yaml",'w') as file:
        dump({"uuid":uuid,"time":strftime("%d %b %Y %H:%M:%S", gmtime())},file)

def _write_data2csv(data_it, path,uuid):
    # check if path exists
    path_existence_check(path)
    # create csv 
    with open(rf"{path}/{uuid}.csv",'a') as file:
        csvfile = csv.writer(file,delimiter=',')
        csvfile.writerows(data_it)
    
    

def _write_data2image(image,path,uuid,):
    # check if path exists
    path_existence_check(path)
    # create meta file
    _create_metadata(path,uuid)
    # save image
    imwrite(rf"{path}/{uuid}.jpg",image)