import pandas as pd
import csv
import os
import argparse
import logging
import json 


# Level of warnings
logging.basicConfig(format='[%(levelname)s]: %(message)s', level=logging.NOTSET) 

#Parser
parser = argparse.ArgumentParser(description='JSON file formater')
parser.add_argument('-file', type=str, required=True, help='path to zip containing KITTI files')
parser.add_argument('-images', type=str, required=True, help='path to images')

def formatFile(path, images):
    #Read specific columns from csv file
    col_list = ["frame_id","type","tracker_id", "truncated", "occluded", "alpha", "bbox1","bbox2","bbox3","bbox4", "dimensions1","dimensions2","dimensions3", "location1","location2","location3","rotation_y","score"]
    df_kitty_original = pd.read_csv(path, sep=' ', header=None, names=col_list)
    df_kitty = df_kitty_original[["frame_id","tracker_id","type", "truncated", "occluded", "alpha", "bbox1","bbox2","bbox3","bbox4", "dimensions1","dimensions2","dimensions3", "location1","location2","location3","rotation_y","score"]]

    annotations = {}
    ext = ".jpg"
    new = {}
    current_frame = None
    size = 596 #EDIT
    countif = 0
    counter=0
    for index, row in df_kitty.iterrows():
        #size = os.path.getsize(row['frame_id'] + ext)
        frameKey = row["frame_id"] +ext+ str(size)
        #print(row["frame_id"])
        if current_frame != row["frame_id"]:
            
            regions = []
            size = b = os.path.getsize(images+row["frame_id"]+ext)
            countif +=1
            current_frame = row["frame_id"]
            shape_attributes = {"name":"rect","x":row["bbox1"],"y":row["bbox2"],"width":row["bbox3"] - row["bbox1"],"height":row["bbox4"] - row["bbox2"]}
            region_attributes = {"tracker id":str(row["tracker_id"]),"frame_id":row["frame_id"],"class":row["type"]}
            regions.append({ 
                "shape_attributes": shape_attributes, 
                "region_attributes": region_attributes}
            )
        else:
            
            shape_attributes = {"name":"rect","x":row["bbox1"],"y":row["bbox2"],"width":row["bbox3"] - row["bbox1"],"height":row["bbox4"] - row["bbox2"]}
            region_attributes = {"tracker id":str(row["tracker_id"]),"frame_id":row["frame_id"],"class":row["type"]}
            regions.append({ 
                "shape_attributes": shape_attributes, 
                "region_attributes": region_attributes}
            )
        

        sub1 = {"filename": row["frame_id"]+ext, "size": size, "regions": regions, "file_attributes": {}}
        annotations[frameKey] =  sub1

    with open('formated_JSON_'+path+".json", 'w') as f:
        json.dump(annotations,f)



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
                    name = fname.split(".")[0]
                    to_write = name +' '+ line
                    outfile.write(to_write)

    #outputName = zip_path.split(".")[0] + '_KITTI_OUTPUT.txt'
    
    #Generate formated JSON file
    formatFile(kitti_cumulated, images)



if __name__ == '__main__':
    main()
