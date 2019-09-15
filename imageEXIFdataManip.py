'''
methods to get the GPS data and Datetime from image files as well as compare the two
based on https://gist.github.com/snakeye/fdc372dbf11370fe29eb
and https://gist.github.com/erans/983821
'''
import exifread
import numpy as np
import datetime


def get_all_exif_tags(image_file):
    """
    Iterates through all the EXIF tags and their data
    """
    with open(image_file, 'rb') as f:
        tags = exifread.process_file(f)
        
    for tag in tags.keys():
        if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
            print("Key: %s, value %s" % (tag, tags[tag]))

def get_exif_data(image_file):
    """
    Gets the EXIF data from image files
    """
    with open(image_file, 'rb') as f:
        exif_tags = exifread.process_file(f)
    return exif_tags 

def get_if_exist(data, key):
    """
    If a particular key exists in a dictionary, return the value paired with that key, otherwise return None
    """
    if key in data:
        return data[key]

    return None
    
def convert_to_degrees(value):
    """
    Converts the GPS coordinates stored in the EXIF to degress in float format
    :param value:
    :type value: exifread.utils.Ratio
    :rtype: float
    """
    #print("more testing stuff")
    d = float(value.values[0].num) / float(value.values[0].den)
    #print("num: " + str(value.values[0].num))
    #print("den: " + str(value.values[0].den))
    
    m = float(value.values[1].num) / float(value.values[1].den)
    #print("num: " + str(value.values[1].num))
    #print("den: " + str(value.values[1].den))
    
    s = float(value.values[2].num) / float(value.values[2].den)
    #print("num: " + str(value.values[2].num))
    #print("den: " + str(value.values[2].den))

    return d + (m / 60) + (s / 3600)    
    
def get_exif_location(exif_data):
    """
    Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above) as degrees
    """
    lat = None
    lon = None

    gps_latitude = get_if_exist(exif_data, 'GPS GPSLatitude')
    gps_latitude_ref = get_if_exist(exif_data, 'GPS GPSLatitudeRef')
    gps_longitude = get_if_exist(exif_data, 'GPS GPSLongitude')
    gps_longitude_ref = get_if_exist(exif_data, 'GPS GPSLongitudeRef')

    if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
        lat = convert_to_degrees(gps_latitude)
        if gps_latitude_ref.values[0] != 'N':
            lat *= -1 #lat = 0 - lat

        lon = convert_to_degrees(gps_longitude)
        if gps_longitude_ref.values[0] != 'E':
            lon *= -1 #lon = 0 - lon

    return lat, lon
    
def get_distance_lat_long(point1, point2):
    """
    Returns the distance between two points (lat1,long1) and (lat2,long2)
    This uses the ‘haversine’ formula to calculate the great-circle distance between two points
    the shortest distance over the earth’s surface – giving an ‘as-the-crow-flies’ distance between the points 
    (ignoring any hills they fly over, of course!).
    Haversine formula:    a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
    c = 2 ⋅ atan2( √a, √(1−a) )
    d = R ⋅ c
    where   φ is latitude, λ is longitude, R is earth’s radius (mean radius = 6,371km);
    note that angles need to be in radians to pass to trig functions!
    """
    dist = -1
    
    if point1 and point2:
        lat1, lon1 = point1
        lat2, lon2 = point2
        
    if lat1 and lat2 and lon1 and lon2:
        #Radius of the earth
        R = 6371.0088
        #Convert to radians
        lat1,lon1,lat2,lon2 = map(np.radians, [lat1,lon1,lat2,lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2) **2
        c = 2 * np.arctan2(a**0.5, (1-a)**0.5)
        d = R * c
        dist = d
        #dist = round(d,4)
    
    if dist == -1:
        #Error!
        print("Something went wrong here. One of the points is completely invalid")
    
    
    return dist
    
def get_location_from_image(image_file):
    """
    Putting it all together now
        get_exif_data() - Retrieve EXIF data from image file 
        get_exif_location() - Retrieve GPS Latitude and Longtitude from EXIF data in degrees
        returns a tuple of (lat,lon)
        
    """
    exif_data = get_exif_data(image_file)
    gps_coords = get_exif_location(exif_data)
    return gps_coords

def get_datetime_from_image(image_file):
    """
    Returns the date and time, if available from the exif_data
    Need to convert it into UTC + 5
    """
    exif_data = get_exif_data(image_file)
    get_time = get_if_exist(exif_data, 'Image DateTime') #BE VERY CAREFUL ABOUT THE CASING WITH THE KEYS
    
    datetimeobj = datetime.datetime.strptime( str(get_time), "%Y:%m:%d %H:%M:%S")
    datetimestr = datetimeobj.strftime("%Y%m%d") #No need for time
    
    #get_time_str = "_".join( str(get_time).split(" ") )
    
    return datetimestr

"""
TEST_IMAGE = "C:\\EXIFdataImageSortingProjectForDaddy\\Python 3.6 version\\input\\20190915_143308.jpg"
lat, lon = get_location_from_image(TEST_IMAGE)
time = get_datetime_from_image(TEST_IMAGE)
print("This image was taken at position\nLatitude: %f\nLongtitude: %f"%(lat, lon))
print("This image was taken on %s"%(str(time)) )
"""
