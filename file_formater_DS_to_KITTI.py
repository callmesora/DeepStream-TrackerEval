import pandas as pd
import csv
import os
import argparse
import logging
import json 
import numpy as np


# Level of warnings
logging.basicConfig(format='[%(levelname)s]: %(message)s', level=logging.NOTSET) 

#Parser
parser = argparse.ArgumentParser(description='DeepStream to KITTI file formater')
parser.add_argument('-file', type=str, required=True, help='path to folder contatining .txt label files outputed by DeepStream')
parser.add_argument('-images', type=str, required=True, help='path to image frames')


def formatToFullKitti(path, images):
    #Read specific columns from csv file
    col_list = ["frame_id","type","tracker_id", "truncated", "occluded", "alpha", "bbox1","bbox2","bbox3","bbox4", "dimensions1","dimensions2","dimensions3", "location1","location2","location3","rotation_y","score"]
    df_kitty_original = pd.read_csv(path, sep=' ', header=None, names=col_list)
    df_kitty = df_kitty_original[["frame_id","tracker_id","type", "truncated", "occluded", "alpha", "bbox1","bbox2","bbox3","bbox4", "dimensions1","dimensions2","dimensions3", "location1","location2","location3","rotation_y","score"]]

    
    #print(df_kitty.values)
    #np.savetxt(r'kitti-out-novo-.txt', df_kitty.values, )
    with open('formated-output-new.txt', 'a') as f:
        dfAsString = df_kitty.to_string(header=False, index=False)
        f.write(dfAsString)

    df_kitty.to_csv(r'KITTI-Culmulated-Formated.txt', header=None, index=None, sep='\t', mode='a')

    

def main():
    global args
    args = parser.parse_args() 
    path = args.file
    images = args.images

    #Generate KITTI cumulated file
    ##Unzip File
    try:
        with zipfile.ZipFile(path, 'r') as zip_ref:
            zip_ref.extractall('.')
    except:
        pass 

    #Generate KITTI cummulated file
    path, dirs, files = next(os.walk("kitty_track/"))
    path = 'kitty_track/'
    filenames = files
    kitti_cumulated = 'KITTI_cummulated.txt'
    with open(kitti_cumulated, 'w') as outfile:
        for fname in filenames:
            with open(os.path.join(path,fname)) as infile:
                for line in infile:
                    name= fname.split('_')[2]
                    name = name.split(".")[0]
                    to_write = name +' '+ line
                    outfile.write(to_write)

    #outputName = zip_path.split(".")[0] + '_KITTI_OUTPUT.txt'
    
    #Generate formated JSON file
    #formatFile(kitti_cumulated, images)
    
    # Generate Original Kitti Format from DeepStream Fortmat
    formatToFullKitti(kitti_cumulated,images)



if __name__ == '__main__':
    main()
    
# Example of run argument:

# python3 file_formater_DS_to_KITTI-new.py -file kitti_track -images frames/


# -images should recive the path to the image folder with the specific frames (0000.png) (0001.png) etc
# -file kitti_track should recieve the path to the folder with the labels (0000.txt) (00001.txt)

# The script will create two text files:
# KITTI_CUMMULATED - cummulated file of all the text files with the specific label
# KITTI_CUMMULATED-FORMATED. This is the one you should use on the Track Eval Software. It has the correct format

