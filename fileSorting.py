import imageEXIFdataManip as imex
import os, shutil


#parameters that can probably be handled externally or changed later if you're careful
REFERENCE_POINTS_PATH = "ReferencePoints.csv"
IMAGES_UNSORTED_PATH = "input"
IMAGES_SORTED_PATH = "output"
IMAGE_EXTENSIONS_VALID = ['jpg','JPG','jpeg','JPEG','png','PNG','tiff','TIFF','tif','TIF','BMP','bmp']
DISTANCE_LIMIT = 0.009144 #approx 30 ft.
RADIUS_EARTH = 6371.0088

#global variables
REFERENCE_POINTS_DICT = None


def load_reference_points(path = REFERENCE_POINTS_PATH):
    """
    Loads the coordinates of all the reference points into a dict
    Reference Point Name: (latitude, longtitude)
    
    the coordinates are stored as a tuple of two floating point values in the dict, whereas the key is a string
    """
    global REFERENCE_POINTS_DICT
    dict, file_lines = {}, []
    
    with open(path) as f:
        file_lines = f.readlines()
    
    if file_lines:    
        for line in file_lines[1:]:
            line_stripped = line.strip() #REMEMBER TO STRIP WHITESPACE
            
            name, latitude_str, longtitude_str = line_stripped.split(",") #If the data is properly formatted this should work
            lat, lon = 0.0, 0.0
            
            #Convert strings into floating point values
            lat = float(latitude_str[:-1])
            if latitude_str[-1] != 'N': lat *= -1
            
            lon = float(longtitude_str[:-1])
            if longtitude_str[-1] != 'E': lon *= -1
            
            dict[name] = (lat, lon)
               
    REFERENCE_POINTS_DICT = dict
    return dict

def print_list_of_reference_points():
    """
    This method prints the list of reference points the app uses to console
    """
    global REFERENCE_POINTS_DICT
    
    if REFERENCE_POINTS_DICT:
        for key in REFERENCE_POINTS_DICT.keys():
            lat, lon = REFERENCE_POINTS_DICT[key]
            print("LOCATION NAME: %s, COORDINATES: %4f, %4f"%(key, lat, lon))
    
def get_list_of_images(path = IMAGES_UNSORTED_PATH):
    """
    Returns a list of all the images in a given path
    """
    file_names = [ IMAGES_UNSORTED_PATH+"//"+fn for fn in os.listdir(path) if any(fn.endswith(ext) for ext in IMAGE_EXTENSIONS_VALID)]
    
    
    return file_names
    
def get_dict_images_coords(image_list):    
    """
    Makes a dictionary of each image and the GPS coordinates found in each one using methods in imageEXIFdataManip module
    """
    dict = {}
    
    for image in image_list:
        lat, lon = imex.get_location_from_image(image)
        dict[image] = (lat, lon)
    
    return dict
    
def get_nearest_reference_point(image, coord):
    """
    For each image, retrieve the distance to each of the "reference point"
    """
    position1 = coord #Coordinates of image
        
    distances = []
    for reference_point in REFERENCE_POINTS_DICT.keys():
        position2 = REFERENCE_POINTS_DICT[reference_point]
        dist = imex.get_distance_lat_long(position1, position2)
        distances.append((reference_point, dist))
        
    print("for %s the distances are:"%(image))
    for ref, dist in distances:
        print("%s: %3f"%(ref,dist))
    
    min_dist = RADIUS_EARTH
    min_ref = "None"
    for ref, dist in distances:
        if dist <= min_dist: 
            min_dist, min_ref = dist, ref
            
    print("for %s the selected reference point is %s\n"%(image, min_ref))

    print("List of files output:\n")
    return str(min_ref)
    
def make_folder(newpath):
    """
    Create subfolders in the output directory for each location/reference point
    """
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    
    pass
       
def output_images_to_new_folder(input_path = IMAGES_UNSORTED_PATH, output_path = IMAGES_SORTED_PATH):
    """
    Take images, determine the nearest reference point to them, and save them to the output folder with the filename REFERENCEPOINT_DATETIME
    """
    #Get dictionary of reference points
    load_reference_points(REFERENCE_POINTS_PATH)
    
    #Get list of images to sort
    file_names = get_list_of_images(input_path)
    out_file_names = []
    
    for src in file_names:    
        #GPS coordinate of image
        lat, lon = imex.get_location_from_image(src)    
        #Datetime of image
        datetime = imex.get_datetime_from_image(src)
        #Nearest reference point to image
        location_name = get_nearest_reference_point(src, (lat, lon))
        
        #extension of image
        file_ext = os.path.splitext(src)[1]        
        
        #folder of output image
        dst_folder = output_path + "\\" + location_name 
        make_folder(dst_folder)
        
        #full filename of image
        image_number = 1
        dst = dst_folder + "\\" + location_name + "_" + str(datetime) + "_" + str(image_number) + str(file_ext)
        
        #prevent filename collisions
        while os.path.exists(dst):
            image_number += 1
            dst = dst_folder + "\\" + location_name + "_" + str(datetime) + "_" + str(image_number) + str(file_ext)
            #forcibly prevent while loop nonsense
            if (image_number > 99999999): 
                print("okay, that's really odd. what's going on here?")
                break
        
        #copy the input file to the output folder
        out_file_names.append(dst)
        shutil.copy2(src,dst)
    
    print("\n".join(out_file_names))
    #Return a list of the files created
    return out_file_names 


"""
#TEST THE REFERENCE POINTS LOADING METHOD
print("+"*64)
print("LIST OF REFERENCE POINTS:")
print("+"*64)
load_reference_points(REFERENCE_POINTS_PATH)
print_list_of_reference_points()
print()
print("+"*64)

#TEST THE METHOD THAT LOADS THE LIST OF IMAGES TO BE SORTED
#AND THE METHOD THAT GETS THEIR COORDINATES
input_files_list = get_list_of_images()
IMAGES_COORDS_DICT = get_dict_images_coords(input_files_list)
print("IMAGES FOUND AND THEIR CORRESPONDING GPS COORDINATES:")
print("+"*64)
for image in IMAGES_COORDS_DICT.keys():
    lat, lon = IMAGES_COORDS_DICT[image]
    print("FILENAME: %s, COORDINATES: %4f, %4f"%(image, lat, lon))

print()
print("+"*64)

#TEST THE METHOD THAT CALCULATES DISTANCE TO EACH REFERENCE POINT FOR AN IMAGE
#print("NOW TESTING THE METHODS FOR GETTING THE DISTANCE TO EACH REFERENCE POINT")
#print("+"*64)
#test_image = list(IMAGES_COORDS_DICT.keys())[1]
#test_location = IMAGES_COORDS_DICT[test_image]
#get_nearest_reference_point(test_image, test_location)
#print("+"*64)   

#TEST THE METHOD THAT MAKES A NEW FILENAME FOR EACH IMAGE
print("NOW TESTING THE METHOD FOR GETTING THE NEW FILE NAMES")
print("+"*64)
output_images_to_new_folder(IMAGES_UNSORTED_PATH, IMAGES_SORTED_PATH)
print("+"*64) 
"""